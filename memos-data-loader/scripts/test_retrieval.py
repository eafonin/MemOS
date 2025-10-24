#!/usr/bin/env python3
"""
Test retrieval quality and semantic relevance metrics.
Generates queries from loaded documents and measures retrieval performance.
"""

import json
import sys
import time
import requests
import random
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict

# Configuration
API_BASE = "http://localhost:8001"
DOCS_DIR = Path("/home/memos/Development/MemOS/docs/processed")

class RetrievalTester:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.metrics = {
            "queries_tested": 0,
            "avg_similarity": 0.0,
            "min_similarity": 1.0,
            "max_similarity": 0.0,
            "avg_results": 0,
            "avg_latency_ms": 0,
            "similarity_distribution": defaultdict(int),
            "queries": []
        }

    def generate_queries_from_docs(self, max_queries: int = 10) -> List[Dict[str, Any]]:
        """Generate test queries by extracting key phrases from documents."""
        print("🔍 Generating test queries from loaded documents...")

        queries = []
        all_files = list(DOCS_DIR.rglob("*.md"))

        # Sample files for query generation
        sample_files = random.sample(all_files, min(max_queries, len(all_files)))

        for file_path in sample_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Extract lines that look like headings or important concepts
                lines = content.split('\n')
                candidates = []

                for line in lines:
                    line = line.strip()
                    # Look for headings, or lines with keywords
                    if (line.startswith('#') or
                        'architecture' in line.lower() or
                        'design' in line.lower() or
                        'implementation' in line.lower() or
                        'memory' in line.lower()):
                        # Clean up markdown formatting
                        query = line.lstrip('#').strip()
                        if 10 < len(query) < 100 and not query.startswith('['):
                            candidates.append(query)

                if candidates:
                    # Pick a random candidate from this file
                    query_text = random.choice(candidates)
                    queries.append({
                        "query": query_text,
                        "source_file": str(file_path.relative_to(DOCS_DIR)),
                        "type": "concept"
                    })

            except Exception as e:
                print(f"  ⚠️  Error reading {file_path.name}: {e}")
                continue

        # Add some general queries
        general_queries = [
            {"query": "MemOS architecture and design", "type": "general"},
            {"query": "memory management in language models", "type": "general"},
            {"query": "chunking strategy for documents", "type": "general"},
            {"query": "embedding models comparison", "type": "general"},
            {"query": "Neo4j graph database integration", "type": "general"},
        ]

        queries.extend(general_queries[:max_queries - len(queries)])

        print(f"  Generated {len(queries)} test queries")
        return queries

    def test_search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Test search endpoint and measure metrics."""
        try:
            start = time.time()
            response = requests.post(
                f"{API_BASE}/product/search",
                json={
                    "user_id": self.user_id,
                    "query": query,
                    "top_k": top_k
                },
                timeout=30
            )
            latency = (time.time() - start) * 1000  # Convert to ms

            if response.status_code == 200:
                result = response.json()

                # Extract similarity scores
                similarities = []
                results_count = 0

                if "data" in result and "text_mem" in result["data"]:
                    for cube in result["data"]["text_mem"]:
                        if "memories" in cube:
                            results_count += len(cube["memories"])
                            for mem in cube["memories"]:
                                if "metadata" in mem and "relativity" in mem["metadata"]:
                                    similarities.append(mem["metadata"]["relativity"])

                return {
                    "success": True,
                    "latency_ms": latency,
                    "results_count": results_count,
                    "similarities": similarities,
                    "avg_similarity": sum(similarities) / len(similarities) if similarities else 0,
                    "min_similarity": min(similarities) if similarities else 0,
                    "max_similarity": max(similarities) if similarities else 0,
                    "response": result
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text[:200]}",
                    "latency_ms": latency
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "latency_ms": 0
            }

    def run_retrieval_tests(self, queries: List[Dict[str, Any]]):
        """Run retrieval tests on generated queries."""
        print()
        print("=" * 70)
        print("  Retrieval Quality Testing")
        print("=" * 70)
        print()

        for idx, query_info in enumerate(queries, 1):
            query = query_info["query"]
            print(f"\n[{idx}/{len(queries)}] Testing query:")
            print(f"  Query: \"{query[:80]}...\"" if len(query) > 80 else f"  Query: \"{query}\"")
            print(f"  Type: {query_info.get('type', 'unknown')}")

            result = self.test_search(query)

            if result["success"]:
                self.metrics["queries_tested"] += 1

                # Update metrics
                if result.get("similarities"):
                    avg_sim = result["avg_similarity"]
                    self.metrics["avg_similarity"] += avg_sim
                    self.metrics["min_similarity"] = min(self.metrics["min_similarity"], result["min_similarity"])
                    self.metrics["max_similarity"] = max(self.metrics["max_similarity"], result["max_similarity"])

                    # Distribution
                    bucket = int(avg_sim * 10) / 10  # Round to 1 decimal
                    self.metrics["similarity_distribution"][bucket] += 1

                    print(f"  ✅ Found {result['results_count']} results")
                    print(f"     Similarity: avg={avg_sim:.3f}, min={result['min_similarity']:.3f}, max={result['max_similarity']:.3f}")
                    print(f"     Latency: {result['latency_ms']:.1f}ms")
                else:
                    print(f"  ⚠️  No results found")

                self.metrics["avg_results"] += result.get("results_count", 0)
                self.metrics["avg_latency_ms"] += result.get("latency_ms", 0)
            else:
                print(f"  ❌ Search failed: {result.get('error', 'Unknown error')}")

            # Store query result
            self.metrics["queries"].append({
                "query": query,
                "type": query_info.get("type"),
                "source": query_info.get("source_file"),
                "result": result
            })

        # Calculate averages
        if self.metrics["queries_tested"] > 0:
            self.metrics["avg_similarity"] /= self.metrics["queries_tested"]
            self.metrics["avg_results"] /= self.metrics["queries_tested"]
            self.metrics["avg_latency_ms"] /= self.metrics["queries_tested"]

        self.print_summary()

    def print_summary(self):
        """Print retrieval testing summary."""
        print()
        print("=" * 70)
        print("  Retrieval Quality Summary")
        print("=" * 70)
        print(f"Queries tested: {self.metrics['queries_tested']}")
        print(f"Average results per query: {self.metrics['avg_results']:.1f}")
        print(f"Average latency: {self.metrics['avg_latency_ms']:.1f}ms")
        print()
        print("Semantic Similarity Metrics:")
        print(f"  Average: {self.metrics['avg_similarity']:.3f}")
        print(f"  Min: {self.metrics['min_similarity']:.3f}")
        print(f"  Max: {self.metrics['max_similarity']:.3f}")
        print()
        print("Similarity Distribution:")
        for bucket in sorted(self.metrics["similarity_distribution"].keys()):
            count = self.metrics["similarity_distribution"][bucket]
            bar = "█" * int(count * 20 / max(self.metrics["similarity_distribution"].values()))
            print(f"  {bucket:.1f}-{bucket+0.1:.1f}: {count:3d} {bar}")
        print()

    def save_report(self, report_path: str):
        """Save detailed metrics report."""
        with open(report_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"📄 Metrics report saved to: {report_path}")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python test_retrieval.py <user_id> [num_queries]")
        print("Example: python test_retrieval.py test_user_123 10")
        sys.exit(1)

    user_id = sys.argv[1]
    num_queries = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    # Create tester
    tester = RetrievalTester(user_id)

    # Generate queries
    queries = tester.generate_queries_from_docs(num_queries)

    if not queries:
        print("❌ No queries generated!")
        return 1

    # Run tests
    tester.run_retrieval_tests(queries)

    # Save report
    report_path = f"/tmp/memos_retrieval_metrics_{user_id}_{int(time.time())}.json"
    tester.save_report(report_path)

    return 0

if __name__ == "__main__":
    sys.exit(main())
