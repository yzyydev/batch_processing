import os
import json
import datetime
from dotenv import load_dotenv
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=anthropic_api_key)

model_list=client.models.list(limit=20)

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
