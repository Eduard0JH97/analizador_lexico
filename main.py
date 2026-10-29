import pathlib
from core.lexer import Lexer
from utils.file_reader import leer_archivo

def main():
    print("--- Analizador Léxico Multilenguaje ---")
    rules_path = pathlib.Path("rules/c_rules.json")
    
    if not rules_path.exists():
        print("Error: No se encontró el archivo de reglas (c_rules.json).")
        return
        
    lexer = Lexer(str(rules_path))
    print(f"Lenguaje configurado: {lexer.rules.get('lenguaje')}\n")
    
    ruta_txt = input("Por favor, ingrese la ruta de ubicación del archivo fuente (.txt): ")
    
    try:
        codigo_fuente = leer_archivo(ruta_txt)
        print("\n--- Iniciando Análisis Léxico ---\n")
        tokens = lexer.tokenize(codigo_fuente)
        
        for t in tokens:
            print(f"{t[0]:<20} -> {t[1]}")
            if t[0] == 'DESCONOCIDO':
                print(f"  [!] ERROR LÉXICO: Caracter no reconocido '{t[1]}'")
                
    except Exception as e:
        print(f"\n[Error de Lectura]: {e}")

if __name__ == "__main__":
    main()
