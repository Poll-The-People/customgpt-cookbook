# First, set your environment variables
export PROJECT_ID=52093

# 1. Create a new conversation
customgpt-cli create-conversation --project-id $PROJECT_ID --name "Test Conversation" --format json

# 2. Create a conversation and save the session ID
SESSION_ID=$(customgpt-cli create-conversation --project-id $PROJECT_ID --name "Test Conversation" --format json | jq -r '.data.session_id')
echo $SESSION_ID

# 3. Update the conversation name
customgpt-cli update-conversation --project-id $PROJECT_ID --session-id $SESSION_ID --name "Updated Name" --format json

# 4. Send a basic message
customgpt-cli send-message --project-id $PROJECT_ID --session-id $SESSION_ID --prompt "Tell me about project management" --format json

# 5. Send a message with GPT-4 Turbo
customgpt-cli send-message --project-id $PROJECT_ID --session-id $SESSION_ID --prompt "Explain agile" --model gpt-4-turbo --format json

# 6. Send a message with custom persona
customgpt-cli send-message --project-id $PROJECT_ID --session-id $SESSION_ID --prompt "Best practices?" --persona "Technical expert" --format json

# 7. Send a message and save the prompt ID
PROMPT_ID=$(customgpt-cli send-message --project-id $PROJECT_ID --session-id $SESSION_ID --prompt "Test message" --format json | jq -r '.data.id')
echo $PROMPT_ID

# 9. Get all messages in ascending order
customgpt-cli get-messages --project-id $PROJECT_ID --session-id $SESSION_ID --order asc --page 1 --format json

# 10. Get all messages in descending order
customgpt-cli get-messages --project-id $PROJECT_ID --session-id $SESSION_ID --order desc --page 1 --format json

# 11. Get a specific message
customgpt-cli get-message --project-id $PROJECT_ID --session-id $SESSION_ID --prompt-id $PROMPT_ID --format json

# 8. Update message feedback
customgpt-cli update-message-feedback --project-id $PROJECT_ID --session-id $SESSION_ID --prompt-id $PROMPT_ID --reaction liked --format json


# 12. Test conversations
# First create a conversation

# Test different message configurations without streaming
echo "=== Testing Basic Message ==="
customgpt-cli send-message \
    --project-id $PROJECT_ID \
    --session-id $SESSION_ID \
    --prompt "Tell me about project management" \
    --format json | jq '.'

echo "=== Testing with GPT-4 Turbo ==="
customgpt-cli send-message \
    --project-id $PROJECT_ID \
    --session-id $SESSION_ID \
    --prompt "Explain agile methodologies" \
    --model gpt-4-turbo \
    --format json | jq '.'

echo "=== Testing with Custom Persona ==="
customgpt-cli send-message \
    --project-id $PROJECT_ID \
    --session-id $SESSION_ID \
    --prompt "What are the best project management tools?" \
    --persona "Technical expert" \
    --format json | jq '.'

echo "=== Testing with Own Content Response Source ==="
customgpt-cli send-message \
    --project-id $PROJECT_ID \
    --session-id $SESSION_ID \
    --prompt "Compare waterfall and agile methodologies" \
    --response-source own_content \
    --format json | jq '.'


# 12a. Test streaming mode 
customgpt-cli send-message --project-id $PROJECT_ID --session-id $SESSION_ID --prompt "Write a story" --stream

# 13. Delete the conversation
customgpt-cli delete-conversation --project-id $PROJECT_ID --session-id $SESSION_ID --force

# Error test cases
# 14. Test invalid session ID
customgpt-cli send-message --project-id $PROJECT_ID --session-id "invalid_id" --prompt "Test" --format json

# 15. Test invalid project ID
customgpt-cli create-conversation --project-id 999999999 --name "Test" --format json

# Quick cleanup script
cleanup_test() {
    local session_id=$1
    echo "Cleaning up conversation $session_id..."
    customgpt-cli delete-conversation \
        --project-id $PROJECT_ID \
        --session-id $session_id \
        --force 
}
cleanup_test $SESSION_ID
