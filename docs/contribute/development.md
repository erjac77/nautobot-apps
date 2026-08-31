---
icon: lucide/hammer
---

# Development

## Overview

- Development inside a Container with [Dev Containers]
- Packaging and dependency management with [uv](https://docs.astral.sh/uv/)
- Python monorepo management with [uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
- Linting with [pre-commit](https://pre-commit.com) and [Ruff Linter](https://docs.astral.sh/ruff/linter/)
- Code formatting with [Ruff Formatter](https://docs.astral.sh/ruff/formatter/)
- Import sorting with [Ruff - isort (I)](https://docs.astral.sh/ruff/rules/#isort-i)
- Automated Python syntax upgrades with [Ruff - pyupgrade (UP)](https://docs.astral.sh/ruff/rules/#pyupgrade-up)
- Static type-checking with [ty](https://docs.astral.sh/ty/)
- Continuous integration with [GitHub Actions](https://github.com/features/actions)
- Automated uploads to [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)
- Testing with [pytest](https://docs.pytest.org/en/stable/)
- Code coverage with [Coverage.py](https://coverage.readthedocs.io/en/latest/)
- Documentation with [Zensical](https://zensical.org)
- Automated release notes with [Towncrier](https://towncrier.readthedocs.io/en/stable/index.html)

## How to setup your development environment

### Dev Container

It is highly recommended to use the `devcontainer` provided in this project. [Dev Containers] (devcontainers) package your application's operating system, dependencies, and tools into an isolated container. This eliminates setup friction by letting developers open any project inside a configured container, ensuring a consistent and fully functional development environment across all team machines.

#### Key Benefits

- **Environment Consistency:** Eliminates "it works on my machine" issues by ensuring every developer shares identical tool versions and configurations.
- **Instant Onboarding:** New developers can start coding immediately without manual setup or tribal knowledge.
- **Isolated Workspaces:** Prevents dependency conflicts by separating project tools from your host operating system and other projects.
- **Instant Tool Switching:** Instantly swaps your entire environment (including databases, runtimes, and extensions) simply by loading a different container.
- **Multi-Platform Support:** Provides a uniform development environment regardless of whether your team uses Windows, Mac, or Linux.
- **Custom Tooling:** Package specific IDE extensions, linters, and libraries directly with the project.

#### How to get started

To use the devcontainer, you will need a few basic tools installed on your computer.

- **Docker:** Ensure [Docker](https://www.docker.com) is installed and running.
- **Visual Studio Code:** Use [VS Code] for the best integrated experience.
- **Dev Containers Extension:** Install the [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) in [VS Code].
- **Open in Container:** Open the project folder in [VS Code] and click `Reopen in Container` when prompted.

## Directory layout

| Name                    | Type      | Description                                                |
| ----------------------- | --------- | ---------------------------------------------------------- |
| .devcontainer           | Directory | Devcontainer config for remote development.                |
| .github                 | Directory | GitHub workflows and issue/pr templates.                   |
| .vscode                 | Directory | VS Code workspace settings and tasks.                      |
| docs                    | Directory | Documentation source (Markdown, assets).                   |
| packages                | Directory | Nautobot apps (e.g., `nautobot-calendars`, test helpers).  |
| src                     | Directory | Runtime source (e.g., `nautobot_apps/manage.py`, configs). |
| .editorconfig           | File      | Editor configuration rules.                                |
| .gitignore              | File      | Files/folders excluded from Git.                           |
| .markdownlint.yaml      | File      | Markdown linting configuration.                            |
| .pre-commit-config.yaml | File      | Pre-commit hooks configuration.                            |
| .yamllint.yaml          | File      | YAML linter configuration.                                 |
| conftest.py             | File      | Pytest configuration for repository-level tests.           |
| docker-compose.yml      | File      | Docker Compose service definitions.                        |
| LICENSE.md              | File      | Project license text.                                      |
| nautobot.env            | File      | Environment variables for Nautobot runtime.                |
| pyproject.toml          | File      | Build/packaging and tooling configuration (PEP 518).       |
| README.md               | File      | Project overview and usage.                                |
| uv.lock                 | File      | Lockfile.                                                  |
| zensical.toml           | File      | Configuration file for Zensical.                           |

## Useful commands

### Running pytest

```bash
uv run pytest
uv run pytest --testmon
uv run pytest --cov
```

### Running Nautobot via the 'manage.py' command script

```bash
uv run python src/nautobot_apps/manage.py makemigrations
uv run python src/nautobot_apps/manage.py migrate
uv run python src/nautobot_apps/manage.py createsuperuser
uv run python src/nautobot_apps/manage.py runserver 0.0.0.0:8080 --insecure
uv run python src/nautobot_apps/manage.py celery worker --loglevel INFO
```

### Running the lint and type checkers

```bash
uvx ruff check
uvx ty check
```

### Running Zensical to preview the documentation

```bash
uvx zensical serve
```

### Bumping the version

```bash
cd packages/nautobot-calendars
uvx --from commitizen cz bump --yes
```

### Creating news fragments and building the changelog

```bash
uvx towncrier create --config pyproject.toml --dir docs/calendars 124.added
uvx towncrier build --config pyproject.toml --dir docs/calendars --version 0.0.0
```

[Dev Containers]: https://containers.dev
[VS Code]: https://code.visualstudio.com
