---
source_url: https://memos-docs.openmem.net/open_source/contribution/setting_up
section: Contribution
scraped_date: 2025-10-16
title: Setting Up Your Development Environment
has_images: no
has_tables: no
---

# Setting Up Your Development Environment
 [ To contribute to MemOS, you'll need to set up your local development environment. ] [ ] #### Fork & Clone the Repository
 
[Set up the repository on your local machine:]
 
- [Fork the repository on GitHub]
- [Clone your fork to your local machine:
git clone https://github.com/YOUR-USERNAME/MemOS.git
cd MemOS
]
- [Add the upstream repository as a remote:
git remote add upstream https://github.com/MemTensor/MemOS.git
]
 
#### Install Poetry
 
[Install Poetry for dependency management:]
 
```
curl -sSL https://install.python-poetry.org | python3 -

```
 
[Or follow the [[official instructions](https://python-poetry.org/docs/#installing-with-the-official-installer)].]
 
[Verify installation:]
 
```
poetry --version

```
 
#### Install Dependencies and Set Up Pre-commit Hooks
 
[Install all project dependencies and development tools:]
 
```
make install

```
 
[As the environment changes across commit history, you may need to **re-run make install** time to time to ensure all dependencies are up-to-date.]
