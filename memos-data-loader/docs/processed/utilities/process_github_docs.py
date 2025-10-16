#!/usr/bin/env python3
"""
Process GitHub MemOS-Docs repository:
- Copy English markdown files
- Flatten directory structure (path/to/file.md -> path-to-file.md)
- Download CDN images to local IMAGES
- Update image references to relative paths
"""

import re
import requests
from pathlib import Path
from urllib.parse import urlparse
import time
import shutil


def slugify_path(file_path: Path, base_path: Path) -> str:
    """Convert a file path to a flat filename."""
    # Get relative path from base
    rel_path = file_path.relative_to(base_path)

    # Remove .md extension
    path_str = str(rel_path.with_suffix(''))

    # Replace slashes with hyphens
    flat_name = path_str.replace('/', '-').replace('\\', '-')

    return f"{flat_name}.md"


def download_image(img_url: str, images_dir: Path, counter: int) -> str:
    """Download an image from CDN and return local path."""
    try:
        response = requests.get(img_url, timeout=30)
        response.raise_for_status()

        # Get file extension from URL
        ext = '.png'
        parsed = urlparse(img_url)
        filename = parsed.path.split('/')[-1]
        if '.' in filename:
            ext = '.' + filename.split('.')[-1].split('?')[0]
            if len(ext) > 5:
                ext = '.png'

        # Create filename
        new_filename = f"image_{counter:03d}{ext}"
        filepath = images_dir / new_filename

        # Save image
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"    Downloaded: {new_filename}")
        return f"./IMAGES/{new_filename}"

    except Exception as e:
        print(f"    Warning: Failed to download {img_url}: {e}")
        return img_url  # Return original URL as fallback


def process_markdown_file(input_file: Path, output_dir: Path, images_dir: Path) -> bool:
    """Process a single markdown file."""
    try:
        # Read content
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all image references
        # Match both markdown ![](url) and HTML <img src="url">
        img_counter = 1

        # Process markdown images
        def replace_md_image(match):
            nonlocal img_counter
            alt_text = match.group(1)
            img_url = match.group(2)

            # Only download CDN images
            if img_url.startswith('http') and 'memtensor.com' in img_url:
                local_path = download_image(img_url, images_dir, img_counter)
                img_counter += 1
                return f"![{alt_text}]({local_path})"

            return match.group(0)

        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_md_image, content)

        # Process HTML img tags
        def replace_html_image(match):
            nonlocal img_counter
            full_tag = match.group(0)
            src = match.group(1)

            # Only download CDN images
            if src.startswith('http') and 'memtensor.com' in src:
                local_path = download_image(src, images_dir, img_counter)
                img_counter += 1

                # Extract alt text if present
                alt_match = re.search(r'alt=["\']([^"\']*)["\']', full_tag)
                alt_text = alt_match.group(1) if alt_match else 'image'

                # Replace with markdown syntax
                return f"![{alt_text}]({local_path})"

            return full_tag

        content = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', replace_html_image, content)

        # Generate output filename
        base_path = input_file.parent
        while base_path.name not in ['en', 'cn']:
            base_path = base_path.parent

        output_filename = slugify_path(input_file, base_path)
        output_file = output_dir / output_filename

        # Write processed content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return True

    except Exception as e:
        print(f"  Error processing {input_file.name}: {e}")
        return False


def main():
    # Paths
    github_repo = Path('/home/memos/Development/MemOS/memos-data-loader/docs/github-memos-docs')
    source_dir = github_repo / 'content' / 'en'
    output_base = Path('/home/memos/Development/MemOS/memos-data-loader/docs/processed')
    output_dir = output_base / 'github-memos-docs'
    images_dir = output_dir / 'IMAGES'

    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(exist_ok=True)

    print("="*70)
    print("PROCESSING GITHUB MEMOS-DOCS REPOSITORY")
    print("="*70)
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    print()

    # Find all markdown files
    md_files = list(source_dir.rglob('*.md'))
    print(f"Found {len(md_files)} markdown files\n")

    # Process each file
    success_count = 0
    for md_file in md_files:
        rel_path = md_file.relative_to(source_dir)
        print(f"Processing: {rel_path}")

        if process_markdown_file(md_file, output_dir, images_dir):
            success_count += 1

        # Small delay to be nice to CDN
        time.sleep(0.5)

    # Count images
    img_count = len(list(images_dir.glob('*')))

    print("\n" + "="*70)
    print("PROCESSING COMPLETE")
    print("="*70)
    print(f"Files processed: {success_count}/{len(md_files)}")
    print(f"Images downloaded: {img_count}")
    print(f"Output directory: {output_dir}")
    print("="*70)


if __name__ == '__main__':
    main()
