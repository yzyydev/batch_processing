import anthropic
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key from environment
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=anthropic_api_key)

# Batch ID to track and retrieve
batch_id = "msgbatch_016RSGZLJjs35kjNXinuWqEM"

# Track batch processing status
message_batch = client.messages.batches.retrieve(batch_id)
print(f"Batch {message_batch.id} processing status is {message_batch.processing_status}")

# Stream and process results
print("\nRetrieving batch results:")
for result in client.messages.batches.results(batch_id):
    match result.result.type:
        case "succeeded":
            print(f"Success! {result}")
        case "errored":
            if result.result.error.type == "invalid_request":
                # Request body must be fixed before re-sending request
                print(f"Validation error {result.custom_id}")
            else:
                # Request can be retried directly
                print(f"Server error {result.custom_id}")
        case "expired":
            print(f"Request expired {result.custom_id}")