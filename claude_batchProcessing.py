import os, time
import json
import datetime
from dotenv import load_dotenv
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=anthropic_api_key)

model_list = client.models.list(limit=20)

# Generate a dynamic custom_id based on current date and timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
custom_id = f"request_{timestamp}"

message_batch = client.messages.batches.create(
    requests=[
        Request(
            custom_id=custom_id,
            params=MessageCreateParamsNonStreaming(
                model="claude-3-5-haiku-20241022",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": "Hello, world",
                }]
            )
        )
    ]
)

print(message_batch)

# Extract batch ID and save to JSON file along with custom_id
batch_info = {
    "batch_id": message_batch.id,
    "custom_id": custom_id
}

# Save batch ID to JSON file for later retrieval
with open("batch_info.json", "w") as f:
    json.dump(batch_info, f)

print(f"Batch ID {message_batch.id} saved to batch_info.json")

batch_id = batch_info["batch_id"]
custom_id = batch_info.get("custom_id", "N/A")

# Track batch processing status
import logging

logging.basicConfig(filename='batch_processing.log', level=logging.INFO)

start_time = time.time()

def log_status():
    message_batch = client.messages.batches.retrieve(batch_id)
    logging.info(f"Processing Status: {message_batch.processing_status}")
    return message_batch.processing_status

while True:
    processing_status = log_status()
    if processing_status == "ended":
        break
    time.sleep(5)

end_time = time.time()
logging.info(f"Total Processing Time: {end_time - start_time} seconds")

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
