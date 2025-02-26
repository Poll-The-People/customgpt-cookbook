# test reports cli commands

PROJECT_ID=51241

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

print_header "Testing get-traffic-report command"
customgpt-cli get-traffic-report --project-id $PROJECT_ID --filters '["traffic", "pages"]'
check_success "Get traffic report"

print_header "Testing get-queries-report command"
customgpt-cli get-queries-report --project-id $PROJECT_ID --filters '["queries", "pages"]'
check_success "Get queries report"

print_header "Testing get-conversations-report command"
customgpt-cli get-conversations-report --project-id $PROJECT_ID --filters '["conversations", "pages"]'
check_success "Get conversations report"

print_header "Testing get-analysis-report command"
customgpt-cli get-analysis-report --project-id $PROJECT_ID --filters '["analysis", "pages"]'
check_success "Get analysis report"