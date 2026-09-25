---
icon: lucide/git-pull-request
---

# Pull requests

The process and requirements we describe below serve as important guardrails that are essential to running an Open Source project and help us prevent wasted effort and ensure the integrity of the codebase. This is more important than ever as the number of attacks on Open Source projects by malicious actors and the amount of AI slop both increase.

## Before you start

Before you start work on a pull request (PR), we need you to open an issue and discuss it with us so we know what you are working on and so we can agree on the approach to take. This prevents you from spending time on a feature that may not align with the project's goals. You then reference the issue number in your PR to link back to our discussion.

!!! info
    Take note that we require PRs to be linked to an issue.

## Styles and linting

It is important that your edits produce clean commits that can be reviewed quickly and without distractions caused by spurious diffs caused by format changes that conflict with the style we use. The projects use the following styling and linting tools and you must make sure that you follow the configured styles and rules:

| Tool                                 | Description                 |
| ------------------------------------ | --------------------------- |
| [Ruff](https://docs.astral.sh/ruff/) | Linting and code formatting |
| [ty](https://docs.astral.sh/ty/)     | Type checking               |

!!! info
    Our development container comes with [pre-commit](https://pre-commit.com) hooks installed. Their purpose is to validate the code and check for formatting errors. In addition, we use an [.editorconfig](https://editorconfig.org) file that configures compatible editors to behave the same way for tasks like removing trailing whitespace or applying indentation styles.

## Commit message standards

We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification, with automatically computed scopes for changes derived from the structure of the project or from configuration. This helps us automate our release notes and versioning. Each commit message must follow this structure:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Accepted commit types

| Type       | Description                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------ |
| `feature`  | A new feature                                                                                          |
| `fix`      | A bug fix                                                                                              |
| `perf`     | A code change that improves performance                                                                |
| `refactor` | A code change that neither fixes a bug nor adds a feature                                              |
| `build`    | Changes that affect the build system or external dependencies                                          |
| `ci`       | Changes to our CI configuration files and scripts                                                      |
| `docs`     | Documentation only changes                                                                             |
| `style`    | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc) |
| `test`     | Adding missing tests or correcting existing tests                                                      |
