import os

def analyze_with_ai(vulnerabilities_json, ai_service):
    # Prompt para darle el rol de experto en seguridad
    prompt = f"""
    Eres un experto en DevSecOps y Python encargado de supervisar el código subido a un repositorio. Analiza estos resultados de Bandit (JSON) con el propósito de asegurar un código seguro:
    '''
    {vulnerabilities_json}
    '''
    Para cada vulnerabilidad:
    1. Explica el riesgo (El porqué el código escrito es vulnerable).
    2. Mantén los enlaces generados por Bandit para referencia.
    3. Proporciona el código corregido (Secure Code Patch) de ese segmento.
    La respuesta debe ser en formato Markdown usando encabezados (##), comparación de código vulnerable y código seguro mediante tablas, todo manteniendo la sintaxis de Python.
    """
    
    # Lógica de llamada a la API
    try:
        if ai_service == "openai":
            from openai import OpenAI 
            api_key = os.getenv("OPENAI_API_KEY")
            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model="gpt-5",
                input=prompt,
                reasoning= {"effort": "low"}
            )
            response_text = response.output_text
        elif ai_service == "gemini":
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            response = client.responses.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_level="low")
                ),  
            )
            response_text = response.text
        else:
            print("Servicio de IA no reconocido")
            return ""

    except Exception as e:
        print(f"Error al conectar con la plataforma de IA: {e}")
        return ""
    
    return response_text