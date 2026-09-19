#!/usr/bin/env python3
"""Publish a WordPress post via the REST API using an application password.

Usage: wp-direct-publish.py <site> <username> <title> <slug> <content_file> <status>
The application password is read from stdin (never from argv, files, or env).
Nothing is stored. Exit 0 prints JSON with id/link/status/slug.
"""
import sys
import json
import base64
import urllib.request
import urllib.error


def main():
    if len(sys.argv) != 7:
        print(
            "usage: wp-direct-publish.py <site> <username> <title> <slug> <content_file> <status>",
            file=sys.stderr,
        )
        sys.exit(2)
    site, username, title, slug, content_file, status = sys.argv[1:7]
    # App passwords are displayed in space-separated chunks; WP accepts them
    # with or without spaces. Normalize by stripping all whitespace.
    password = "".join(sys.stdin.read().split())
    if not password:
        print("no password received on stdin", file=sys.stderr)
        sys.exit(2)
    with open(content_file, encoding="utf-8") as f:
        content = f.read()
    creds = base64.b64encode(f"{username}:{password}".encode()).decode()
    payload = json.dumps(
        {"title": title, "slug": slug, "content": content, "status": status}
    ).encode()
    req = urllib.request.Request(
        f"{site.rstrip('/')}/wp-json/wp/v2/posts",
        data=payload,
        headers={
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/json",
            "User-Agent": "GlintDirectPublish/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:600]
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    print(
        json.dumps(
            {
                "id": data.get("id"),
                "link": data.get("link"),
                "status": data.get("status"),
                "slug": data.get("slug"),
            }
        )
    )


if __name__ == "__main__":
    main()
