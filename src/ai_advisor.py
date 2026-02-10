import os
import sys

def analyze_with_ai(vulnerabilities_data, ai_service):
    # Security analysis prompt for the AI
    prompt = f"""
    You're a DevSecOps and Python expert tasked with overseeing code uploaded to a repository. Analyze these Bandit results (JSON) with the purpose of ensuring secure code:
    '''
    {vulnerabilities_data}
    '''
    For each vulnerability found, provide the following:
    1. Explain the risk (Why the written code is vulnerable).
    2. Keep the generated Bandit links for reference.
    3. Proporciona el código corregido (Secure Code Patch) de ese segmento.
    3. Show the fixed code (Secure Code Patch) for that segment.
    The answer should be in Markdown format using headers (##), comparison of vulnerable code and secure code using tables, all while maintaining Python syntax.
    """
    
    # API call logic for both OpenAI and Gemini (would be better to have a unified interface)
    try:
        api_key_ai = os.getenv("AI_API_KEY")
        if not api_key_ai:
            print("AI_API_KEY environment variable not set.")
            sys.exit(1)
        if ai_service == "openai":
            from openai import OpenAI 
            client = OpenAI(api_key=api_key_ai)
            response = client.responses.create(
                model="gpt-5",
                input=prompt,
                reasoning= {"effort": "low"}
            )
            response_text = response.output_text
        elif ai_service == "gemini":
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=str(api_key_ai))
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_level="low")
                ),  
            )
            response_text = response.text
        else:
            print("AI service not recognized")
            sys.exit(1)

    except Exception as e:
        print(f"Error connecting to AI platform: {e}")
        sys.exit(1)
    
    return response_text