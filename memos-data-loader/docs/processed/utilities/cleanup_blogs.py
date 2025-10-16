#!/usr/bin/env python3
"""
Cleanup blog directories:
- Remove empty IMAGES directories
- Rename article.md to unique names based on domain
"""

from pathlib import Path
import shutil


def cleanup_blog(blog_dir: Path):
    """Cleanup a single blog directory."""
    print(f"\nProcessing {blog_dir.name}...")

    # Check and remove empty IMAGES directory
    images_dir = blog_dir / 'IMAGES'
    if images_dir.exists():
        if not any(images_dir.iterdir()):
            print(f"  Removing empty IMAGES directory")
            images_dir.rmdir()
        else:
            img_count = len(list(images_dir.iterdir()))
            print(f"  Keeping IMAGES directory ({img_count} files)")

    # Rename article.md to unique name
    article_file = blog_dir / 'article.md'
    if article_file.exists():
        # Create new name from directory name
        new_name = f"{blog_dir.name}.md"
        new_path = blog_dir / new_name

        print(f"  Renaming article.md → {new_name}")
        article_file.rename(new_path)
    else:
        print(f"  Warning: article.md not found")


def main():
    base_path = Path('/home/memos/Development/MemOS/memos-data-loader/docs/processed')

    blog_dirs = [
        base_path / 'ai-plainenglish-io-memos',
        base_path / 'xugj520-cn-memos',
        base_path / 'llmmultiagents-com-memos'
    ]

    print("="*70)
    print("CLEANING UP BLOG DIRECTORIES")
    print("="*70)

    for blog_dir in blog_dirs:
        if blog_dir.exists():
            cleanup_blog(blog_dir)
        else:
            print(f"\nWarning: {blog_dir} does not exist")

    print("\n" + "="*70)
    print("CLEANUP COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()
