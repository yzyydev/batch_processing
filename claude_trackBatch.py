import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=anthropic_api_key)

message_batch = client.messages.batches.retrieve(
    "msgbatch_016RSGZLJjs35kjNXinuWqEM",
)
print(f"Batch {message_batch.id} processing status is {message_batch.processing_status}")
