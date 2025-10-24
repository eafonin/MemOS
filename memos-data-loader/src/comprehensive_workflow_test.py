#!/usr/bin/env python3
"""
Comprehensive MemOS Workflow Testing Script

This script tests all MemOS memory types and internal workflows by:
1. Loading documents one at a time
2. Capturing detailed logs at each workflow step
3. Analyzing database state changes
4. Generating a comprehensive report

Test Documents:
- Document 1: github-memos-docs/open_source-contribution-writing_tests.md
- Document 2: arxiv-2507.03724v3/arxiv-2507.03724v3_references.md
- Document 3: alidocs-dingtalc-com/help.md
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from neo4j import GraphDatabase
from qdrant_client import QdrantClient

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8001")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7688")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "memospassword123")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6334"))

# Test documents
TEST_DOCS = [
    {
        "id": "doc1",
        "name": "PyTest Testing Guide",
        "path": "/home/memos/Development/MemOS/memos-data-loader/docs/processed/github-memos-docs/open_source-contribution-writing_tests.md",
        "type": "technical_documentation",
    },
    {
        "id": "doc2",
        "name": "MemOS Paper References",
        "path": "/home/memos/Development/MemOS/memos-data-loader/docs/processed/arxiv-2507.03724v3/arxiv-2507.03724v3_references.md",
        "type": "academic_references",
    },
    {
        "id": "doc3",
        "name": "MemOS Help Q&A",
        "path": "/home/memos/Development/MemOS/memos-data-loader/docs/processed/alidocs-dingtalc-com/help.md",
        "type": "faq_documentation",
    },
]


class WorkflowTester:
    """Comprehensive workflow tester for MemOS"""

    def __init__(self):
        self.neo4j_driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
        self.qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        self.test_results = []

        # Generate unique IDs using timestamp to avoid conflicts
        timestamp = int(time.time())
        self.user_id = f"workflow_test_user_{timestamp}"
        self.cube_id = f"test_cube_{timestamp}"

        self.report_data = {
            "test_start_time": datetime.now().isoformat(),
            "test_user_id": self.user_id,
            "test_cube_id": self.cube_id,
            "documents_tested": [],
            "workflows_analyzed": [],
            "database_states": [],
        }

    def __del__(self):
        """Cleanup connections"""
        if hasattr(self, "neo4j_driver"):
            self.neo4j_driver.close()

    def get_neo4j_state(self) -> dict:
        """Get current Neo4j database state"""
        with self.neo4j_driver.session() as session:
            # Count nodes by label
            node_counts = session.run(
                """
                MATCH (n)
                RETURN labels(n) as labels, count(*) as count
                """
            ).data()

            # Count relationships by type
            rel_counts = session.run(
                """
                MATCH ()-[r]->()
                RETURN type(r) as type, count(*) as count
                """
            ).data()

            # Get sample nodes
            sample_nodes = session.run(
                """
                MATCH (n)
                RETURN labels(n) as labels, properties(n) as props
                LIMIT 10
                """
            ).data()

            return {
                "node_counts": node_counts,
                "relationship_counts": rel_counts,
                "sample_nodes": sample_nodes,
                "total_nodes": sum(item["count"] for item in node_counts),
                "total_relationships": sum(item["count"] for item in rel_counts),
            }

    def get_qdrant_state(self) -> dict:
        """Get current Qdrant database state"""
        collections = self.qdrant_client.get_collections().collections

        collection_info = []
        for collection in collections:
            info = self.qdrant_client.get_collection(collection.name)
            collection_info.append(
                {
                    "name": collection.name,
                    "vectors_count": info.vectors_count,
                    "points_count": info.points_count,
                    "config": {
                        "distance": info.config.params.vectors.distance.name
                        if hasattr(info.config.params.vectors, "distance")
                        else "N/A",
                    },
                }
            )

        return {
            "collections": collection_info,
            "total_collections": len(collections),
            "total_vectors": sum(c["vectors_count"] for c in collection_info),
        }

    def register_user(self, user_id: str, cube_id: str) -> dict:
        """Register a new user with cube (combined operation)"""
        print(f"\n[USER & CUBE REGISTRATION] Registering user: {user_id} with cube: {cube_id}")

        try:
            response = requests.post(
                f"{API_URL}/product/users/register",
                json={
                    "user_id": user_id,
                    "mem_cube_id": cube_id,
                    "user_name": f"Test User {user_id}"
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                print(f"  Success: {result}")
                return {"success": True, "result": result}
            else:
                print(f"  Error: {response.text}")
                return {"success": False, "error": response.text}

        except Exception as e:
            print(f"  Exception: {e}")
            return {"success": False, "error": str(e)}

    def load_document(self, doc: dict) -> dict:
        """Load a document via MemOS API and capture response"""
        print(f"\n{'='*80}")
        print(f"LOADING DOCUMENT: {doc['name']}")
        print(f"{'='*80}\n")

        # Read document content
        with open(doc["path"], "r", encoding="utf-8") as f:
            content = f.read()

        print(f"Document size: {len(content)} characters")
        print(f"Document type: {doc['type']}")

        # Capture state before
        print("\n[BEFORE] Capturing database state...")
        state_before = {
            "neo4j": self.get_neo4j_state(),
            "qdrant": self.get_qdrant_state(),
            "timestamp": datetime.now().isoformat(),
        }

        print(f"  Neo4j: {state_before['neo4j']['total_nodes']} nodes")
        print(
            f"  Qdrant: {state_before['qdrant']['total_vectors']} vectors in {state_before['qdrant']['total_collections']} collections"
        )

        # Load document via API
        print("\n[API CALL] Sending document to MemOS API...")
        start_time = time.time()

        try:
            response = requests.post(
                f"{API_URL}/product/add",
                json={
                    "user_id": self.user_id,
                    "memory_content": content,
                    "source": f"{doc['type']}:{doc['name']}",
                },
                timeout=120,
            )

            elapsed_time = time.time() - start_time
            print(f"  Response time: {elapsed_time:.2f}s")
            print(f"  HTTP Status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"  Response: {json.dumps(result, indent=2)}")
            else:
                print(f"  Error: {response.text}")
                result = {"error": response.text}

        except Exception as e:
            print(f"  Exception: {e}")
            result = {"error": str(e)}
            elapsed_time = time.time() - start_time

        # Wait for processing to complete
        print("\n[WAIT] Waiting 5 seconds for processing to complete...")
        time.sleep(5)

        # Capture state after
        print("\n[AFTER] Capturing database state...")
        state_after = {
            "neo4j": self.get_neo4j_state(),
            "qdrant": self.get_qdrant_state(),
            "timestamp": datetime.now().isoformat(),
        }

        print(f"  Neo4j: {state_after['neo4j']['total_nodes']} nodes")
        print(
            f"  Qdrant: {state_after['qdrant']['total_vectors']} vectors in {state_after['qdrant']['total_collections']} collections"
        )

        # Calculate changes
        changes = {
            "neo4j_nodes_added": state_after["neo4j"]["total_nodes"]
            - state_before["neo4j"]["total_nodes"],
            "neo4j_rels_added": state_after["neo4j"]["total_relationships"]
            - state_before["neo4j"]["total_relationships"],
            "qdrant_vectors_added": state_after["qdrant"]["total_vectors"]
            - state_before["qdrant"]["total_vectors"],
        }

        print("\n[CHANGES]")
        print(f"  Neo4j nodes added: {changes['neo4j_nodes_added']}")
        print(f"  Neo4j relationships added: {changes['neo4j_rels_added']}")
        print(f"  Qdrant vectors added: {changes['qdrant_vectors_added']}")

        return {
            "document": doc,
            "api_response": result,
            "elapsed_time": elapsed_time,
            "state_before": state_before,
            "state_after": state_after,
            "changes": changes,
        }

    def test_search(self, query: str, description: str) -> dict:
        """Test search functionality"""
        print(f"\n[SEARCH TEST] {description}")
        print(f"  Query: {query}")

        try:
            response = requests.post(
                f"{API_URL}/product/search",
                json={"user_id": self.user_id, "query": query, "top_k": 5},
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                # Parse MemOS API response format: data.text_mem[].memories[]
                data = result.get('data', {})
                text_mem = data.get('text_mem', [])
                total_results = sum(len(cube.get('memories', [])) for cube in text_mem)
                print(f"  Results: {total_results} items found")
                return {"success": True, "results": result, "query": query, "count": total_results}
            else:
                print(f"  Error: {response.text}")
                return {"success": False, "error": response.text}

        except Exception as e:
            print(f"  Exception: {e}")
            return {"success": False, "error": str(e)}

    def run_comprehensive_test(self):
        """Run comprehensive workflow test"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE MEMOS WORKFLOW TEST")
        print("=" * 80)
        print(f"Start time: {self.report_data['test_start_time']}")
        print(f"API URL: {API_URL}")
        print(f"Neo4j URI: {NEO4J_URI}")
        print(f"Qdrant: {QDRANT_HOST}:{QDRANT_PORT}")
        print("=" * 80)

        # Step 1: Register user with cube
        print(f"\n{'='*80}")
        print("STEP 1: USER & CUBE REGISTRATION WORKFLOW")
        print(f"{'='*80}")
        user_reg_result = self.register_user(self.user_id, self.cube_id)
        self.report_data["user_registration"] = user_reg_result

        if not user_reg_result.get("success", False):
            print("\n⚠️  WARNING: User registration failed. Continuing anyway...")

        # Step 2: Test each document
        print(f"\n{'='*80}")
        print("STEP 2: DOCUMENT INGESTION WORKFLOWS")
        print(f"{'='*80}")

        for doc in TEST_DOCS:
            result = self.load_document(doc)
            self.report_data["documents_tested"].append(result)
            self.test_results.append(result)

        # Test search after all documents loaded
        print(f"\n{'='*80}")
        print("TESTING SEARCH WORKFLOWS")
        print(f"{'='*80}\n")

        search_tests = [
            ("pytest", "Search for pytest testing content"),
            ("MemOS memory", "Search for MemOS memory types"),
            ("references", "Search for academic references"),
        ]

        search_results = []
        for query, desc in search_tests:
            result = self.test_search(query, desc)
            search_results.append(result)

        self.report_data["search_results"] = search_results

        # Final database state
        print(f"\n{'='*80}")
        print("FINAL DATABASE STATE")
        print(f"{'='*80}\n")

        final_state = {
            "neo4j": self.get_neo4j_state(),
            "qdrant": self.get_qdrant_state(),
        }

        self.report_data["final_state"] = final_state
        self.report_data["test_end_time"] = datetime.now().isoformat()

        print(f"Neo4j:")
        print(f"  Total nodes: {final_state['neo4j']['total_nodes']}")
        print(
            f"  Total relationships: {final_state['neo4j']['total_relationships']}"
        )
        print(f"  Node types: {json.dumps(final_state['neo4j']['node_counts'], indent=4)}")

        print(f"\nQdrant:")
        print(f"  Total collections: {final_state['qdrant']['total_collections']}")
        print(f"  Total vectors: {final_state['qdrant']['total_vectors']}")
        print(
            f"  Collections: {json.dumps(final_state['qdrant']['collections'], indent=4)}"
        )

        return self.report_data

    def generate_report(self, output_file: str):
        """Generate comprehensive test report"""
        print(f"\n{'='*80}")
        print("GENERATING REPORT")
        print(f"{'='*80}\n")

        with open(output_file, "w") as f:
            json.dump(self.report_data, f, indent=2, default=str)

        print(f"Report saved to: {output_file}")

        # Also generate summary
        summary_file = output_file.replace(".json", "_summary.txt")
        with open(summary_file, "w") as f:
            f.write("MEMOS COMPREHENSIVE WORKFLOW TEST SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Test Period: {self.report_data['test_start_time']} to {self.report_data['test_end_time']}\n\n")

            f.write("DOCUMENTS TESTED:\n")
            for doc_result in self.report_data["documents_tested"]:
                doc = doc_result["document"]
                changes = doc_result["changes"]
                f.write(f"\n  {doc['name']} ({doc['type']})\n")
                f.write(f"    Processing time: {doc_result['elapsed_time']:.2f}s\n")
                f.write(f"    Neo4j nodes added: {changes['neo4j_nodes_added']}\n")
                f.write(f"    Neo4j rels added: {changes['neo4j_rels_added']}\n")
                f.write(f"    Qdrant vectors added: {changes['qdrant_vectors_added']}\n")

            final = self.report_data["final_state"]
            f.write(f"\n\nFINAL STATE:\n")
            f.write(f"  Neo4j: {final['neo4j']['total_nodes']} nodes, {final['neo4j']['total_relationships']} relationships\n")
            f.write(f"  Qdrant: {final['qdrant']['total_vectors']} vectors in {final['qdrant']['total_collections']} collections\n")

        print(f"Summary saved to: {summary_file}")


def main():
    """Main entry point"""
    tester = WorkflowTester()

    try:
        # Run comprehensive test
        report_data = tester.run_comprehensive_test()

        # Generate reports
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"/tmp/memos_workflow_test_{timestamp}.json"
        tester.generate_report(output_file)

        print(f"\n{'='*80}")
        print("TEST COMPLETED SUCCESSFULLY")
        print(f"{'='*80}\n")

        return 0

    except Exception as e:
        print(f"\n{'='*80}")
        print(f"TEST FAILED: {e}")
        print(f"{'='*80}\n")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
