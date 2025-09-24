#!/usr/bin/env python3
"""
Model Comparison Script
Test different OpenAI models with the same question to compare performance
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_model_performance():
    """Test different models with sample questions"""
    
    # Sample context from Calumino documentation
    sample_context = """
    Configure a Wi-Fi Hotspot using the name "Calumino" and the password "Calumino_EVK123".
    Note: iPhone users will need to change the device name in Settings > General > About > Name.
    Ensure "Maximize Compatibility" is enabled in the Wi-Fi settings.
    The Calumino EVK supports both 2.4GHz and 5GHz bands.
    """
    
    sample_questions = [
        "What is the Wi-Fi password for the Calumino hotspot?",
        "What should iPhone users do to connect?",
        "What frequency bands does the Calumino EVK support?",
        "How do I configure the Wi-Fi hotspot?"
    ]
    
    models_to_test = [
        "gpt-4o-mini",
        "gpt-4o", 
        "gpt-4o-turbo",
        "gpt-4"
    ]
    
    print("🤖 Model Performance Comparison")
    print("=" * 50)
    
    for question in sample_questions:
        print(f"\n📝 Question: {question}")
        print("-" * 40)
        
        for model in models_to_test:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a technical assistant. Answer based only on the provided context."
                        },
                        {
                            "role": "user",
                            "content": f"Context:\n{sample_context}\n\nQuestion: {question}"
                        }
                    ],
                    temperature=0.1,
                    max_tokens=200
                )
                
                answer = response.choices[0].message.content
                print(f"\n{model}:")
                print(f"  {answer[:100]}{'...' if len(answer) > 100 else ''}")
                
            except Exception as e:
                print(f"\n{model}: Error - {str(e)}")
        
        print("\n" + "="*50)

def show_model_costs():
    """Display approximate costs for different models"""
    print("\n💰 Approximate Costs (per 1K tokens)")
    print("=" * 40)
    print("GPT-4o Mini:  $0.00015 (Input) / $0.0006 (Output)")
    print("GPT-4o:       $0.0025  (Input) / $0.01   (Output)")
    print("GPT-4o Turbo: $0.0025  (Input) / $0.01   (Output)")
    print("GPT-4:        $0.03    (Input) / $0.06   (Output)")
    print("\n💡 Recommendation:")
    print("- Use GPT-4o Mini for simple questions (cost-effective)")
    print("- Use GPT-4o for most technical questions (balanced)")
    print("- Use GPT-4 for complex reasoning (highest accuracy)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "costs":
        show_model_costs()
    else:
        test_model_performance()
        show_model_costs()
