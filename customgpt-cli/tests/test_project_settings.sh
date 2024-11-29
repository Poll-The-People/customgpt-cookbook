# test project settings

# First, set your environment variables
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
    
# Test project settings
print_header "Testing project settings command"
customgpt-cli get-project-settings --project-id $PROJECT_ID
check_success "Get project settings"

print_header "Testing update-project-settings command"
customgpt-cli update-project-settings --project-id $PROJECT_ID --default-prompt "Test prompt" --chatbot-avatar "./tests/files/test.png" --chatbot-background "./tests/files/test.png" --example-questions '["Test questions"]' --response-source "default" --chatbot-msg-lang "en" --chatbot-color "#0e57cc" --chatbot-toolbar-color "#0e57cc" --persona-instructions "Test instructions" --citations-answer-source-label-msg "Test label" --citations-sources-label-msg "Test label" --hang-in-there-msg "Test message" --chatbot-siesta-msg "Test message" --is-loading-indicator-enabled --enable-citations 0 --enable-feedbacks --citations-view-type "user" --no-answer-message "Test message" --ending-message "Test message" --remove-branding --enable-recaptcha-for-public-chatbots --chatbot-model "gpt-4-o" --is-selling-enabled --license-slug "test" --selling-url "test"
check_success "Update project settings"
