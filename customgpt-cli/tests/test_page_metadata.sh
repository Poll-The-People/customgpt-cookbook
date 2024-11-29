export PROJECT_ID=51241

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

# Test page metadata
print_header "Testing get-page-metadata command"
PAGE_ID=$(customgpt-cli get-pages --project-id $PROJECT_ID --page 1 | jq -r '.data.pages.data[0].id')
customgpt-cli get-page-metadata --project-id $PROJECT_ID --page-id $PAGE_ID
check_success "Get page metadata"

print_header "Testing update-page-metadata command"
customgpt-cli update-page-metadata --project-id $PROJECT_ID --page-id $PAGE_ID --title "Test Title" --url "https://app.customgpt.ai" --description "This is a test page." --image "https://app.customgpt.ai/assets/imgs/default_chatbot_avatar.png"
check_success "Update page metadata"
