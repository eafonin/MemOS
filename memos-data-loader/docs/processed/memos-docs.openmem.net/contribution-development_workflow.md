---
source_url: https://memos-docs.openmem.net/open_source/contribution/development_workflow
section: Contribution
scraped_date: 2025-10-16
title: Development Workflow
has_images: no
has_tables: no
---

# Development Workflow
 [
[Follow these steps to contribute to the project.]
 [
#### Sync with Upstream

[If you've previously forked the repository, sync with the upstream changes:]

```
git checkout dev # switch to dev branch
git fetch upstream # fetch latest changes from upstream
git pull upstream dev # merge changes into your local dev branch
git push origin dev # push changes to your fork

```

#### Create a Feature Branch

[Create a new branch for your feature or fix:]

```
git checkout -b feat/descriptive-name

```

#### Make Your Changes

[Implement your feature, fix, or improvement in the appropriate files.]

- [For example, you might add a function in `src/memos/hello_world.py` and create corresponding tests in `tests/test_hello_world.py`.]

#### Test Your Changes

[Run the test suite to ensure your changes work correctly:]

```
make test

```

#### Commit Your Changes

[Follow the project's commit guidelines (see [Commit Guidelines](/open_source/contribution/commit_guidelines)) when committing your changes.]

#### Push to Your Fork

[Push your feature branch to your forked repository:]

```
git push origin feat/descriptive-name

```

#### Create a Pull Request

[Submit your changes for review:]

- [**Important:** Please create your pull request against
â the dev branch of the upstream repository,â not the main branch of the upstream repository.]
- [Go to the original repository on GitHub]
- [Click on "Pull Requests"]
- [Click on "New Pull Request"]
- [Select `dev` as the base branch, and your branch as compare]
- [Fulfill the PR description carefully.]
