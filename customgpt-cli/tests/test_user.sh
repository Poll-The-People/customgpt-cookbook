# test user cli commands

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

print_header "Testing get-user command"
customgpt-cli get-user
check_success "Get user"