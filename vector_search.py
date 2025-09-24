import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client with API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_most_relevant(query, embeddings, top_k=3, similarity_threshold=0.7):
    """Find the most relevant chunks for a query"""
    # Create embedding for the query
    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    # Compute similarities for all chunks
    similarities = []
    for i, e in enumerate(embeddings):
        sim = cosine_similarity(q_emb, e["embedding"])
        similarities.append((i, sim, e))
    
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Filter by threshold and get top_k
    relevant_chunks = []
    for i, sim, chunk_data in similarities[:top_k]:
        if sim >= similarity_threshold:
            relevant_chunks.append({
                'chunk': chunk_data['chunk'],
                'similarity': sim,
                'metadata': chunk_data.get('metadata', {})
            })
    
    # If no chunks meet threshold, return the best one anyway
    if not relevant_chunks and similarities:
        best_idx, best_sim, best_chunk = similarities[0]
        relevant_chunks.append({
            'chunk': best_chunk['chunk'],
            'similarity': best_sim,
            'metadata': best_chunk.get('metadata', {})
        })
    
    # Combine all relevant chunks into context
    if len(relevant_chunks) == 1:
        return relevant_chunks[0]['chunk']
    else:
        # Combine multiple chunks with clear separation
        combined_context = ""
        for i, chunk_info in enumerate(relevant_chunks):
            source = chunk_info['metadata'].get('source_file', 'Unknown')
            page = chunk_info['metadata'].get('page', 'Unknown')
            combined_context += f"[Context {i+1} from {os.path.basename(source)}, page {page}]\n"
            combined_context += chunk_info['chunk'] + "\n\n"
        return combined_context.strip()
