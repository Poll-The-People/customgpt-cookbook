# Docker Support for CustomGPT CLI Development

This document explains how to build and run the CustomGPT CLI tool using Docker in a development environment.

## Development Setup

The development setup mounts the current directory into the container, allowing you to modify code and test changes without rebuilding the image.

### Authentication

You can provide your API key in two ways:

1. Environment Variable (recommended):
   ```bash
   # On host machine
   export CUSTOMGPT_API_KEY=your_api_key
   docker run -it --rm \
     -v $(pwd):/app \
     -e CUSTOMGPT_API_KEY=$CUSTOMGPT_API_KEY \
     customgpt-cli-dev

   # Inside container
   customgpt-cli list-projects  # uses CUSTOMGPT_API_KEY from environment
   ```

2. Command Line Argument:
   ```bash
   # Inside container
   customgpt-cli --api-key YOUR_API_KEY list-projects
   ```

Note: Command line argument takes precedence over environment variable if both are set.

### Building the Development Image

Build the image from the project root:
```bash
docker build -t customgpt-cli-dev .
```

### Running in Development Mode

Start an interactive development session:
```bash
docker run -it --rm \
  -v $(pwd):/app \
  customgpt-cli-dev
```

This command:
- Mounts the current directory to `/app` (source code)
- Starts an interactive bash session

## Common Development Workflows

### 1. Modifying and Testing Code

When you modify the code:
```bash
# Inside the container
pip install -e /app  # Reinstall the package after changes
customgpt-cli --help  # Test your changes
```

### 2. Running CLI Commands

Set your API key and run commands:
```bash
# Inside the container
export CUSTOMGPT_API_KEY=your_api_key

# Test your implementation
customgpt-cli list-projects
customgpt-cli create-project --name "Test Project" --file test.pdf
```

### 3. Quick Command Execution

Run a single command without starting an interactive session:
```bash
docker run --rm \
  -v $(pwd):/app \
  customgpt-cli-dev customgpt-cli --api-key YOUR_API_KEY list-projects
```

## Using Docker Compose for Development

Create a `docker-compose.yml` file:

```yaml
version: '3'
services:
  cli:
    build: .
    volumes:
      - .:/app
    environment:
      - CUSTOMGPT_API_KEY=${CUSTOMGPT_API_KEY}
```

Start an interactive development session:
```bash
docker-compose run --rm cli
```

Run a specific command:
```bash
docker-compose run --rm cli customgpt-cli list-projects
```

## Development Tips

### Code Changes

1. **Live Code Updates**:
   - The source code is mounted at `/app`
   - Changes to the code are immediately available in the container
   - Remember to reinstall the package after changes: `pip install -e /app`

2. **Working with Files**:
   - Project directory is mounted at `/app` 

### Testing

1. **Running Tests**:
```bash
# Inside the container
cd /app
python -m pytest tests/
```

2. **Debugging**:
```bash
# Inside the container
python -m pdb /app/customgpt_cli/cli.py
```

### Environment Variables

Set up your development environment:
```bash
# On host terminal
export CUSTOMGPT_API_KEY=your_api_key

# Start container with environment variables
docker run -it --rm \
  -v $(pwd):/app \
  -e CUSTOMGPT_API_KEY \
  customgpt-cli-dev

# Inside container, API key is already available
customgpt-cli list-projects

# Or override with command line argument
customgpt-cli --api-key different_key list-projects
```

### File Permissions

If you encounter permission issues:
```bash
# In host terminal
sudo chown -R $(id -u):$(id -g) .
```

## Development Best Practices

1. **Version Control**:
   - The `.dockerignore` file excludes development artifacts
   - Keep the Docker image clean of development files
   - Don't commit API keys or sensitive data

2. **Testing Changes**:
   - Test changes in the container before committing
   - Verify functionality with different Python versions if needed
   - Check file permissions for generated files

3. **Performance**:
   - The development image includes all source files
   - Use volume mounts for development
   - Consider building a slimmer production image if needed

## Troubleshooting

1. **Module Not Found**:
```bash
# Inside container
pip install -e /app  # Reinstall the package
```

2. **File Permission Issues**:
```bash
# Inside container
ls -la /app  # Check file ownership
```

3. **Docker Volume Issues**:
```bash
# On host
docker volume ls  # List volumes
docker volume prune  # Clean up unused volumes
```

## Production Deployment

For production deployment, consider:
1. Creating a separate production Dockerfile
2. Removing development dependencies
3. Setting up proper user permissions
4. Configuring appropriate security measures
