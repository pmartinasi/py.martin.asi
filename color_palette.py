import openai
import json
import os
import sys

def generate_metadata(api_key, image_path):
    prompt = ("Imagine you are a content creator for a stock agency. Create a title (MUST be lesser than 190 letters, including spaces), a description and a list of 20-45 keywords, shown in a single line, separated by commas (,) for this image.")
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI specialized in generating stock photography metadata."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    result = response["choices"][0]["message"]["content"]
    
    output_file = os.path.splitext(image_path)[0] + "_metadata.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(result)
    
    print(f"Metadata saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    API_KEY = "your-api-key-here"  # Replace with your actual OpenAI API key
    generate_metadata(API_KEY, image_path)
