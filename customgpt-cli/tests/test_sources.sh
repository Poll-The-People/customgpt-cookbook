#test sources

# First, set your environment variables
export PROJECT_ID=52093
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

# Test sources
print_header "Testing sources command"
customgpt-cli list-sources --project-id $PROJECT_ID
check_success "List sources"

# Test create source
print_header "Testing create-source command with sitemap"
SOURCE_ID=$(customgpt-cli create-source --project-id $PROJECT_ID --sitemap-path $SITEMAP_URL --file-data-retension --is-ocr-enabled --is-anonymized | jq -r '.data.id')
echo "SOURCE_ID: $SOURCE_ID"
check_success "Create source with sitemap"

# Test create source with file
print_header "Testing create-source command with file"
customgpt-cli create-source --project-id $PROJECT_ID --file ./tests/files/test.pdf --file-data-retension --is-ocr-enabled --is-anonymized
check_success "Create source with file"

# # Test update source
print_header "Testing update-source command"
customgpt-cli update-source --project-id $PROJECT_ID --source-id $SOURCE_ID --executive-js --data-refresh-frequency never --create-new-pages --remove-unexist-pages --refresh-existing-pages always --refresh-schedule ["00:00","08:00"]
check_success "Update source"


# Test delete source
print_header "Testing delete-source command"
customgpt-cli delete-source --project-id $PROJECT_ID --source-id $SOURCE_ID
check_success "Delete source"

# Test sync source
print_header "Testing sync-source command"
customgpt-cli sync-source --project-id $PROJECT_ID --source-id $SOURCE_ID
check_success "Sync source"