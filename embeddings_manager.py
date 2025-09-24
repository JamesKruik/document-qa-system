import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_embeddings(chunks):
    """Create embeddings for chunks with metadata"""
    embeddings = []
    print(f"Creating embeddings for {len(chunks)} chunks...")
    
    for i, chunk_data in enumerate(chunks):
        if i % 10 == 0:  # Progress indicator
            print(f"Processing chunk {i+1}/{len(chunks)}")
        
        # Handle both old format (string) and new format (dict)
        if isinstance(chunk_data, dict):
            chunk_text = chunk_data['text']
            metadata = {
                'source_file': chunk_data.get('source_file', ''),
                'page': chunk_data.get('page', 1),
                'chunk_id': chunk_data.get('chunk_id', f'chunk_{i}')
            }
        else:
            # Legacy format - just text
            chunk_text = chunk_data
            metadata = {'chunk_id': f'legacy_chunk_{i}'}
        
        try:
            emb = client.embeddings.create(
                model="text-embedding-3-small",
                input=chunk_text
            )
            embeddings.append({
                "chunk": chunk_text,
                "embedding": emb.data[0].embedding,
                "metadata": metadata
            })
        except Exception as e:
            print(f"Error creating embedding for chunk {i}: {e}")
            continue
    
    print(f"Successfully created {len(embeddings)} embeddings")
    return embeddings

def save_embeddings(embeddings, file_path="embeddings.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(embeddings, f)

def load_embeddings(file_path="embeddings.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
