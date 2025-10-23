# MemOS Patches Index

This directory contains patches and fixes that can be applied to the main MemOS codebase.

---

## Available Patches

### neo4j-complex-object-serialization/

**Status:** ✅ Tested and verified
**Date:** 2025-10-20
**Priority:** 🔴 **CRITICAL** - Blocks all memory storage
**Type:** Bug fix (Critical)

**Summary:**
Fixes Neo4j `CypherTypeError` that prevents storage of memories with complex nested objects (dicts, arrays of dicts). Without this fix, ALL memory operations fail silently.

**Impact:**
- **Enables memory storage** - Critical fix for Neo4j Community Edition
- **Enables chat context** - Memories can now be retrieved
- **Enables full search** - Graph + vector integration works
- **Prevents data loss** - All memory operations now succeed

**Root Cause:**
Neo4j only accepts primitive types or arrays of primitives as node properties. MemOS stores `sources` field as array of message dictionaries, which Neo4j rejects. This patch adds JSON serialization layer.

**Files Modified:** 1 file (neo4j_community.py)
**Lines Changed:** +65, -1

**Quick Apply:**
```bash
cd /home/memos/Development/MemOS
git apply patches/neo4j-complex-object-serialization/*.patch
# Rebuild and restart API container
```

**Documentation:** See `patches/neo4j-complex-object-serialization/README.md`

**Test Verification:**
```bash
bash patches/neo4j-complex-object-serialization/TEST.sh test1-memos-api
```

---

### bge-large-embeddings-512-tokens/

**Status:** ✅ Tested and verified
**Date:** 2025-10-21
**Priority:** 🔴 **CRITICAL** - Fixes silent data loss
**Type:** Bug fix + Enhancement

**Summary:**
Upgrades embedding model from `sentence-transformers/all-mpnet-base-v2` (384-token limit) to `BAAI/bge-large-en-v1.5` (512-token limit), fixing critical silent failures where documents >384 tokens were rejected but API returned 200 OK.

**Impact:**
- **Fixes silent data loss** - Documents >384 tokens now processed successfully
- **+33% token capacity** - 512 vs 384 token limit
- **Better embedding quality** - BGE-Large outperforms all-mpnet-base-v2
- **Improved success rate** - 33% → ~90% document ingestion success
- **Truncation warnings** - Logs now alert if chunks exceed limits

**Root Cause:**
Chunker created 512-token chunks but TEI embedding service only accepts 384 tokens. Documents >384 tokens failed with Error 413 but API incorrectly returned 200 OK, causing silent data loss.

**Files Modified:** 2 files + docker-compose.yml
**Lines Changed:** +21, -3

**Quick Apply:**
```bash
cd /home/memos/Development/MemOS
bash patches/bge-large-embeddings-512-tokens/APPLY.sh
# Then manually update docker-compose.yml (see README)
# Rebuild: docker-compose build --no-cache memos-api
```

**Documentation:** See `patches/bge-large-embeddings-512-tokens/README.md`

**Test Verification:**
```bash
bash patches/bge-large-embeddings-512-tokens/TEST.sh test1-memos-api
```

**Dependencies:** None (standalone patch)

**Note:** Requires docker-compose.yml update to change TEI model. See `docker-compose-bge-large.yml.example` for reference configuration.

---

### chonkie-tokenizer-fix/

**Status:** ✅ Tested and verified
**Date:** 2025-10-20
**Priority:** Medium
**Type:** Bug fix + Enhancement

**Summary:**
Fixes Chonkie text chunker falling back to character-based chunking instead of using proper tokenization from HuggingFace cache.

**Impact:**
- Improves chunking quality (token-based vs character-based)
- Enables offline tokenizer loading from cache
- Fixes "Tokenizer not found" errors

**Files Modified:** 5 files (4 source + 1 dependency)
**Lines Changed:** +33, -6

**Quick Apply:**
```bash
cd /home/memos/Development/MemOS
git apply patches/chonkie-tokenizer-fix/*.patch
```

**Documentation:** See `patches/chonkie-tokenizer-fix/README.md`

---

## How to Use This Directory

### Applying Patches

1. **Review the patch**
   ```bash
   cat patches/<patch-name>/*.patch
   cat patches/<patch-name>/README.md
   ```

2. **Check if patch applies cleanly**
   ```bash
   cd /home/memos/Development/MemOS
   git apply --check patches/<patch-name>/*.patch
   ```

3. **Apply the patch**
   ```bash
   git apply patches/<patch-name>/*.patch
   # Or use the provided APPLY.sh script
   bash patches/<patch-name>/APPLY.sh
   ```

4. **Verify the fix**
   ```bash
   # Use the provided TEST.sh script
   bash patches/<patch-name>/TEST.sh [container-name]
   ```

5. **Commit the changes**
   ```bash
   git add .
   git commit -m "Apply patch: <patch-name>"
   ```

### Creating New Patches

When you fix an issue that should be preserved:

1. **Create patch directory**
   ```bash
   mkdir -p patches/<patch-name>
   ```

2. **Generate git diff**
   ```bash
   git diff > patches/<patch-name>/0001-description.patch
   ```

3. **Create documentation**
   ```bash
   # Create README.md explaining the patch
   # Include: problem, solution, files modified, testing
   ```

4. **Add to INDEX.md**
   ```bash
   # Add entry to this file
   ```

5. **Optional: Add helper scripts**
   ```bash
   # APPLY.sh - automated application
   # TEST.sh - verification testing
   # REVERT.sh - rollback script
   ```

---

## Patch Format

Each patch directory should contain:

- `*.patch` - The actual patch files (numbered if multiple)
- `README.md` - Comprehensive documentation
- `APPLY.sh` - (Optional) Automated application script
- `TEST.sh` - (Optional) Verification testing script
- `REVERT.sh` - (Optional) Rollback script

---

## Patch Metadata Template

When adding a new patch to this index:

```markdown
### <patch-name>/

**Status:** [✅ Tested | ⚠️ Needs Testing | ❌ Deprecated]
**Date:** YYYY-MM-DD
**Priority:** [High | Medium | Low]
**Type:** [Bug fix | Enhancement | Security | Performance]

**Summary:**
Brief description of what the patch does.

**Impact:**
- List of improvements
- Changes in behavior
- Performance impact

**Files Modified:** X files
**Lines Changed:** +additions, -deletions

**Quick Apply:**
\`\`\`bash
# Command to apply
\`\`\`

**Documentation:** Link to detailed README
```

---

## Maintenance

### Periodic Review

Patches should be reviewed periodically:

- ✅ **Active:** Apply to main branch when stable
- ⚠️ **Outdated:** Update if codebase has changed
- ❌ **Obsolete:** Remove if no longer needed

### Integration with Main

When a patch is merged to main:

1. Mark as integrated in this INDEX
2. Move patch to `patches/integrated/` directory
3. Keep for historical reference

---

## Contributing

If you create a patch that fixes an issue:

1. Follow the patch format above
2. Test thoroughly in isolated environment (like docker-test1)
3. Document the problem, solution, and testing
4. Add entry to this INDEX.md
5. Consider submitting as PR to main branch

---

**Last Updated:** 2025-10-21
**Maintainer:** Development Team
