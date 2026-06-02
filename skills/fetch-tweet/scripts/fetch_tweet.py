#!/usr/bin/env python3
"""Fetch tweet content via FxEmbed API (api.fxtwitter.com).

Usage:
    python fetch_tweet.py <x_url> [--json] [--translate <lang>]

Examples:
    python fetch_tweet.py https://x.com/garrytan/status/2020072098635665909
    python fetch_tweet.py https://twitter.com/karpathy/status/123456 --json
    python fetch_tweet.py https://x.com/someone/status/123 --translate ko
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error


def parse_x_url(url: str) -> tuple[str, str] | None:
    """Extract screen_name and status_id from X/Twitter URL."""
    patterns = [
        r"(?:https?://)?(?:www\.)?(?:x\.com|twitter\.com|fxtwitter\.com|fixupx\.com)/(\w+)/status/(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1), match.group(2)
    return None


def fetch_tweet(screen_name: str, status_id: str) -> dict:
    """Fetch tweet data from FxEmbed API."""
    api_url = f"https://api.fxtwitter.com/{screen_name}/status/{status_id}"
    req = urllib.request.Request(api_url, headers={"User-Agent": "fetch-tweet/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def format_number(n: int) -> str:
    """Format large numbers (e.g., 1234 -> 1.2K)."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def format_tweet(data: dict) -> str:
    """Format tweet data for display."""
    tweet = data.get("tweet", {})
    author = tweet.get("author", {})

    lines = []
    # Author
    name = author.get("name", "")
    handle = author.get("screen_name", "")
    bio = author.get("description", "")
    followers = author.get("followers", 0)
    lines.append(f"@{handle} ({name})")
    if bio:
        lines.append(f"  Bio: {bio}")
    lines.append(f"  Followers: {format_number(followers)}")
    lines.append("")

    # Tweet text
    lines.append(tweet.get("text", ""))
    lines.append("")

    # Engagement
    likes = tweet.get("likes", 0)
    retweets = tweet.get("retweets", 0)
    replies = tweet.get("replies", 0)
    bookmarks = tweet.get("bookmarks", 0)
    views = tweet.get("views", 0)
    lines.append(
        f"Likes: {format_number(likes)}  "
        f"RTs: {format_number(retweets)}  "
        f"Replies: {format_number(replies)}  "
        f"Bookmarks: {format_number(bookmarks)}  "
        f"Views: {format_number(views)}"
    )

    # Date
    created = tweet.get("created_at", "")
    if created:
        lines.append(f"Date: {created}")

    # Media
    media = tweet.get("media", {})
    if media:
        photos = media.get("photos", [])
        videos = media.get("videos", [])
        if photos:
            lines.append(f"\nMedia: {len(photos)} photo(s)")
            for p in photos:
                lines.append(f"  {p.get('url', '')}")
        if videos:
            lines.append(f"\nMedia: {len(videos)} video(s)")
            for v in videos:
                lines.append(f"  {v.get('url', '')}")

    # Quote tweet
    quote = tweet.get("quote")
    if quote:
        q_author = quote.get("author", {})
        lines.append(f"\n--- Quote: @{q_author.get('screen_name', '')} ---")
        lines.append(quote.get("text", ""))
        lines.append(f"Likes: {format_number(quote.get('likes', 0))}  Views: {format_number(quote.get('views', 0))}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch tweet via FxEmbed API")
    parser.add_argument("url", help="X/Twitter URL")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    parsed = parse_x_url(args.url)
    if not parsed:
        print(f"Error: Invalid X/Twitter URL: {args.url}", file=sys.stderr)
        sys.exit(1)

    screen_name, status_id = parsed

    try:
        data = fetch_tweet(screen_name, status_id)
    except urllib.error.HTTPError as e:
        print(f"Error: API returned {e.code} for @{screen_name}/status/{status_id}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Network error - {e.reason}", file=sys.stderr)
        sys.exit(1)

    if data.get("code") != 200:
        print(f"Error: {data.get('message', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_tweet(data))


if __name__ == "__main__":
    main()
