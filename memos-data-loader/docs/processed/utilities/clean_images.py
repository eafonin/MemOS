#!/usr/bin/env python3
"""
Clean up images in the memos-docs.openmem.net folder:
- Remove image files that are not referenced in any MD file
- Remove image links from MD files that point to non-existent images
"""

import re
from pathlib import Path
from typing import Set, Dict, List


def find_image_references(md_file: Path) -> Set[str]:
    """Find all image references in a markdown file."""
    references = set()

    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match markdown image syntax: ![alt](path)
        # Match various formats: ./IMAGES/file.ext, IMAGES/file.ext, /path/IMAGES/file.ext
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        matches = re.findall(pattern, content)

        for alt_text, img_path in matches:
            # Extract just the filename if it's in IMAGES folder
            if 'IMAGES' in img_path:
                # Get the part after IMAGES/
                parts = img_path.split('IMAGES/')
                if len(parts) > 1:
                    filename = parts[-1].split('?')[0].strip()  # Remove query params
                    references.add(filename)

    except Exception as e:
        print(f"  Warning: Could not read {md_file}: {e}")

    return references


def remove_broken_image_links(md_file: Path, existing_images: Set[str]) -> int:
    """Remove image links that point to non-existent files. Returns number of links removed."""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        removed_count = 0

        # Pattern to match image links
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

        def replace_broken_link(match):
            nonlocal removed_count
            alt_text = match.group(1)
            img_path = match.group(2)

            # Check if this is an IMAGES reference
            if 'IMAGES' in img_path:
                parts = img_path.split('IMAGES/')
                if len(parts) > 1:
                    filename = parts[-1].split('?')[0].strip()
                    if filename not in existing_images:
                        removed_count += 1
                        return ''  # Remove the broken link

            return match.group(0)  # Keep the link

        content = re.sub(pattern, replace_broken_link, content)

        # Clean up extra blank lines that might be left
        content = re.sub(r'\n{3,}', '\n\n', content)

        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)

        return removed_count

    except Exception as e:
        print(f"  Warning: Could not process {md_file}: {e}")
        return 0


def main():
    base_dir = Path('/home/memos/Development/MemOS/memos-data-loader/docs/processed/memos-docs.openmem.net')
    images_dir = base_dir / 'IMAGES'

    if not images_dir.exists():
        print(f"Error: IMAGES directory not found at {images_dir}")
        return

    print("="*70)
    print("CLEANING IMAGES IN memos-docs.openmem.net")
    print("="*70)

    # Step 1: Find all MD files
    print("\n1. Scanning markdown files...")
    md_files = list(base_dir.glob('*.md'))
    print(f"   Found {len(md_files)} markdown files")

    # Step 2: Collect all image references from MD files
    print("\n2. Collecting image references from markdown files...")
    all_references = set()
    for md_file in md_files:
        refs = find_image_references(md_file)
        all_references.update(refs)

    print(f"   Found {len(all_references)} unique image references")

    # Step 3: Find all actual image files
    print("\n3. Finding image files in IMAGES directory...")
    image_files = set()
    for img_file in images_dir.iterdir():
        if img_file.is_file() and not img_file.name.startswith('.'):
            image_files.add(img_file.name)

    print(f"   Found {len(image_files)} image files")

    # Step 4: Find orphaned images (not referenced)
    print("\n4. Finding orphaned images (not referenced in any MD)...")
    orphaned_images = image_files - all_references

    if orphaned_images:
        print(f"   Found {len(orphaned_images)} orphaned images:")
        for img in sorted(orphaned_images):
            print(f"     - {img}")

        # Remove orphaned images
        print("\n5. Removing orphaned images...")
        removed_count = 0
        for img in orphaned_images:
            img_path = images_dir / img
            try:
                img_path.unlink()
                removed_count += 1
                print(f"     ✓ Removed: {img}")
            except Exception as e:
                print(f"     ✗ Error removing {img}: {e}")

        print(f"   Removed {removed_count}/{len(orphaned_images)} orphaned images")
    else:
        print("   No orphaned images found")

    # Step 6: Find broken links (references to non-existent images)
    print("\n6. Finding broken image links (pointing to non-existent files)...")
    broken_references = all_references - image_files

    if broken_references:
        print(f"   Found {len(broken_references)} broken references:")
        for ref in sorted(broken_references):
            print(f"     - {ref}")

        # Remove broken links from MD files
        print("\n7. Removing broken image links from markdown files...")
        total_removed = 0
        for md_file in md_files:
            removed = remove_broken_image_links(md_file, image_files)
            if removed > 0:
                total_removed += removed
                print(f"     ✓ {md_file.name}: removed {removed} broken link(s)")

        print(f"   Removed {total_removed} broken link(s) from markdown files")
    else:
        print("   No broken image links found")

    # Final summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Markdown files: {len(md_files)}")
    print(f"Image references found: {len(all_references)}")
    print(f"Image files before: {len(image_files)}")
    print(f"Orphaned images removed: {len(orphaned_images)}")
    print(f"Broken links removed: {len(broken_references)}")
    print(f"Image files after: {len(image_files - orphaned_images)}")
    print("="*70)


if __name__ == '__main__':
    main()
