import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client with API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Available models with their characteristics
AVAILABLE_MODELS = {
    "gpt-4o-mini": {
        "name": "GPT-4o Mini",
        "description": "Fast and cost-effective, good for simple questions",
        "cost": "Low",
        "accuracy": "Good",
        "max_tokens": 4000
    },
    "gpt-4o": {
        "name": "GPT-4o",
        "description": "Balanced performance and cost, excellent for most tasks",
        "cost": "Medium",
        "accuracy": "Excellent",
        "max_tokens": 4000
    },
    "gpt-4o-turbo": {
        "name": "GPT-4o Turbo",
        "description": "Fast GPT-4o variant with good performance",
        "cost": "Medium",
        "accuracy": "Excellent",
        "max_tokens": 4000
    },
    "gpt-4": {
        "name": "GPT-4",
        "description": "Highest accuracy, best for complex reasoning",
        "cost": "High",
        "accuracy": "Outstanding",
        "max_tokens": 4000
    }
}

def ask_gpt(question, context, model="gpt-4o", temperature=0.1):
    """Ask GPT a question with provided context using specified model"""
    try:
        # Enhanced system prompt for better accuracy
        system_prompt = """You are an expert technical assistant specializing in document analysis and question answering. 

Your task is to provide accurate, helpful answers based ONLY on the provided context. Follow these guidelines:

1. **Accuracy First**: Only use information explicitly stated in the context
2. **Be Specific**: Provide detailed, specific answers when the context supports it
3. **Acknowledge Limitations**: If the context doesn't contain enough information, clearly state this
4. **Technical Precision**: For technical documents, maintain precision in terminology and specifications
5. **Source Attribution**: When possible, reference which part of the context supports your answer

If the context is insufficient to answer the question completely, explain what information is missing and what you can determine from the available context."""

        user_prompt = f"""Context:
{context}

Question: {question}

Please provide a comprehensive answer based on the context above. If the context doesn't contain sufficient information, please explain what information is missing."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=AVAILABLE_MODELS[model]["max_tokens"]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response from OpenAI using {model}: {str(e)}"

def get_available_models():
    """Return information about available models"""
    return AVAILABLE_MODELS

def get_model_recommendation(question_complexity="medium"):
    """Get model recommendation based on question complexity"""
    recommendations = {
        "simple": "gpt-4o-mini",      # Fast, cheap for simple questions
        "medium": "gpt-4o",           # Balanced for most questions
        "complex": "gpt-4o-turbo",    # Good for complex technical questions
        "critical": "gpt-4"           # Highest accuracy for critical applications
    }
    return recommendations.get(question_complexity, "gpt-4o")
