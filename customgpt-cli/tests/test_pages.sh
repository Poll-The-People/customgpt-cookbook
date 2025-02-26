#!/bin/bash
export PROJECT_ID=51241
# First, set your environment variables
export TEST_PROJECT_NAME="CLI Test Project $(date +%s)"
export SITEMAP_URL="https://adorosario.github.io/small-sitemap.xml"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'

# Helper function for printing
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to check command success
check_success() {
    if [ $? -eq 0 ]; then
        print_success "$1"
    else
        print_error "$1"
        if [ "$2" = "exit" ]; then
            exit 1
        fi
    fi
}

# use _handle_pages_commands to test all page-related commands

# Test pages
print_header "Testing pages command"
PAGE_ID=$(customgpt-cli get-pages --project-id $PROJECT_ID | grep -A10 '"pages": {' | grep -o '"id": [0-9]*' | head -1 | awk '{print $2}')
echo "PAGE_ID: $PAGE_ID"
check_success "List pages"
# Test sync page
print_header "Testing sync-page command"
customgpt-cli reindex-page --project-id $PROJECT_ID --page-id $PAGE_ID
check_success "Sync page"

# Test delete page
print_header "Testing delete-page command"
# customgpt-cli delete-page --project-id $PROJECT_ID --page-id $PAGE_ID
check_success "Delete page"

# use all filters to test get-pages command

# Test get-pages command with filters
print_header "Testing get-pages command with filters"
customgpt-cli get-pages --project-id $PROJECT_ID --page $PAGE_ID --duration 90 --order asc
check_success "Get pages with filters"