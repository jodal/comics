# Agent instructions

Comics is a webcomics aggregator. It is a Django project. Each comic has one
crawler module in `src/comics/comics/`, which holds the comic's metadata and
the code that finds each release.

## Layout

| Path | Contents |
| --- | --- |
| `src/comics/comics/` | One crawler module per comic |
| `src/comics/aggregator/` | Crawler base classes, feed and page parsers, downloader |
| `src/comics/core/` | Models, metadata loading, services |
| `docs/` | User and developer documentation |
| `tests/` | Test suite |

## Commands

Run the full set of checks:

```sh
tox
```

Run one check at a time:

```sh
pytest                  # Tests
ruff format .           # Format the code
ruff check .            # Lint the code
basedpyright src        # Check the types
uvx rumdl check docs/   # Lint the documentation
```

Run a management command against the local development database:

```sh
uv run comics <command>
```

## Conventions

- Write the minimum code that solves the problem. Do not add speculative
  changes.
- Change only the code that the task needs.
- Use conventional commits. Do not use scopes. Use sentence case in the
  subject.
- Lint the documentation after you change any file in `docs/`.

## Routines

- To repair a crawler that no longer fetches releases, follow
  [.agents/fix-crawler.md](.agents/fix-crawler.md).
