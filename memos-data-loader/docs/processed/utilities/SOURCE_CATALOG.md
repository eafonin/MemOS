# Documentation Source Catalog

**Created:** 2025-10-16
**Purpose:** Track all documentation sources for MEMOS data loader project

---

## Local Files (To be transferred from Windows)

### Text Files
1. **memos-example-prompts.md**
   - Size: 8,964 bytes
   - Source: `C:\Users\afoni\Downloads\memOS\docs\memos-example-prompts.md`
   - Type: Markdown
   - Status: ⏳ Pending transfer

2. **memOSbasedDynamicSchema.txt**
   - Size: 10,317 bytes
   - Source: `C:\Users\afoni\Downloads\memOS\docs\memOSbasedDynamicSchema.txt`
   - Type: Text
   - Status: ⏳ Pending transfer

### Image Files
3. **memos-architecture.png**
   - Size: 174,967 bytes
   - Source: `C:\Users\afoni\Downloads\memOS\docs\memos-architecture.png`
   - Type: PNG Image
   - Status: ⏳ Pending transfer

### PDF Files
4. **2505.22101v1.pdf**
   - Source: `C:\Users\afoni\Downloads\memOS\docs\source\2505.22101v1.pdf`
   - Type: Academic paper (arXiv)
   - Title: MemOS Short Paper
   - Status: ⏳ Pending transfer

5. **2507.03724v3_MEMEOS.pdf**
   - Source: `C:\Users\afoni\Downloads\memOS\docs\source\2507.03724v3_MEMEOS.pdf`
   - Type: Academic paper (arXiv)
   - Title: MemOS Long Paper
   - Status: ⏳ Pending transfer

6. **memOSoverview.pdf**
   - Source: `C:\Users\afoni\Downloads\memOS\docs\source\memOSoverview.pdf`
   - Type: Overview document
   - Status: ⏳ Pending transfer

---

## Web Sources

### Official Documentation
1. **MEMOS Introduction**
   - URL: https://memos-docs.openmem.net/overview/introduction
   - Type: Official documentation
   - Status: ⏳ Pending scrape

### Blog Articles
2. **LLM Multi-Agents Blog**
   - URL: https://llmmultiagents.com/en/blogs/memos-revolutionizing-llm-memory-management-as-a-first-class-operating-system
   - Type: Technical blog post
   - Status: ⏳ Pending scrape

---

## Transfer Instructions

### Option 1: Direct File Copy (If using WSL or shared filesystem)
```bash
# From Windows to Linux
cp /mnt/c/Users/afoni/Downloads/memOS/docs/*.{md,txt,png} /home/memos/Development/MemOS/memos-data-loader/docs/scraped/
cp /mnt/c/Users/afoni/Downloads/memOS/docs/source/*.pdf /home/memos/Development/MemOS/memos-data-loader/docs/scraped/
```

### Option 2: Manual Upload
Place all files in:
```
/home/memos/Development/MemOS/memos-data-loader/docs/scraped/
```

---

## Processing Status

- [ ] All local files transferred
- [ ] Web sources scraped
- [ ] Files cataloged and validated
- [ ] Ready for processing phase

---

## Notes
- Total local files: 6 (3 text/image + 3 PDFs)
- Total web sources: 2 URLs
- Combined documentation corpus will provide comprehensive MEMOS understanding
