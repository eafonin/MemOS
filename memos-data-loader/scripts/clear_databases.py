#!/usr/bin/env python3
"""
Clear Neo4j and Qdrant databases for MemOS testing.
Provides clean slate for loading documents.
"""

import sys
from neo4j import GraphDatabase
from qdrant_client import QdrantClient

def clear_neo4j(uri: str, user: str, password: str):
    """Clear all data from Neo4j database."""
    print("🔄 Connecting to Neo4j...")
    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        with driver.session() as session:
            # Count nodes before
            count_before = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
            print(f"   Nodes before: {count_before:,}")

            # Delete all nodes and relationships
            print("🗑️  Deleting all nodes and relationships...")
            session.run("MATCH (n) DETACH DELETE n")

            # Count nodes after
            count_after = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
            print(f"   Nodes after: {count_after:,}")
            print("✅ Neo4j cleared successfully")

            return count_before
    finally:
        driver.close()

def clear_qdrant(host: str, port: int):
    """Clear all collections from Qdrant."""
    print(f"\n🔄 Connecting to Qdrant at {host}:{port}...")
    client = QdrantClient(host=host, port=port)

    try:
        # Get all collections
        collections = client.get_collections().collections
        print(f"   Found {len(collections)} collection(s)")

        total_vectors = 0
        for coll in collections:
            info = client.get_collection(coll.name)
            vectors_count = info.vectors_count
            total_vectors += vectors_count
            print(f"   - {coll.name}: {vectors_count:,} vectors")

        # Delete all collections
        print("🗑️  Deleting all collections...")
        for coll in collections:
            client.delete_collection(coll.name)
            print(f"   Deleted: {coll.name}")

        print(f"✅ Qdrant cleared successfully ({total_vectors:,} vectors removed)")
        return total_vectors

    except Exception as e:
        print(f"❌ Error clearing Qdrant: {e}")
        return 0

def main():
    """Main function."""
    print("=" * 60)
    print("  MemOS Database Cleanup")
    print("=" * 60)
    print()

    # Neo4j configuration
    neo4j_uri = "bolt://localhost:7688"
    neo4j_user = "neo4j"
    neo4j_password = "memospassword123"

    # Qdrant configuration
    qdrant_host = "localhost"
    qdrant_port = 6334

    try:
        # Clear Neo4j
        nodes_deleted = clear_neo4j(neo4j_uri, neo4j_user, neo4j_password)

        # Clear Qdrant
        vectors_deleted = clear_qdrant(qdrant_host, qdrant_port)

        print()
        print("=" * 60)
        print("  Summary")
        print("=" * 60)
        print(f"✅ Neo4j nodes deleted: {nodes_deleted:,}")
        print(f"✅ Qdrant vectors deleted: {vectors_deleted:,}")
        print(f"✅ Databases are now clean and ready for testing")
        print()

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
