import anthropic
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Get API key from environment
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=anthropic_api_key)

# Read batch information from JSON file
try:
    with open("batch_info.json", "r") as f:
        batch_info = json.load(f)
    batch_id = batch_info["batch_id"]
    custom_id = batch_info.get("custom_id", "N/A")  # Use N/A if custom_id is not present
    print(f"Loaded batch ID: {batch_id} from batch_info.json")
    print(f"Request custom ID: {custom_id}")
except FileNotFoundError:
    print("batch_info.json not found. Please run claude_createBatch.py first.")
    exit(1)
except (json.JSONDecodeError, KeyError) as e:
    print(f"Error reading batch_info.json: {e}")
    exit(1)

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
