<a name="aiursoft-template-documentation"></a>
# Aiursoft Template Documentation

This repository contains the English Markdown source for the [Aiursoft Template documentation](https://template-docs.aiursoft.com/), served by [DocsViewer](https://github.com/AiursoftWeb/DocsViewer).

## Overview

### What is Template Documentation?

This repository is the Markdown source for the Aiursoft ASP.NET Core project template, its features and step-by-step development tutorials. Read the published site at [https://template-docs.aiursoft.com/](https://template-docs.aiursoft.com/). The content is served by [DocsViewer](https://github.com/AiursoftWeb/DocsViewer), using `properdocs.yml` for navigation; the viewer renders the content and provides site navigation.

## Installation

Readers can use the published site without installing anything. To edit and validate the source, install Git and Python 3 with support for built-in generic annotations (Python 3.9 or newer), then clone the repository:

```bash
git clone https://github.com/AiursoftWeb/Template-Docs.git
cd Template-Docs
python3 check-links.py
```

The link checker uses only Python's standard library. It does not require a Python package install, Node.js or a .NET SDK. To host your own instance, follow the [DocsViewer installation instructions](https://github.com/AiursoftWeb/DocsViewer#install-with-docker) and configure it to read this documentation repository. This content repository does not ship a standalone application, Dockerfile or local site server.

## Usage

Start with [the before-you-start guide](Docs/Tutorial/before.md), or browse the sections in [properdocs.yml](properdocs.yml). Use the published site for its navigation and search.

### Editing documentation

Edit `Docs/` and update the navigation in `properdocs.yml`. Put chapter images in an `images/` subdirectory and run `python3 check-links.py` before submitting a merge request.

For a new or renamed page:

1. Add or edit the Markdown file under the appropriate chapter in `Docs/`.
2. Keep image paths relative to the document and provide descriptive alt text.
3. Add the page path to `nav` in `properdocs.yml`, relative to `Docs/`, and update links affected by renames.
4. Run the existing checker, review the rendered Markdown and submit a merge request. The viewer publishes content through its configured repository synchronization; merging this content does not deploy or upgrade DocsViewer itself.

### Project structure

- [Docs/](Docs/): published Markdown and chapter-local images; [Docs/README.md](Docs/README.md) is the documentation home page.
- [properdocs.yml](properdocs.yml): site metadata, source/edit links, Markdown extensions and the full ordered navigation tree.
- [check-links.py](check-links.py): existing content/link validation used by CI.
- [LICENSE](LICENSE): the repository's GPL-3.0 license.

## Configuration

The content configuration is [properdocs.yml](properdocs.yml), not `mkdocs.yml`. The viewer owns server settings, authentication, storage and synchronization; do not put server credentials in this public content repository.

| Key | Current meaning |
| --- | --- |
| `site_name`, `site_description` | Site title and description. |
| `repo_name`, `repo_url` | Source-repository identity and link. |
| `edit_uri` | Edit-link prefix; currently `edit/master/Docs/`. |
| `docs_dir` | `Docs`; navigation entries are relative to this directory. |
| `markdown_extensions` | The declared Markdown features, including details, fenced blocks, snippets and task lists. Keep content compatible with the renderer; do not assume a Python extension alone changes the deployed viewer. |
| `nav` | The complete ordered groups and page paths; keep the actual configuration in sync with content. External entries remain full URLs. |

For example, the existing home-page entry is structured as follows:

```yaml
docs_dir: Docs
nav:
  - Home:
    - Welcome: README.md
```

This is an excerpt, not a replacement for the complete configuration. Preserve all existing groups when adding a page. There are no content-repository runtime environment variables to set for the checker.

## Development

From the repository root, run the same command as CI:

```bash
python3 check-links.py
```

The existing check covers local Markdown links and images, unused/orphaned images and documents, empty or stub documents, image alt text and zero-byte images. It also considers the repository's YAML references. It does not validate remote HTTP availability, run the deployed DocsViewer or replace a visual preview. There is no MkDocs build or application deployment job in this repository's current CI.

**Preview and publication.** Review edited Markdown in your editor or repository preview; a full-site preview requires a configured DocsViewer instance. Host installation and upgrade belong to the viewer, while this repository supplies content. Keep the published site's current navigation and editing conventions when contributing.

To contribute, edit `Docs/`, update `properdocs.yml`, keep chapter images under `images/`, then run the checker before review.

## How to contribute

There are many ways to contribute to the project: logging bugs, submitting pull requests, reporting issues, and creating suggestions.

Even if you have push rights on the repository, you should create a personal fork and create feature branches there when you need them. This keeps the main repository clean and your workflow cruft out of sight.

We're also interested in your feedback on the future of this project. You can submit a suggestion or feature request through the issue tracker. To make this process more effective, we're asking that these include more information to help define them more clearly.


## License

Licensed under [GPL-3.0](LICENSE).
