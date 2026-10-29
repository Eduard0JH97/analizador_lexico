import pathlib
from core.lexer import Lexer
from core.parser import Parser
from utils.file_reader import leer_archivo

def main():
    print("--- Analizador Léxico y Sintáctico ---")
    rules_path = pathlib.Path("rules/c_rules.json")
    
    if not rules_path.exists():
        print("Error: No se encontró c_rules.json.")
        return
        
    lexer = Lexer(str(rules_path))
    ruta_txt = input("Ingrese la ruta del archivo fuente (.txt): ")
    
    try:
        codigo_fuente = leer_archivo(ruta_txt)
        print("\n[ FASE 1: Análisis Léxico ]")
        tokens = lexer.tokenize(codigo_fuente)
        
        hay_errores_lexicos = False
        for t in tokens:
            if t[0] != 'ESPACIO':
                print(f"{t[0]:<20} -> {t[1]}")
            if t[0] == 'DESCONOCIDO':
                print(f"  [!] ERROR LÉXICO: Caracter no reconocido '{t[1]}'")
                hay_errores_lexicos = True
                
        if hay_errores_lexicos:
            print("\nSe detiene el analisis por errores lexicos.")
            return
            
        print("\n[ FASE 2: Análisis Sintáctico ]")
        parser = Parser(tokens)
        errores_sintacticos = parser.parse()
        
        if not errores_sintacticos:
            print("El analisis sintactico termino SIN ERRORES. El codigo es correcto.")
        else:
            for error in errores_sintacticos:
                print(f"[!] {error}")
                
    except Exception as e:
        print(f"\n[Error]: {e}")

if __name__ == "__main__":
    main()
