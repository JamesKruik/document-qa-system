from document_loader import load_and_chunk
from embeddings_manager import create_embeddings, save_embeddings, load_embeddings

from vector_search import find_most_relevant
from qa_agent import ask_gpt
import os

PDF_FILES = ["2103115-Calumino-EVK-QuickStart-Guide.pdf", "2103115-Calumino-EVK-QuickStart-Guide.pdf"]  # your two PDFs
EMBEDDINGS_FILE = "embeddings.json"

def main():
    # Step 1: Load PDFs and chunk text
    print("Loading and chunking documents...")
    chunks = load_and_chunk(PDF_FILES)

    # Step 2: Create embeddings if not already saved
    if os.path.exists(EMBEDDINGS_FILE):
        print("Loading embeddings from file...")
        embeddings = load_embeddings(EMBEDDINGS_FILE)
    else:
        print("Creating embeddings...")
        embeddings = create_embeddings(chunks)
        save_embeddings(embeddings, EMBEDDINGS_FILE)

    # Step 3: Live Q&A loop
    print("Ready! Ask a question about your documents.")
    while True:
        query = input("\nQuestion (or 'exit' to quit): ")
        if query.lower() == "exit":
            break
        context = find_most_relevant(query, embeddings)
        answer = ask_gpt(query, context)
        print(f"\nAnswer:\n{answer}")

if __name__ == "__main__":
    main()
