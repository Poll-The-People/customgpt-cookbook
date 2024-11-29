# citations test shell script based on customgpt_cli/openapi.json

export PROJECT_ID=51241
UUID=4a4f4547-9a47-4402-a620-339f78ed947f
# $(uuidgen)
echo "UUID: $UUID"

echo "Testing citations command"

# foll parse_citations in cli.py

CITATION_ID=$(customgpt-cli send-message --project-id $PROJECT_ID --session-id $UUID --prompt "Tell me about your knowledge base in 10 words." --format json | jq -r '.data.citations[0]')

echo "CITATION_ID: $CITATION_ID"
customgpt-cli get-citation --project-id $PROJECT_ID --citation-id $CITATION_ID