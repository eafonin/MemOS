#!/usr/bin/env python3
"""
Qdrant Debug Agent - Utilities for MemOS Data Debugging

This script provides utilities to:
- Authenticate and test Qdrant connections
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
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    from qdrant_client.http.exceptions import UnexpectedResponse
except ImportError:
    print("ERROR: qdrant-client package not installed. Install with: pip install qdrant-client")
    sys.exit(1)


class QdrantDebugAgent:
    """Debug agent for Qdrant vector database operations"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6334,
        api_key: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize Qdrant connection

        Args:
            host: Qdrant host
            port: Qdrant port
            api_key: API key (if authentication enabled)
            timeout: Connection timeout in seconds
        """
        self.host = host
        self.port = port
        self.api_key = api_key
        self.timeout = timeout
        self.client = None

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def connect(self) -> bool:
        """
        Establish connection to Qdrant

        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.client = QdrantClient(
                host=self.host,
                port=self.port,
                api_key=self.api_key,
                timeout=self.timeout
            )

            # Test connection by getting collections
            collections = self.client.get_collections()
            print(f"✓ Connected to Qdrant at {self.host}:{self.port}")
            print(f"✓ Found {len(collections.collections)} collection(s)")
            return True
        except Exception as e:
            print(f"✗ Connection failed to {self.host}:{self.port}")
            print(f"  Error: {e}")
            return False

    def close(self):
        """Close Qdrant connection"""
        if self.client:
            self.client.close()
            print("✓ Connection closed")

    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection and return server info

        Returns:
            Dictionary with connection status and server info
        """
        if not self.client:
            return {"connected": False, "error": "No client initialized"}

        try:
            collections = self.client.get_collections()

            info = {
                "connected": True,
                "host": self.host,
                "port": self.port,
                "collections_count": len(collections.collections),
                "collections": [col.name for col in collections.collections]
            }

            print(f"\n{'='*60}")
            print(f"Qdrant Connection Test Results")
            print(f"{'='*60}")
            print(f"Status:      ✓ Connected")
            print(f"Host:        {info['host']}:{info['port']}")
            print(f"Collections: {info['collections_count']}")
            if info['collections']:
                print(f"\nCollections:")
                for col in info['collections']:
                    print(f"  - {col}")
            print(f"{'='*60}\n")

            return info
        except Exception as e:
            error_info = {"connected": False, "error": str(e)}
            print(f"\n✗ Connection test failed: {e}\n")
            return error_info

    def list_collections(self) -> List[str]:
        """
        List all collections

        Returns:
            List of collection names
        """
        if not self.client:
            print("✗ No client initialized")
            return []

        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            print(f"\n{'='*60}")
            print(f"Qdrant Collections ({len(collection_names)})")
            print(f"{'='*60}")

            for name in collection_names:
                print(f"  - {name}")

            print(f"{'='*60}\n")

            return collection_names
        except Exception as e:
            print(f"✗ Error listing collections: {e}")
            return []

    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a collection

        Args:
            collection_name: Name of the collection

        Returns:
            Dictionary with collection info
        """
        if not self.client:
            return {"error": "No client initialized"}

        try:
            collection_info = self.client.get_collection(collection_name)

            info = {
                "name": collection_name,
                "vectors_count": collection_info.points_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count,
                "segments_count": collection_info.segments_count,
                "status": collection_info.status,
                "optimizer_status": collection_info.optimizer_status,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
            }

            print(f"\n{'='*60}")
            print(f"Collection Info: {collection_name}")
            print(f"{'='*60}")
            print(f"Vectors Count:        {info['vectors_count']:,}")
            print(f"Indexed Vectors:      {info['indexed_vectors_count']:,}")
            print(f"Segments:             {info['segments_count']}")
            print(f"Status:               {info['status']}")
            print(f"Optimizer Status:     {info['optimizer_status']}")
            print(f"Vector Size:          {info['vector_size']}")
            print(f"Distance Metric:      {info['distance']}")
            print(f"{'='*60}\n")

            return info
        except Exception as e:
            print(f"✗ Error getting collection info: {e}")
            return {"error": str(e)}

    def get_all_stats(self) -> Dict[str, Any]:
        """
        Get statistics for all collections

        Returns:
            Dictionary with stats for all collections
        """
        if not self.client:
            return {"error": "No client initialized"}

        try:
            collections = self.client.get_collections()
            stats = {}

            print(f"\n{'='*60}")
            print(f"Qdrant Database Statistics")
            print(f"{'='*60}")
            print(f"Total Collections: {len(collections.collections)}\n")

            total_vectors = 0
            for col in collections.collections:
                col_info = self.client.get_collection(col.name)
                vectors_count = col_info.points_count

                stats[col.name] = {
                    "vectors_count": vectors_count,
                    "vector_size": col_info.config.params.vectors.size,
                    "distance": col_info.config.params.vectors.distance
                }

                total_vectors += vectors_count

                print(f"Collection: {col.name}")
                print(f"  Vectors:  {vectors_count:,}")
                print(f"  Dim:      {col_info.config.params.vectors.size}")
                print(f"  Distance: {col_info.config.params.vectors.distance}")
                print()

            print(f"Total Vectors: {total_vectors:,}")
            print(f"{'='*60}\n")

            stats["_total_vectors"] = total_vectors
            stats["_total_collections"] = len(collections.collections)

            return stats
        except Exception as e:
            print(f"✗ Error getting database stats: {e}")
            return {"error": str(e)}

    def inspect_collection(self, collection_name: str, limit: int = 5) -> List[Dict]:
        """
        Inspect collection and show sample vectors

        Args:
            collection_name: Name of the collection
            limit: Number of sample vectors to show

        Returns:
            List of sample points
        """
        if not self.client:
            return [{"error": "No client initialized"}]

        try:
            # Get collection info first
            col_info = self.client.get_collection(collection_name)

            print(f"\n{'='*60}")
            print(f"Collection Inspection: {collection_name}")
            print(f"{'='*60}")
            print(f"Total Vectors: {col_info.points_count:,}")
            print(f"Vector Size:   {col_info.config.params.vectors.size}")
            print(f"\nSample Vectors:\n")

            # Scroll through collection to get samples
            records, _ = self.client.scroll(
                collection_name=collection_name,
                limit=limit,
                with_payload=True,
                with_vectors=False  # Don't show full vectors to save space
            )

            samples = []
            for i, record in enumerate(records, 1):
                point_data = {
                    "id": record.id,
                    "payload": record.payload
                }
                samples.append(point_data)

                print(f"Sample {i}:")
                print(f"  ID: {record.id}")
                print(f"  Payload:")
                for key, value in record.payload.items():
                    value_str = str(value)
                    if len(value_str) > 100:
                        value_str = value_str[:100] + "..."
                    print(f"    {key}: {value_str}")
                print()

            print(f"{'='*60}\n")

            return samples
        except Exception as e:
            print(f"✗ Error inspecting collection: {e}")
            return [{"error": str(e)}]

    def search_similar(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 5
    ) -> List[Dict]:
        """
        Search for similar vectors

        Args:
            collection_name: Name of the collection
            query_vector: Query vector
            limit: Number of results to return

        Returns:
            List of similar points with scores
        """
        if not self.client:
            return [{"error": "No client initialized"}]

        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit
            )

            print(f"\n{'='*60}")
            print(f"Search Results from {collection_name}")
            print(f"{'='*60}\n")

            search_results = []
            for i, result in enumerate(results, 1):
                result_data = {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                }
                search_results.append(result_data)

                print(f"Result {i}:")
                print(f"  Score: {result.score:.4f}")
                print(f"  ID:    {result.id}")
                print(f"  Payload:")
                for key, value in result.payload.items():
                    value_str = str(value)
                    if len(value_str) > 100:
                        value_str = value_str[:100] + "..."
                    print(f"    {key}: {value_str}")
                print()

            print(f"{'='*60}\n")

            return search_results
        except Exception as e:
            print(f"✗ Error searching: {e}")
            return [{"error": str(e)}]

    def verify_memos_data(self) -> Dict[str, Any]:
        """
        Verify that MemOS data was loaded correctly

        Returns:
            Dictionary with verification results
        """
        if not self.client:
            return {"error": "No client initialized"}

        print(f"\n{'='*60}")
        print(f"MemOS Data Verification")
        print(f"{'='*60}\n")

        try:
            collections = self.client.get_collections()
            verification = {}

            # Look for typical MemOS collection patterns
            memos_patterns = ["memos", "memory", "chunk", "document", "embedding"]

            for col in collections.collections:
                col_info = self.client.get_collection(col.name)
                is_memos = any(pattern in col.name.lower() for pattern in memos_patterns)

                verification[col.name] = {
                    "vectors_count": col_info.points_count,
                    "vector_size": col_info.config.params.vectors.size,
                    "is_memos_related": is_memos
                }

                status = "✓" if col_info.points_count > 0 else "✗"
                marker = " [MemOS]" if is_memos else ""
                print(f"{status} {col.name}{marker}: {col_info.points_count:,} vectors (dim={col_info.config.params.vectors.size})")

            print(f"\n{'='*60}\n")
            return verification
        except Exception as e:
            print(f"✗ Error verifying data: {e}")
            return {"error": str(e)}

    def delete_collection(self, collection_name: str, confirm: bool = False) -> bool:
        """
        Delete a collection

        Args:
            collection_name: Name of the collection to delete
            confirm: Must be True to actually delete

        Returns:
            True if deletion successful
        """
        if not confirm:
            print(f"⚠ WARNING: This will delete collection: {collection_name}")
            print("⚠ Call with confirm=True to proceed")
            return False

        if not self.client:
            print("✗ No client initialized")
            return False

        try:
            self.client.delete_collection(collection_name)
            print(f"✓ Collection '{collection_name}' deleted\n")
            return True
        except Exception as e:
            print(f"✗ Error deleting collection: {e}")
            return False

    def delete_all_collections(self, confirm: bool = False) -> bool:
        """
        Delete all collections

        Args:
            confirm: Must be True to actually delete

        Returns:
            True if deletion successful
        """
        if not confirm:
            print("⚠ WARNING: This will delete ALL collections!")
            print("⚠ Call with confirm=True to proceed")
            return False

        if not self.client:
            print("✗ No client initialized")
            return False

        try:
            collections = self.client.get_collections()
            deleted_count = 0

            print(f"\nDeleting {len(collections.collections)} collections...")

            for col in collections.collections:
                self.client.delete_collection(col.name)
                print(f"  ✓ Deleted: {col.name}")
                deleted_count += 1

            print(f"\n✓ All collections deleted. Total: {deleted_count}\n")
            return True
        except Exception as e:
            print(f"✗ Error deleting collections: {e}")
            return False

    def clear_collection(self, collection_name: str, confirm: bool = False) -> bool:
        """
        Clear all vectors from a collection (but keep the collection)

        Args:
            collection_name: Name of the collection
            confirm: Must be True to actually clear

        Returns:
            True if clearing successful
        """
        if not confirm:
            print(f"⚠ WARNING: This will delete all vectors from: {collection_name}")
            print("⚠ Call with confirm=True to proceed")
            return False

        if not self.client:
            print("✗ No client initialized")
            return False

        try:
            # Get collection info
            col_info = self.client.get_collection(collection_name)
            vector_size = col_info.config.params.vectors.size
            distance = col_info.config.params.vectors.distance

            # Delete and recreate collection
            self.client.delete_collection(collection_name)
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance)
            )

            print(f"✓ Collection '{collection_name}' cleared\n")
            return True
        except Exception as e:
            print(f"✗ Error clearing collection: {e}")
            return False


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Qdrant Debug Agent for MemOS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test connection
  python qdrant_utils.py --test

  # List all collections
  python qdrant_utils.py --list

  # Show database statistics
  python qdrant_utils.py --stats

  # Get collection info
  python qdrant_utils.py --info my_collection

  # Inspect collection
  python qdrant_utils.py --inspect my_collection

  # Verify MemOS data
  python qdrant_utils.py --verify

  # Delete collection (DANGEROUS!)
  python qdrant_utils.py --delete my_collection --confirm

  # Delete all collections (VERY DANGEROUS!)
  python qdrant_utils.py --delete-all --confirm
        """
    )

    # Connection options
    parser.add_argument("--host", default=os.getenv("QDRANT_HOST", "localhost"),
                       help="Qdrant host (default: localhost)")
    parser.add_argument("--port", type=int, default=int(os.getenv("QDRANT_PORT", "6334")),
                       help="Qdrant port (default: 6334)")
    parser.add_argument("--api-key", default=os.getenv("QDRANT_API_KEY"),
                       help="Qdrant API key")

    # Actions
    parser.add_argument("--test", action="store_true",
                       help="Test connection and show server info")
    parser.add_argument("--list", action="store_true",
                       help="List all collections")
    parser.add_argument("--stats", action="store_true",
                       help="Show database statistics")
    parser.add_argument("--info", type=str, metavar="COLLECTION",
                       help="Get collection info")
    parser.add_argument("--inspect", type=str, metavar="COLLECTION",
                       help="Inspect collection data")
    parser.add_argument("--verify", action="store_true",
                       help="Verify MemOS data was loaded")
    parser.add_argument("--delete", type=str, metavar="COLLECTION",
                       help="Delete collection (requires --confirm)")
    parser.add_argument("--delete-all", action="store_true",
                       help="Delete all collections (requires --confirm)")
    parser.add_argument("--clear", type=str, metavar="COLLECTION",
                       help="Clear collection (requires --confirm)")
    parser.add_argument("--confirm", action="store_true",
                       help="Confirm destructive operations")

    args = parser.parse_args()

    # Create agent
    agent = QdrantDebugAgent(
        host=args.host,
        port=args.port,
        api_key=args.api_key
    )

    # Connect
    if not agent.connect():
        sys.exit(1)

    try:
        # Execute requested action
        if args.test:
            agent.test_connection()
        elif args.list:
            agent.list_collections()
        elif args.stats:
            agent.get_all_stats()
        elif args.info:
            agent.get_collection_info(args.info)
        elif args.inspect:
            agent.inspect_collection(args.inspect)
        elif args.verify:
            agent.verify_memos_data()
        elif args.delete:
            agent.delete_collection(args.delete, confirm=args.confirm)
        elif args.delete_all:
            agent.delete_all_collections(confirm=args.confirm)
        elif args.clear:
            agent.clear_collection(args.clear, confirm=args.confirm)
        else:
            parser.print_help()
    finally:
        agent.close()


if __name__ == "__main__":
    main()
