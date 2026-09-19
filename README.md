# wp-direct-publish

Publish a WordPress post via the REST API. No dependencies, no SDK, no stored credentials.

Built for an autonomous overnight publishing lane — storm-warning pulses that have to ship while the operator sleeps. The lane needed something boring and exact: byte-identical posts, zero improvisation, and an application password that never touches disk, argv, or environment variables. So the password comes in on stdin, gets used once, and is gone.

## Usage

```bash
printf '%s' "$APP_PASSWORD" | ./wp-direct-publish.py \
  https://example.com myuser "Hello world" hello-world body.html publish
```

Arguments: `<site> <username> <title> <slug> <content_file> <status>`

Exit 0 prints JSON:

```json
{"id": 123, "link": "https://example.com/hello-world/", "status": "publish", "slug": "hello-world"}
```

Non-zero exit prints the error to stderr (including the HTTP status and a truncated response body on API failures).

## Why stdin

A WordPress application password is a long-lived bearer token. Passing it as an argument exposes it in process listings; environment variables leak into crash dumps and child processes; files linger on disk. stdin is the smallest blast radius: pipe it in, use it once, never persist it.

## Notes

- Python 3, standard library only. Nothing to install.
- App passwords displayed in space-separated chunks work — all whitespace is stripped before use.
- `status` accepts anything the WP REST API accepts: `publish`, `draft`, `pending`, `future`.
- Dogfooded nightly on a real publishing lane before release.

Take it, make it better. If you build something better, come back — we'll be customer #1.

## License

MIT — see [LICENSE](LICENSE).
