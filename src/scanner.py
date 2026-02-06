import argparse
import subprocess
import json

from ai_advisor import analyze_with_ai

def run_security_scan(target_path, ai_platform):
    print(f"🚀 Iniciando escaneo de seguridad en {target_path}...")
    
    # Ejecutamos Bandit sobre la carpeta src/
    result = subprocess.run(
        ["bandit", "-r", target_path, "-f", "json"], 
        capture_output=True, 
        text=True
    )
    
    # Bandit devuelve código 1 si encuentra vulnerabilidades
    scan_data = json.loads(result.stdout)
    
    if scan_data['results']:
        print(f"⚠️ Se encontraron {len(scan_data['results'])} vulnerabilidades.")
        # Enviamos los hallazgos a la IA para obtener sugerencias
        report = analyze_with_ai(scan_data, ai_platform)
        print("\n--- REPORTE DE IA ---\n")
        print(report)
    else:
        print("✅ No se detectaron vulnerabilidades críticas.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="./src", help="Ruta del código a evaluar")
    parser.add_argument("--ai_platform", default="gemini", choices=["gemini", "openai"], help="Servicio de IA a utilizar ('gemini', 'openai')")
    args = parser.parse_args()
    run_security_scan(args.path, args.ai_platform)