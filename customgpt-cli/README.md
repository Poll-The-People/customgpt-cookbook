# CustomGPT CLI

[![PyPI version](https://badge.fury.io/py/customgpt-cli.svg)](https://badge.fury.io/py/customgpt-cli)
[![Python Support](https://img.shields.io/pypi/pyversions/customgpt-cli.svg)](https://pypi.org/project/customgpt-cli/)
[![Documentation Status](https://readthedocs.org/projects/customgpt-cli/badge/?version=latest)](https://customgpt-cli.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://codecov.io/gh/yourusername/customgpt-cli/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/customgpt-cli)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker Pulls](https://img.shields.io/docker/pulls/yourusername/customgpt-cli.svg)](https://hub.docker.com/r/yourusername/customgpt-cli)

🚀 A powerful command-line interface for CustomGPT SDK, enabling efficient project management and automation.

## ✨ Features

- 🛠️ Full CustomGPT SDK integration
- 🔐 Secure API key management
- 📊 Project management and monitoring
- 🤖 Conversation handling
- 📄 Page management
- 🐳 Docker support
- 🔄 Bulk operations
- 📊 Advanced filtering

## Installation

```bash
pip install customgpt-cli
```

## Authentication

The CLI requires your CustomGPT API key. You can provide it in two ways:

1. Environment Variable (recommended):
```bash
export CUSTOMGPT_API_KEY=your_api_key
customgpt-cli list-projects
```

2. Command Line Argument:
```bash
customgpt-cli --api-key YOUR_API_KEY list-projects
```

Note: Command line argument takes precedence over environment variable if both are set.

## Usage

### Project Management

Create a project:
```bash
# Using environment variable
export CUSTOMGPT_API_KEY=your_api_key

# With a sitemap
customgpt-cli create-project --name "My Project" --sitemap https://example.com/sitemap.xml

# With a file
customgpt-cli create-project --name "My Project" --file /path/to/file.pdf
```

List projects with filtering:
```bash
# Basic listing
customgpt-cli list-projects

# Filter by name pattern (supports regex)
customgpt-cli list-projects --name-filter "test.*project"

# Filter by activity
customgpt-cli list-projects --inactive-days 30

# Filter by query count
customgpt-cli list-projects --min-queries 100 --max-queries 1000

# Change output format
customgpt-cli list-projects --format json
customgpt-cli list-projects --format table
customgpt-cli list-projects --format id-only
```

Update a project:
```bash
customgpt-cli update-project --project-id PROJECT_ID --name "New Name" --is-shared 1
```

Delete projects:
```bash
# Delete single project
customgpt-cli delete-projects --project-ids PROJECT_ID

# Delete multiple projects
customgpt-cli delete-projects --project-ids "id1,id2,id3"

# Delete (with dry run)
customgpt-cli delete-projects --project-ids PROJECT_ID --dry-run

# Force delete without confirmation
customgpt-cli delete-projects --project-ids PROJECT_ID --force
```

### Conversation Management

Create a conversation:
```bash
customgpt-cli create-conversation --project-id PROJECT_ID --name "My Conversation"
```

Send a message:
```bash
# Without streaming
customgpt-cli send-message --project-id PROJECT_ID --session-id SESSION_ID --prompt "Hello"

# With streaming
customgpt-cli send-message --project-id PROJECT_ID --session-id SESSION_ID --prompt "Hello" --stream

# With custom persona
customgpt-cli send-message --project-id PROJECT_ID --session-id SESSION_ID --prompt "Hello" --persona "You are a helpful assistant"
```

### Page Management

Get project pages:
```bash
customgpt-cli get-pages --project-id PROJECT_ID
```

Delete a page:
```bash
customgpt-cli delete-page --project-id PROJECT_ID --page-id PAGE_ID
```

Reindex a page:
```bash
customgpt-cli reindex-page --project-id PROJECT_ID --page-id PAGE_ID
```

## Scripting Examples

Here is an examples of how to use the CLI in scripts:

1. Export project IDs to a file and process them:
```bash
#!/bin/bash
export CUSTOMGPT_API_KEY=your_api_key

# Export IDs
customgpt-cli list-projects --name-filter "test" --format id-only > projects.txt

# Process the IDs
customgpt-cli delete-projects --project-ids $(paste -s -d, projects.txt) --force
```

## Output Formats

The CLI supports multiple output formats for better integration with other tools:

- `table`: Human-readable formatted table (default)
- `json`: JSON format for parsing
- `csv`: CSV format for stats data
- `id-only`: Just the IDs, one per line (good for scripting)

## Safety Features

The CLI includes several safety features:

- `--dry-run`: Shows what would be deleted without actually deleting
- Confirmation prompts for destructive operations
- `--force` flag to skip confirmations in scripts
- Error handling with informative messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License