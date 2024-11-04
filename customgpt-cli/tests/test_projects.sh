#!/bin/bash

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

# Test listing projects
print_header "Testing list-projects command"
customgpt-cli list-projects
check_success "List projects (table format)"

customgpt-cli list-projects --format json
check_success "List projects (JSON format)"

customgpt-cli list-projects --format id-only
check_success "List projects (ID only format)"

# Test creating a new project
print_header "Testing create-project command"
NEW_PROJECT_ID=$(customgpt-cli create-project --name "$TEST_PROJECT_NAME" --sitemap "$SITEMAP_URL" --format id-only)
check_success "Create new project" "exit"
print_success "New project ID: $NEW_PROJECT_ID"

# Test showing project details
print_header "Testing show-project command"
customgpt-cli show-project --project-id $NEW_PROJECT_ID
check_success "Show project details (table format)"

customgpt-cli show-project --project-id $NEW_PROJECT_ID --format json
check_success "Show project details (JSON format)"

# Test project stats
print_header "Testing project-stats command"
customgpt-cli project-stats --project-id $NEW_PROJECT_ID
check_success "Get project stats (table format)"

customgpt-cli project-stats --project-id $NEW_PROJECT_ID --format json
check_success "Get project stats (JSON format)"

# Test updating project
print_header "Testing update-project command"
UPDATED_NAME="$TEST_PROJECT_NAME Updated"
customgpt-cli update-project --project-id $NEW_PROJECT_ID --name "$UPDATED_NAME"
check_success "Update project name"

# Test project replication
print_header "Testing replicate-project command"
REPLICATED_PROJECT_ID=$(customgpt-cli replicate-project --project-id $NEW_PROJECT_ID --format id-only)
check_success "Replicate project"
print_success "Replicated project ID: $REPLICATED_PROJECT_ID"

# Test project deletion
print_header "Testing delete-projects command"
echo "Deleting both original and replicated projects..."
customgpt-cli delete-projects --project-ids "$NEW_PROJECT_ID,$REPLICATED_PROJECT_ID" --force
check_success "Delete projects"

# Additional filtering tests for list-projects
print_header "Testing list-projects with filters"
customgpt-cli list-projects --name-filter "Test" --format json
check_success "List projects with name filter"

customgpt-cli list-projects --inactive-days 30 --format json
check_success "List projects with inactivity filter"

customgpt-cli list-projects --min-queries 10 --max-queries 1000 --format json
check_success "List projects with query count filters"

customgpt-cli list-projects \
    --min-pages-found 1 \
    --min-pages-crawled 1 \
    --min-pages-indexed 1 \
    --min-words-indexed 1000 \
    --format json
check_success "List projects with comprehensive stats filters"

# Final summary
print_header "Test Summary"
echo -e "${GREEN}Project command tests completed.${NC}"
echo "Note: Some tests might show expected errors for invalid inputs or non-existent projects."
echo "Remember to check the output manually for expected results."

# Clean up environment variables
unset TEST_PROJECT_NAME
unset SITEMAP_URL
