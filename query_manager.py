# query_manager.py
from embeddings_manager import load_embeddings
from vector_search import find_most_relevant
from qa_agent import ask_gpt

def main():
    # Load precomputed embeddings
    embeddings = load_embeddings("embeddings.json")

    print("Document Q&A System. Type 'exit' to quit.\n")

    while True:
        question = input("Ask a question: ")
        if question.lower() in ["exit", "quit"]:
            break

        # Find most relevant chunk(s)
        context = find_most_relevant(question, embeddings)

        # Ask GPT with retrieved context
        answer = ask_gpt(question, context)
        print(f"\nAnswer: {answer}\n")

if __name__ == "__main__":
    main()
