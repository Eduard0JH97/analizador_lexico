import pathlib
from core.lexer import Lexer

def main():
    print("--- Analizador Léxico Multilenguaje ---")
    rules_path = pathlib.Path("rules/c_rules.json")
    
    if rules_path.exists():
        lexer = Lexer(str(rules_path))
        codigo_prueba = "int total = 15; \n if (total >= 10) { return 1; }"
        
        print(f"\nAnalizando código fuente en memoria:\n{codigo_prueba}\n")
        tokens = lexer.tokenize(codigo_prueba)
        
        print("Tokens identificados:")
        for t in tokens:
            print(f"[{t[0]}] -> {t[1]}")
    else:
        print("Error: No se encontró el archivo de reglas.")

if __name__ == "__main__":
    main()
