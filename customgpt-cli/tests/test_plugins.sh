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

# Test plugins
print_header "Testing list-plugins command"
customgpt-cli list-plugins --project-id $PROJECT_ID
check_success "List plugins"

print_header "Testing create-plugin command"
customgpt-cli create-plugin --project-id $PROJECT_ID --model-name "TestPlugin" --human-name "Test Assistant" --keywords "test,automation" --description "This is a helpful automation tool." --is-active
check_success "Create plugin"

print_header "Testing update-plugin command"
customgpt-cli update-plugin --project-id $PROJECT_ID --model-name "Updated" --human-name "Updated Assistant" --keywords "updated,assistant" --description "Trusted information about indoor plants and gardening." --is-active
check_success "Update plugin"
