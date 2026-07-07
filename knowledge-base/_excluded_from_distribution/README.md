# Excluded from Commercial Distribution

Files in this directory are **not** included in the Coltex Product package
(`make product`) and must not be shipped in commercial releases.

## Why excluded

These documents are procedural placeholder stubs generated from templates.
They contain a single boilerplate paragraph and do not constitute substantive
original documentation suitable for commercial distribution.

Example marker:

> "This document provides detailed information on … as it relates to the
> Coltex Enterprise AI Coding Chatbot …"

## License status

These files are included under the commercial use license (see `knowledge-base/LICENSE`) but are
quarantined because they do not meet product quality standards — not because of
third-party copyright concerns.

## Subdirectories

| Directory | Contents | Count |
|-----------|----------|-------|
| `boilerplate-stubs/` | Single-paragraph placeholder "supporting documents" | 50 |
| `thin-stubs/` | Title-only incident reports and support tickets | 4 |


Release scripts, Docker images, and tarballs must exclude:

- `knowledge-base/_excluded_from_distribution/`
- `knowledge-base/generated/`
- `knowledge-base/_seed/`
