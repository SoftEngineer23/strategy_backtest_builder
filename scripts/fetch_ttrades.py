"""
Fetch TTrades price action articles for corpus expansion.
Downloads raw HTML content for processing.
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json
import time

# TTrades article URLs organized by category
ARTICLES = {
    "core_concepts": [
        {
            "id": "phases_consolidation",
            "title": "Phases of Price - Part 1: Consolidations",
            "url": "https://ttrades.com/phases-of-price-part-1-how-to-trade-consolidations-for-high-probability-setups/",
            "concepts": ["consolidation", "range", "breakout", "accumulation"]
        },
        {
            "id": "phases_expansion",
            "title": "Phases of Price - Part 2: Expansion",
            "url": "https://ttrades.com/phases-of-price-part-2-mastering-expansion-for-strong-trend-trades/",
            "concepts": ["expansion", "trend", "momentum", "impulse"]
        },
        {
            "id": "phases_retracement",
            "title": "Phases of Price - Part 3: Retracements",
            "url": "https://ttrades.com/phases-of-price-part-3-mastering-retracements-for-high-probability-setups/",
            "concepts": ["retracement", "pullback", "continuation", "fibonacci"]
        },
        {
            "id": "phases_reversal",
            "title": "Phases of Price - Part 4: Reversals",
            "url": "https://ttrades.com/phases-of-price-part-4-mastering-reversals-for-high-probability-setups/",
            "concepts": ["reversal", "trend_change", "exhaustion", "divergence"]
        },
        {
            "id": "phases_blending",
            "title": "Phases of Price - Part 5: Blending All Phases",
            "url": "https://ttrades.com/phases-of-price-part-5-how-to-blend-expansion-retracement-consolidation-reversal/",
            "concepts": ["phase_blending", "market_cycle", "context", "multi_phase"]
        },
        {
            "id": "market_structure_basic",
            "title": "Understanding Basic Market Structure",
            "url": "https://ttrades.com/understanding-basic-market-structure-in-trading/",
            "concepts": ["market_structure", "higher_highs", "lower_lows", "trend"]
        },
        {
            "id": "market_structure_advanced",
            "title": "Advanced Market Structure",
            "url": "https://ttrades.com/advanced-market-structure-simplified-from-short-term-to-long-term-trends/",
            "concepts": ["market_structure", "multi_timeframe", "nested_structure", "swing_points"]
        },
        {
            "id": "position_sizing",
            "title": "Mastering Position Sizing",
            "url": "https://ttrades.com/mastering-position-sizing-the-key-to-profitable-trading/",
            "concepts": ["position_sizing", "risk_management", "account_size", "lot_size"]
        }
    ],
    "entry_exit": [
        {
            "id": "timeframe_alignment",
            "title": "Timeframe Alignment",
            "url": "https://ttrades.com/timeframe-alignment-how-to-align-higher-and-lower-time-frames-for-precision-entries/",
            "concepts": ["timeframe", "multi_timeframe", "htf", "ltf", "entry"]
        },
        {
            "id": "protected_swings",
            "title": "Protected Swings",
            "url": "https://ttrades.com/protected-swings-understanding-trends-and-invalidations/",
            "concepts": ["protected_swing", "swing_high", "swing_low", "invalidation"]
        },
        {
            "id": "stop_loss_mastery",
            "title": "Stop Loss Mastery",
            "url": "https://ttrades.com/stop-loss-mastery-using-protected-swings-for-precise-invalidations/",
            "concepts": ["stop_loss", "invalidation", "risk", "protected_swing"]
        },
        {
            "id": "reversal_sequence",
            "title": "Reversal Sequence Entry Model",
            "url": "https://ttrades.com/reversal-sequence-building-an-entry-model-for-trading/",
            "concepts": ["reversal", "entry_model", "sequence", "setup"]
        }
    ]
}

RAW_OUTPUT_DIR = Path(__file__).parent.parent / 'data' / 'ttrades_raw'


def fetch_article(url, delay=1.0):
    """Fetch article HTML content with rate limiting."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    time.sleep(delay)
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def extract_content(html):
    """Extract main article content from HTML."""
    soup = BeautifulSoup(html, 'html.parser')

    # Remove unwanted elements
    for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer',
                                   'aside', 'iframe', 'noscript']):
        element.decompose()

    # Remove common ad/promo classes
    for selector in ['.cookie-notice', '.newsletter', '.sidebar', '.comments',
                     '.social-share', '.author-bio', '.related-posts', '.cta',
                     '.wp-block-buttons', '.elementor-widget-container']:
        for element in soup.select(selector):
            element.decompose()

    # Try to find main content area
    content = None

    # Try common content selectors
    for selector in ['article', '.entry-content', '.post-content',
                     '.article-content', 'main', '.content']:
        content = soup.select_one(selector)
        if content:
            break

    if not content:
        content = soup.body

    return content


def content_to_text(content):
    """Convert BeautifulSoup content to clean text with structure."""
    lines = []

    for element in content.descendants:
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(element.name[1])
            prefix = '#' * level
            text = element.get_text(strip=True)
            if text:
                lines.append(f"\n{prefix} {text}\n")

        elif element.name == 'p':
            text = element.get_text(strip=True)
            if text and len(text) > 20:
                lines.append(text + "\n")

        elif element.name == 'li':
            text = element.get_text(strip=True)
            if text:
                lines.append(f"- {text}")

        elif element.name in ['pre', 'code']:
            text = element.get_text(strip=True)
            if text:
                lines.append(f"```\n{text}\n```\n")

    # Clean up multiple blank lines
    result = '\n'.join(lines)
    while '\n\n\n' in result:
        result = result.replace('\n\n\n', '\n\n')

    return result.strip()


def fetch_all_articles():
    """Fetch all TTrades articles and save raw content."""
    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    total = sum(len(articles) for articles in ARTICLES.values())
    count = 0

    for category, articles in ARTICLES.items():
        print(f"\nCategory: {category}")

        for article in articles:
            count += 1
            print(f"  [{count}/{total}] Fetching: {article['title']}")

            try:
                html = fetch_article(article['url'])
                content = extract_content(html)
                text = content_to_text(content)

                # Save raw content
                output_path = RAW_OUTPUT_DIR / f"{article['id']}.json"
                output_data = {
                    'id': article['id'],
                    'title': article['title'],
                    'url': article['url'],
                    'category': category,
                    'concepts': article['concepts'],
                    'content': text
                }

                output_path.write_text(json.dumps(output_data, indent=2), encoding='utf-8')
                print(f"    Saved: {output_path.name} ({len(text)} chars)")

                results.append({
                    'id': article['id'],
                    'title': article['title'],
                    'chars': len(text),
                    'status': 'success'
                })

            except Exception as e:
                print(f"    ERROR: {e}")
                results.append({
                    'id': article['id'],
                    'title': article['title'],
                    'chars': 0,
                    'status': f'error: {e}'
                })

    # Summary
    print(f"\n{'='*60}")
    print("FETCH SUMMARY")
    print(f"{'='*60}")

    success = sum(1 for r in results if r['status'] == 'success')
    print(f"Successfully fetched: {success}/{total} articles")

    total_chars = sum(r['chars'] for r in results)
    print(f"Total content: {total_chars:,} characters")

    if success < total:
        print("\nFailed articles:")
        for r in results:
            if r['status'] != 'success':
                print(f"  - {r['title']}: {r['status']}")

    return results


if __name__ == '__main__':
    fetch_all_articles()
