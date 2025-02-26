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

# With a sitemap, return project ID
customgpt-cli create-project --name "My Test Project With Sitemap" --sitemap "https://adorosario.github.io/small-sitemap.xml" --format id-only

# With a file, returning JSON output. 
customgpt-cli create-project --name "My Test Project With File" --file /path/to/file.pdf --format json
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

Show a project details: 
```bash
customgpt-cli show-project --project-id PROJECT_ID --format json
```

Update a project:
```bash
customgpt-cli update-project --project-id PROJECT_ID --name "New Name" --is-shared 1 --format json
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

### Project Settings Management

Get project settings:
```bash
customgpt-cli get-project-settings --project-id PROJECT_ID
```

Update project settings:
```bash
customgpt-cli update-project-settings --project-id $PROJECT_ID --default-prompt "Test prompt" --chatbot-avatar "./tests/files/test.png" --chatbot-background "./tests/files/test.png" --example-questions '["Test questions"]' --response-source "default" --chatbot-msg-lang "en" --chatbot-color "#0e57cc" --chatbot-toolbar-color "#0e57cc" --persona-instructions "Test instructions" --citations-answer-source-label-msg "Test label" --citations-sources-label-msg "Test label" --hang-in-there-msg "Test message" --chatbot-siesta-msg "Test message" --is-loading-indicator-enabled --enable-citations 0 --enable-feedbacks --citations-view-type "user" --no-answer-message "Test message" --ending-message "Test message" --remove-branding --enable-recaptcha-for-public-chatbots --chatbot-model "gpt-4-o" --is-selling-enabled --license-slug "test" --selling-url "test"
```

### Plugin Management

Get plugins:
```bash
customgpt-cli get-plugins --project-id PROJECT_ID
```

Create plugins:
```bash
customgpt-cli create-plugin --project-id $PROJECT_ID --model-name "TestPlugin" --human-name "Test Assistant" --keywords "test,automation" --description "This is a helpful automation tool." --is-active
```

Update plugins:
```bash
customgpt-cli update-plugin --project-id $PROJECT_ID --model-name "Updated" --human-name "Updated Assistant" --keywords "updated,assistant" --description "Trusted information about indoor plants and gardening." --is-active
```

### Page Metadata Management

Get page metadata:
```bash
customgpt-cli get-page-metadata --project-id PROJECT_ID --page-id PAGE_ID
```

Update page metadata:
```bash
customgpt-cli update-page-metadata --project-id PROJECT_ID --page-id PAGE_ID --title "Page Title" --url "https://page-url.com" --description "Page description" --image "https://image-url.com/image.png"
```

### Report Management

Get reports:
```bash
# Get traffic report
customgpt-cli get-traffic-report --project-id PROJECT_ID --filters '["traffic", "pages"]'

# Get queries report
customgpt-cli get-queries-report --project-id PROJECT_ID --filters '["queries", "pages"]'

# Get conversations report
customgpt-cli get-conversations-report --project-id PROJECT_ID --filters '["conversations", "pages"]'

# Get analysis report
customgpt-cli get-analysis-report --project-id PROJECT_ID --filters '["analysis", "pages"]'
```

### Limits Management

Get limits:
```bash
customgpt-cli get-limits
```

### Citations Management

Get citations:
```bash
customgpt-cli get-citations --project-id PROJECT_ID --citation-id CITATION_ID
```

### Sources Management

Get sources:
```bash
customgpt-cli list-sources --project-id PROJECT_ID
```

Create a source:
```bash
# Create source with sitemap
customgpt-cli create-source --project-id PROJECT_ID --sitemap-path URL --file-data-retension --is-ocr-enabled --is-anonymized

# Create source with file
customgpt-cli create-source --project-id PROJECT_ID --file PATH --file-data-retension --is-ocr-enabled --is-anonymized
```

Update source:
```bash
customgpt-cli update-source --project-id PROJECT_ID --source-id SOURCE_ID --executive-js --data-refresh-frequency never --create-new-pages --remove-unexist-pages --refresh-existing-pages always --refresh-schedule ["00:00","08:00"]
```

Delete source:
```bash
customgpt-cli delete-source --project-id PROJECT_ID --source-id SOURCE_ID
```

Sync source:
```bash
customgpt-cli sync-source --project-id PROJECT_ID --source-id SOURCE_ID
```

### User Management

Get user:
```bash
customgpt-cli get-user
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