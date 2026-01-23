"""
Process raw TTrades content into chunked markdown files for the corpus.
Chunks by semantic sections with metadata tagging.
"""

import json
import re
from pathlib import Path
from typing import List, Dict

RAW_INPUT_DIR = Path(__file__).parent.parent / 'data' / 'ttrades_raw'
CORPUS_OUTPUT_DIR = Path(__file__).parent.parent / 'app' / 'corpus' / 'price_action'

# Target chunk size in characters (roughly 4 chars per token)
TARGET_CHUNK_CHARS = 2400  # ~600 tokens
MAX_CHUNK_CHARS = 3200     # ~800 tokens
OVERLAP_CHARS = 400        # ~100 tokens


def split_into_sections(content: str) -> List[Dict]:
    """Split content into sections based on headers."""
    sections = []
    current_section = {'header': None, 'level': 0, 'content': []}

    for line in content.split('\n'):
        # Check for header
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)

        if header_match:
            # Save previous section if it has content
            if current_section['content']:
                current_section['text'] = '\n'.join(current_section['content']).strip()
                if current_section['text']:
                    sections.append(current_section.copy())

            # Start new section
            level = len(header_match.group(1))
            header = header_match.group(2)
            current_section = {
                'header': header,
                'level': level,
                'content': []
            }
        else:
            current_section['content'].append(line)

    # Don't forget last section
    if current_section['content']:
        current_section['text'] = '\n'.join(current_section['content']).strip()
        if current_section['text']:
            sections.append(current_section)

    return sections


def create_chunks(sections: List[Dict], article_meta: Dict) -> List[Dict]:
    """Create overlapping chunks from sections."""
    chunks = []
    current_chunk = {
        'sections': [],
        'text': '',
        'headers': []
    }

    for section in sections:
        section_text = section.get('text', '')
        section_header = section.get('header', '')

        # If adding this section would exceed max, finalize current chunk
        if (len(current_chunk['text']) + len(section_text) > MAX_CHUNK_CHARS
                and current_chunk['text']):

            # Finalize chunk
            chunks.append(finalize_chunk(current_chunk, article_meta, len(chunks)))

            # Start new chunk with overlap from previous
            overlap_text = current_chunk['text'][-OVERLAP_CHARS:] if current_chunk['text'] else ''
            current_chunk = {
                'sections': [],
                'text': overlap_text,
                'headers': []
            }

        # Add section to current chunk
        if section_header:
            current_chunk['headers'].append(section_header)

        if section_text:
            if current_chunk['text'] and not current_chunk['text'].endswith('\n'):
                current_chunk['text'] += '\n\n'
            current_chunk['text'] += section_text
            current_chunk['sections'].append(section)

    # Don't forget last chunk
    if current_chunk['text'].strip():
        chunks.append(finalize_chunk(current_chunk, article_meta, len(chunks)))

    return chunks


def finalize_chunk(chunk: Dict, article_meta: Dict, index: int) -> Dict:
    """Create final chunk with metadata."""
    # Determine section name from headers
    section_name = chunk['headers'][0] if chunk['headers'] else 'Introduction'

    return {
        'id': f"{article_meta['id']}_{index:03d}",
        'title': article_meta['title'],
        'section': section_name,
        'category': article_meta['category'],
        'concepts': article_meta['concepts'],
        'url': article_meta['url'],
        'text': chunk['text'].strip(),
        'char_count': len(chunk['text'])
    }


def format_as_markdown(chunk: Dict) -> str:
    """Format chunk as markdown with header containing metadata."""
    # Main title
    md = f"# {chunk['title']}\n\n"

    # Section subtitle if different from title
    if chunk['section'] and chunk['section'] != chunk['title']:
        md += f"## {chunk['section']}\n\n"

    # Metadata block for reference (will be parsed by vector store)
    md += f"**Source:** TTrades Education\n"
    md += f"**Category:** {chunk['category']}\n"
    md += f"**Concepts:** {', '.join(chunk['concepts'])}\n\n"

    # Horizontal rule to separate metadata from content
    md += "---\n\n"

    # Main content
    md += chunk['text']

    return md


def process_all_articles():
    """Process all raw articles into chunked corpus files."""
    if not RAW_INPUT_DIR.exists():
        print(f"ERROR: Raw input directory not found: {RAW_INPUT_DIR}")
        print("Run fetch_ttrades.py first to download articles.")
        return

    CORPUS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load all raw articles
    raw_files = list(RAW_INPUT_DIR.glob('*.json'))
    print(f"Found {len(raw_files)} raw articles to process")

    all_chunks = []

    for raw_path in raw_files:
        print(f"\nProcessing: {raw_path.name}")

        with open(raw_path, 'r', encoding='utf-8') as f:
            article = json.load(f)

        # Split into sections
        sections = split_into_sections(article['content'])
        print(f"  Found {len(sections)} sections")

        # Create chunks
        chunks = create_chunks(sections, article)
        print(f"  Created {len(chunks)} chunks")

        for chunk in chunks:
            print(f"    - {chunk['id']}: {chunk['char_count']} chars")

        all_chunks.extend(chunks)

    # Write chunks as markdown files
    print(f"\n{'='*60}")
    print(f"Writing {len(all_chunks)} chunks to {CORPUS_OUTPUT_DIR}")
    print(f"{'='*60}")

    for chunk in all_chunks:
        md_content = format_as_markdown(chunk)
        output_path = CORPUS_OUTPUT_DIR / f"{chunk['id']}.md"
        output_path.write_text(md_content, encoding='utf-8')

    # Summary
    print(f"\nDone! Created {len(all_chunks)} markdown files.")

    total_chars = sum(c['char_count'] for c in all_chunks)
    avg_chars = total_chars / len(all_chunks) if all_chunks else 0
    print(f"Total content: {total_chars:,} characters")
    print(f"Average chunk size: {avg_chars:.0f} characters (~{avg_chars/4:.0f} tokens)")

    # By category breakdown
    categories = {}
    for chunk in all_chunks:
        cat = chunk['category']
        categories[cat] = categories.get(cat, 0) + 1

    print("\nChunks by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    return all_chunks


if __name__ == '__main__':
    process_all_articles()
