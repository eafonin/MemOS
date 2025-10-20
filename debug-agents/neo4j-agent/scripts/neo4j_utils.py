#!/usr/bin/env python3
"""
Neo4j Debug Agent - Utilities for MemOS Data Debugging

This script provides utilities to:
- Authenticate and test Neo4j connections
- Query and inspect data structure
- Verify data was loaded correctly
- Clean/reset test data
- Troubleshoot connection issues
"""

import os
import sys
from typing import Optional, Dict, List, Any
from datetime import datetime
import json

try:
    from neo4j import GraphDatabase
    from neo4j.exceptions import ServiceUnavailable, AuthError
except ImportError:
    print("ERROR: neo4j package not installed. Install with: pip install neo4j")
    sys.exit(1)


class Neo4jDebugAgent:
    """Debug agent for Neo4j database operations"""

    def __init__(
        self,
        uri: str = "bolt://localhost:7688",
        user: str = "neo4j",
        password: str = "memospassword123",
        database: str = "test1_memos_db"
    ):
        """
        Initialize Neo4j connection

        Args:
            uri: Neo4j connection URI
            user: Neo4j username
            password: Neo4j password
            database: Database name to use
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.database = database
        self.driver = None

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def connect(self) -> bool:
        """
        Establish connection to Neo4j

        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test connection
            self.driver.verify_connectivity()
            print(f"✓ Connected to Neo4j at {self.uri}")
            print(f"✓ Database: {self.database}")
            return True
        except ServiceUnavailable as e:
            print(f"✗ Connection failed: Neo4j service unavailable at {self.uri}")
            print(f"  Error: {e}")
            return False
        except AuthError as e:
            print(f"✗ Authentication failed: Invalid credentials")
            print(f"  Error: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            print("✓ Connection closed")

    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection and return server info

        Returns:
            Dictionary with connection status and server info
        """
        if not self.driver:
            return {"connected": False, "error": "No driver initialized"}

        try:
            with self.driver.session(database=self.database) as session:
                result = session.run("CALL dbms.components() YIELD name, versions, edition")
                record = result.single()

                info = {
                    "connected": True,
                    "uri": self.uri,
                    "database": self.database,
                    "name": record["name"],
                    "versions": record["versions"],
                    "edition": record["edition"]
                }

                print(f"\n{'='*60}")
                print(f"Neo4j Connection Test Results")
                print(f"{'='*60}")
                print(f"Status:     ✓ Connected")
                print(f"URI:        {info['uri']}")
                print(f"Database:   {info['database']}")
                print(f"Name:       {info['name']}")
                print(f"Version:    {', '.join(info['versions'])}")
                print(f"Edition:    {info['edition']}")
                print(f"{'='*60}\n")

                return info
        except Exception as e:
            error_info = {"connected": False, "error": str(e)}
            print(f"\n✗ Connection test failed: {e}\n")
            return error_info

    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics

        Returns:
            Dictionary with node counts, relationship counts, etc.
        """
        if not self.driver:
            return {"error": "No driver initialized"}

        try:
            with self.driver.session(database=self.database) as session:
                stats = {}

                # Count nodes by label
                result = session.run("""
                    CALL db.labels() YIELD label
                    CALL apoc.cypher.run('MATCH (n:`' + label + '`) RETURN count(n) as count', {})
                    YIELD value
                    RETURN label, value.count as count
                    ORDER BY count DESC
                """)

                # If APOC is not available, use basic query
                try:
                    node_counts = {record["label"]: record["count"] for record in result}
                except:
                    # Fallback without APOC
                    result = session.run("MATCH (n) RETURN labels(n) as labels, count(n) as count")
                    node_counts = {}
                    for record in result:
                        for label in record["labels"]:
                            node_counts[label] = node_counts.get(label, 0) + record["count"]

                stats["nodes_by_label"] = node_counts
                stats["total_nodes"] = sum(node_counts.values())

                # Count relationships by type
                result = session.run("""
                    MATCH ()-[r]->()
                    RETURN type(r) as type, count(r) as count
                    ORDER BY count DESC
                """)
                rel_counts = {record["type"]: record["count"] for record in result}
                stats["relationships_by_type"] = rel_counts
                stats["total_relationships"] = sum(rel_counts.values())

                # Print stats
                print(f"\n{'='*60}")
                print(f"Database Statistics: {self.database}")
                print(f"{'='*60}")
                print(f"\nNodes:")
                for label, count in node_counts.items():
                    print(f"  {label}: {count:,}")
                print(f"  Total: {stats['total_nodes']:,}")

                print(f"\nRelationships:")
                for rel_type, count in rel_counts.items():
                    print(f"  {rel_type}: {count:,}")
                print(f"  Total: {stats['total_relationships']:,}")
                print(f"{'='*60}\n")

                return stats
        except Exception as e:
            print(f"✗ Error getting database stats: {e}")
            return {"error": str(e)}

    def inspect_data_structure(self, limit: int = 5) -> Dict[str, Any]:
        """
        Inspect data structure and show sample records

        Args:
            limit: Number of sample records to show per label

        Returns:
            Dictionary with sample data for each node type
        """
        if not self.driver:
            return {"error": "No driver initialized"}

        try:
            with self.driver.session(database=self.database) as session:
                # Get all labels
                result = session.run("CALL db.labels() YIELD label RETURN label")
                labels = [record["label"] for record in result]

                print(f"\n{'='*60}")
                print(f"Data Structure Inspection")
                print(f"{'='*60}\n")

                samples = {}
                for label in labels:
                    print(f"Label: {label}")
                    print(f"{'-'*60}")

                    # Get sample nodes
                    result = session.run(
                        f"MATCH (n:`{label}`) RETURN n LIMIT $limit",
                        limit=limit
                    )

                    label_samples = []
                    for i, record in enumerate(result, 1):
                        node = dict(record["n"])
                        label_samples.append(node)

                        print(f"\n  Sample {i}:")
                        for key, value in node.items():
                            # Truncate long values
                            value_str = str(value)
                            if len(value_str) > 100:
                                value_str = value_str[:100] + "..."
                            print(f"    {key}: {value_str}")

                    samples[label] = label_samples
                    print(f"\n{'-'*60}\n")

                return samples
        except Exception as e:
            print(f"✗ Error inspecting data structure: {e}")
            return {"error": str(e)}

    def query(self, cypher: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Execute a custom Cypher query

        Args:
            cypher: Cypher query string
            params: Query parameters

        Returns:
            List of result records as dictionaries
        """
        if not self.driver:
            return [{"error": "No driver initialized"}]

        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(cypher, params or {})
                records = [dict(record) for record in result]

                print(f"\nQuery executed successfully. Returned {len(records)} records.\n")

                # Print results in a nice format
                if records:
                    for i, record in enumerate(records[:10], 1):  # Show first 10
                        print(f"Record {i}:")
                        for key, value in record.items():
                            value_str = str(value)
                            if len(value_str) > 200:
                                value_str = value_str[:200] + "..."
                            print(f"  {key}: {value_str}")
                        print()

                    if len(records) > 10:
                        print(f"... and {len(records) - 10} more records\n")

                return records
        except Exception as e:
            print(f"✗ Query failed: {e}")
            return [{"error": str(e)}]

    def verify_memos_data(self) -> Dict[str, Any]:
        """
        Verify that MemOS data was loaded correctly

        Returns:
            Dictionary with verification results
        """
        if not self.driver:
            return {"error": "No driver initialized"}

        print(f"\n{'='*60}")
        print(f"MemOS Data Verification")
        print(f"{'='*60}\n")

        checks = {}

        # Check for typical MemOS node types
        memos_labels = ["MemoryNode", "Chunk", "Document", "Memory", "Entity", "Concept"]

        with self.driver.session(database=self.database) as session:
            for label in memos_labels:
                try:
                    result = session.run(
                        f"MATCH (n:`{label}`) RETURN count(n) as count"
                    )
                    count = result.single()["count"]
                    checks[label] = count

                    status = "✓" if count > 0 else "✗"
                    print(f"{status} {label}: {count:,} nodes")
                except:
                    checks[label] = 0
                    print(f"  {label}: Not found")

            # Check for relationships
            print(f"\nRelationships:")
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(r) as count
                ORDER BY count DESC
                LIMIT 10
            """)

            for record in result:
                print(f"  {record['type']}: {record['count']:,}")

        print(f"\n{'='*60}\n")
        return checks

    def delete_all_data(self, confirm: bool = False) -> bool:
        """
        Delete all data from the database

        Args:
            confirm: Must be True to actually delete data (safety check)

        Returns:
            True if deletion successful
        """
        if not confirm:
            print("⚠ WARNING: This will delete ALL data from the database!")
            print("⚠ Call with confirm=True to proceed")
            return False

        if not self.driver:
            print("✗ No driver initialized")
            return False

        try:
            with self.driver.session(database=self.database) as session:
                print(f"\nDeleting all data from {self.database}...")

                # Delete in batches to avoid memory issues
                batch_size = 10000
                deleted_total = 0

                while True:
                    result = session.run(f"""
                        MATCH (n)
                        WITH n LIMIT {batch_size}
                        DETACH DELETE n
                        RETURN count(n) as deleted
                    """)
                    deleted = result.single()["deleted"]
                    deleted_total += deleted

                    if deleted > 0:
                        print(f"  Deleted {deleted:,} nodes (total: {deleted_total:,})")

                    if deleted < batch_size:
                        break

                print(f"\n✓ All data deleted. Total nodes deleted: {deleted_total:,}\n")
                return True
        except Exception as e:
            print(f"✗ Error deleting data: {e}")
            return False

    def delete_by_user(self, user_id: str, confirm: bool = False) -> bool:
        """
        Delete data for a specific user

        Args:
            user_id: User ID to delete data for
            confirm: Must be True to actually delete data

        Returns:
            True if deletion successful
        """
        if not confirm:
            print(f"⚠ WARNING: This will delete all data for user: {user_id}")
            print("⚠ Call with confirm=True to proceed")
            return False

        if not self.driver:
            print("✗ No driver initialized")
            return False

        try:
            with self.driver.session(database=self.database) as session:
                # Try different user identifier patterns
                user_patterns = [
                    f"MATCH (n {{user_id: '{user_id}'}})",
                    f"MATCH (n {{userId: '{user_id}'}})",
                    f"MATCH (n {{owner: '{user_id}'}})",
                    f"MATCH (n) WHERE n.user_id = '{user_id}' OR n.userId = '{user_id}' OR n.owner = '{user_id}'"
                ]

                total_deleted = 0
                for pattern in user_patterns:
                    result = session.run(f"""
                        {pattern}
                        WITH n LIMIT 10000
                        DETACH DELETE n
                        RETURN count(n) as deleted
                    """)
                    deleted = result.single()["deleted"]
                    if deleted > 0:
                        print(f"  Deleted {deleted:,} nodes for user {user_id}")
                        total_deleted += deleted

                if total_deleted == 0:
                    print(f"⚠ No data found for user: {user_id}")
                else:
                    print(f"\n✓ Total deleted for user {user_id}: {total_deleted:,}\n")

                return True
        except Exception as e:
            print(f"✗ Error deleting user data: {e}")
            return False


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Neo4j Debug Agent for MemOS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test connection
  python neo4j_utils.py --test

  # Show database statistics
  python neo4j_utils.py --stats

  # Inspect data structure
  python neo4j_utils.py --inspect

  # Verify MemOS data
  python neo4j_utils.py --verify

  # Custom query
  python neo4j_utils.py --query "MATCH (n) RETURN count(n) as total"

  # Delete all data (DANGEROUS!)
  python neo4j_utils.py --delete-all --confirm

  # Delete user data
  python neo4j_utils.py --delete-user test1_user --confirm
        """
    )

    # Connection options
    parser.add_argument("--uri", default=os.getenv("NEO4J_URI", "bolt://localhost:7688"),
                       help="Neo4j URI (default: bolt://localhost:7688)")
    parser.add_argument("--user", default=os.getenv("NEO4J_USER", "neo4j"),
                       help="Neo4j username")
    parser.add_argument("--password", default=os.getenv("NEO4J_PASSWORD", "memospassword123"),
                       help="Neo4j password")
    parser.add_argument("--database", default=os.getenv("NEO4J_DB_NAME", "test1_memos_db"),
                       help="Database name")

    # Actions
    parser.add_argument("--test", action="store_true",
                       help="Test connection and show server info")
    parser.add_argument("--stats", action="store_true",
                       help="Show database statistics")
    parser.add_argument("--inspect", action="store_true",
                       help="Inspect data structure")
    parser.add_argument("--verify", action="store_true",
                       help="Verify MemOS data was loaded")
    parser.add_argument("--query", type=str,
                       help="Execute custom Cypher query")
    parser.add_argument("--delete-all", action="store_true",
                       help="Delete all data (requires --confirm)")
    parser.add_argument("--delete-user", type=str,
                       help="Delete data for specific user (requires --confirm)")
    parser.add_argument("--confirm", action="store_true",
                       help="Confirm destructive operations")

    args = parser.parse_args()

    # Create agent
    agent = Neo4jDebugAgent(
        uri=args.uri,
        user=args.user,
        password=args.password,
        database=args.database
    )

    # Connect
    if not agent.connect():
        sys.exit(1)

    try:
        # Execute requested action
        if args.test:
            agent.test_connection()
        elif args.stats:
            agent.get_database_stats()
        elif args.inspect:
            agent.inspect_data_structure()
        elif args.verify:
            agent.verify_memos_data()
        elif args.query:
            agent.query(args.query)
        elif args.delete_all:
            agent.delete_all_data(confirm=args.confirm)
        elif args.delete_user:
            agent.delete_by_user(args.delete_user, confirm=args.confirm)
        else:
            parser.print_help()
    finally:
        agent.close()


if __name__ == "__main__":
    main()
