# Authoring a local documentation site

## Choose the workspace

Inspect the project's existing docs and publishing configuration first. Retain an existing site unless its owner approves a migration. This template is a separate example of the documentation workflow, not service documentation.

For a new site, use the reviewed project directory `docs-site/`. Before copying, confirm that it is empty and is not a symlink. Copy `templates/zensical.toml` and the contents of `templates/docs/` without overwriting existing files. Put the workflow's reviewed `requirements.lock` beside `zensical.toml`. Keep `github-pages.yml.example` outside `.github/workflows/`; it is not needed for local use.

The resulting workspace is:

```text
docs-site/
  zensical.toml
  requirements.lock
  docs/
    index.md
    media.md
    api.md
```

Do not replace an existing project lock or environment. Use the project's ignore convention for `docs-site/.venv/`, `docs-site/site/`, and local build caches. Keep editable documentation sources under review. Only add media that exists and has been reviewed.

## Install and preview locally

Installation needs separate approval. Zensical 0.0.71 requires Python 3.11 or newer, but this workflow's reviewed lock targets CPython 3.14 on Linux x86_64 only. The optional workflow uses Python 3.14 on `ubuntu-latest`. Other Python versions or platforms require an explicit lock refresh and review, not removal of hashes.

From `docs-site/`, after installation approval:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check --require-hashes --only-binary=:all: -r requirements.lock
```

Do not upgrade dependencies, remove hash checking, or fall back to source builds when a wheel is unavailable. Report the unsupported environment and review the lock separately.

When a local build is authorized, run from the same directory:

```sh
.venv/bin/zensical build
```

For an authorized local preview:

```sh
.venv/bin/zensical serve --dev-addr 127.0.0.1:8000
```

Open `http://127.0.0.1:8000/` in the existing browser. Stop the preview when finished. The preview server is not a production server. A build produces `site/`; it does not publish anything.

## Paths at the root and under a repository

Keep `docs_dir = "docs"`, `site_dir = "site"`, and `use_directory_urls = false`. The three pages become sibling `.html` files. This makes the relative media patterns in the template work both at the site root and beneath a repository prefix.

- Link Markdown pages by their source paths, such as `media.md`.
- Link assets with relative paths, such as `assets/system.html`, not `/assets/system.html`.
- Raw HTML paths resolve from the generated page. A nested page needs the corresponding `../` path.
- Keep related adapter output files together, including the static composition referenced by video playback HTML.
- Keep adapter-generated Markdown link fragments outside `docs/`. With `use_directory_urls = false`, `assets/system.md` renders to `assets/system.html` and can overwrite the actual interactive HTML; the same applies to video playback fragments. Paste links into the owning documentation page instead.

The local template omits `site_url`. Before publication, set it inside `[project]` to the actual canonical URL, including any repository prefix and a trailing slash. For example, a project site uses `https://OWNER.github.io/REPOSITORY/`; an account root site uses `https://OWNER.github.io/`. These are illustrative values, not destinations to use unchanged. A custom domain may use a different path.

The site URL does not repair absolute paths inside authored HTML. During authorized verification, serve the generated site at the intended path prefix and inspect page navigation, image and video requests, iframe loads, and direct links. Keep instant navigation disabled unless embedded script initialization has been checked across page transitions.

## Optional GitHub Pages publication

Publication is a separate decision. Review every file in `site/`, not only pages in navigation. Markdown can contain executable HTML, and local assets can expose private information. Build only trusted sources and reviewed configuration.

After explicit approval:

1. Confirm the destination repository, canonical URL, and content audience.
2. Enable GitHub Pages with GitHub Actions in the repository settings.
3. Configure the `github-pages` environment with the intended branch restrictions and required reviewers where available.
4. Review `templates/github-pages.yml.example`, its action pins, and the project's hash-locked binary dependencies.
5. Copy the example to `.github/workflows/docs-pages.yml` through the normal reviewed change process. Do not overwrite an existing workflow.
6. Dispatch it manually from the default branch after approval.

The example has no push or pull-request trigger. It builds `docs-site/` with read-only repository permission, uploads only `docs-site/site`, and gives Pages/OIDC permissions only to the deployment job. It neither renders media nor installs Scalar. Pre-generated media must already be reviewed site assets. No deployment or account configuration occurs merely by copying the local template.

The four top-level action commits were resolved from official repositories on 2026-10-19, and their `action.yml` files were inspected. The pinned upload-pages-artifact v3 action invokes `actions/upload-artifact@v4` internally. This transitive moving tag means the workflow is not a fully immutable action dependency graph. Review that residual dependency before activation. The runner image and Python patch release can also change; the package lock pins Python packages, not the entire execution environment.

## Sources and scope

- [Zensical configuration](https://zensical.org/docs/setup/basics/), [fonts](https://zensical.org/docs/setup/fonts/), [navigation](https://zensical.org/docs/setup/navigation/), and [preview](https://zensical.org/docs/usage/preview/): configuration and commands. These are current upstream docs, not a versioned 0.0.71 documentation snapshot.
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages): artifact deployment, permissions, and environment requirements.
- [checkout v4 source](https://github.com/actions/checkout/blob/11d5960a326750d5838078e36cf38b85af677262/action.yml)
- [setup-python v5 source](https://github.com/actions/setup-python/blob/a26af69be951a213d495a4c3e4e4022e16d87065/action.yml)
- [upload-pages-artifact v3 source](https://github.com/actions/upload-pages-artifact/blob/56afc609e74202658d3ffba0e8f6dda462b719fa/action.yml)
- [deploy-pages v4 source](https://github.com/actions/deploy-pages/blob/d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e/action.yml)

Read the installed Archify and HyperFrames skills for their local adapters and media contracts. This reference does not replace those instructions or authorize rendering, verification, installation, or publication.
