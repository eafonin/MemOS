#!/usr/bin/env python3
"""
Monitor for patch-specific issues during document loading.
Checks for:
- Chunker configuration consistency (centralized-chunker-config patch)
- BGE-Large truncation issues (bge-large-embeddings patch)
- 413 errors (TEI token limit issues)
- Chunk sizes staying under 512 tokens
"""

import subprocess
import sys
from datetime import datetime

class PatchMonitor:
    def __init__(self, container_name: str = "test1-memos-api"):
        self.container_name = container_name
        self.issues_found = []

    def check_chunker_config(self) -> dict:
        """Verify chunker config is using centralized helper."""
        print("🔍 Checking chunker configuration...")

        try:
            # Test that get_chunker_config() is being used
            result = subprocess.run(
                [
                    "docker", "exec", self.container_name,
                    "python3", "-c",
                    """
import sys
sys.path.insert(0, '/app/src')
from memos.api.config import APIConfig

config = APIConfig.get_chunker_config()
print(f"Backend: {config['backend']}")
print(f"Tokenizer: {config['config']['tokenizer_or_token_counter']}")
print(f"Chunk size: {config['config']['chunk_size']}")
print(f"Chunk overlap: {config['config']['chunk_overlap']}")
                    """
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                print(f"  ✅ Chunker config loaded:")
                for line in output.split('\n'):
                    print(f"     {line}")

                # Verify expected values
                if "bert-base-uncased" in output and "480" in output:
                    print("  ✅ Using expected values (bert-base-uncased, 480 tokens)")
                    return {"status": "ok", "output": output}
                else:
                    issue = "⚠️  Unexpected chunker config values"
                    print(f"  {issue}")
                    self.issues_found.append(issue)
                    return {"status": "warning", "output": output}
            else:
                issue = f"❌ Failed to load chunker config: {result.stderr}"
                print(f"  {issue}")
                self.issues_found.append(issue)
                return {"status": "error", "error": result.stderr}

        except Exception as e:
            issue = f"❌ Error checking chunker config: {e}"
            print(f"  {issue}")
            self.issues_found.append(issue)
            return {"status": "error", "error": str(e)}

    def check_tei_truncation(self) -> dict:
        """Check for TEI truncation warnings in logs."""
        print("\n🔍 Checking for TEI truncation warnings...")

        try:
            result = subprocess.run(
                ["docker", "logs", "--tail=500", self.container_name],
                capture_output=True,
                text=True,
                timeout=10
            )

            logs = result.stdout + result.stderr

            # Look for truncation warnings
            truncation_count = logs.count("TRUNCATION RISK")
            error_413_count = logs.count("413")
            error_413_count += logs.count("Error code: 413")

            print(f"  Truncation warnings: {truncation_count}")
            print(f"  413 errors: {error_413_count}")

            if truncation_count == 0 and error_413_count == 0:
                print("  ✅ No truncation issues found")
                return {"status": "ok", "truncations": 0, "errors_413": 0}
            elif truncation_count > 0 and truncation_count < 10:
                issue = f"⚠️  Found {truncation_count} truncation warnings (acceptable)"
                print(f"  {issue}")
                return {"status": "warning", "truncations": truncation_count, "errors_413": error_413_count}
            else:
                issue = f"❌ Found {truncation_count} truncation warnings, {error_413_count} 413 errors"
                print(f"  {issue}")
                self.issues_found.append(issue)
                return {"status": "error", "truncations": truncation_count, "errors_413": error_413_count}

        except Exception as e:
            issue = f"❌ Error checking logs: {e}"
            print(f"  {issue}")
            self.issues_found.append(issue)
            return {"status": "error", "error": str(e)}

    def check_bge_large_embeddings(self) -> dict:
        """Verify BGE-Large is being used via TEI."""
        print("\n🔍 Checking BGE-Large embeddings...")

        try:
            # Check TEI info endpoint
            result = subprocess.run(
                ["curl", "-s", "http://localhost:8081/info"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                import json
                info = json.loads(result.stdout)

                model_id = info.get("model_id", "unknown")
                max_tokens = info.get("max_input_length", 0)

                print(f"  Model: {model_id}")
                print(f"  Max tokens: {max_tokens}")

                if "bge-large" in model_id and max_tokens == 512:
                    print("  ✅ BGE-Large configured correctly (512 token limit)")
                    return {"status": "ok", "model": model_id, "max_tokens": max_tokens}
                else:
                    issue = f"⚠️  Unexpected model configuration: {model_id}, {max_tokens} tokens"
                    print(f"  {issue}")
                    self.issues_found.append(issue)
                    return {"status": "warning", "model": model_id, "max_tokens": max_tokens}
            else:
                issue = "❌ Failed to query TEI info endpoint"
                print(f"  {issue}")
                self.issues_found.append(issue)
                return {"status": "error", "error": "TEI not responding"}

        except Exception as e:
            issue = f"❌ Error checking BGE-Large: {e}"
            print(f"  {issue}")
            self.issues_found.append(issue)
            return {"status": "error", "error": str(e)}

    def check_container_health(self) -> dict:
        """Check if containers are healthy."""
        print("\n🔍 Checking container health...")

        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=test1", "--format", "{{.Names}}\t{{.Status}}"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                containers = result.stdout.strip().split('\n')
                print(f"  Found {len(containers)} test1 containers:")

                all_healthy = True
                for container in containers:
                    if '\t' in container:
                        name, status = container.split('\t')
                        is_healthy = "healthy" in status.lower() or "up" in status.lower()
                        symbol = "✅" if is_healthy else "❌"
                        print(f"    {symbol} {name}: {status}")
                        all_healthy = all_healthy and is_healthy

                if all_healthy:
                    return {"status": "ok", "containers": len(containers)}
                else:
                    issue = "⚠️  Some containers are not healthy"
                    self.issues_found.append(issue)
                    return {"status": "warning", "containers": len(containers)}
            else:
                issue = "❌ Failed to check container status"
                print(f"  {issue}")
                self.issues_found.append(issue)
                return {"status": "error", "error": "docker ps failed"}

        except Exception as e:
            issue = f"❌ Error checking containers: {e}"
            print(f"  {issue}")
            self.issues_found.append(issue)
            return {"status": "error", "error": str(e)}

    def run_all_checks(self):
        """Run all patch-specific monitoring checks."""
        print("=" * 70)
        print("  Patch-Specific Monitoring")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()

        results = {}
        results["container_health"] = self.check_container_health()
        results["chunker_config"] = self.check_chunker_config()
        results["bge_large"] = self.check_bge_large_embeddings()
        results["truncation"] = self.check_tei_truncation()

        self.print_summary(results)
        return results

    def print_summary(self, results: dict):
        """Print monitoring summary."""
        print()
        print("=" * 70)
        print("  Monitoring Summary")
        print("=" * 70)

        all_ok = True
        for check_name, result in results.items():
            status = result.get("status", "unknown")
            symbol = "✅" if status == "ok" else ("⚠️" if status == "warning" else "❌")
            print(f"{symbol} {check_name.replace('_', ' ').title()}: {status}")
            all_ok = all_ok and (status == "ok")

        print()
        if all_ok:
            print("✅ All patches working correctly!")
        else:
            print(f"⚠️  Found {len(self.issues_found)} issue(s):")
            for issue in self.issues_found:
                print(f"   - {issue}")

        print()

def main():
    """Main function."""
    container_name = sys.argv[1] if len(sys.argv) > 1 else "test1-memos-api"

    monitor = PatchMonitor(container_name)
    results = monitor.run_all_checks()

    # Return exit code based on results
    has_errors = any(r.get("status") == "error" for r in results.values())
    return 1 if has_errors else 0

if __name__ == "__main__":
    sys.exit(main())
