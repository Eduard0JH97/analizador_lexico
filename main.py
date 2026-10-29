import sys
import pathlib
from core.lexer import Lexer

def main():
    print("Iniciando Analizador Multilenguaje...")
    # Ejemplo de instanciación dinámica
    rules_path = pathlib.Path("rules/c_rules.json")
    if rules_path.exists():
        lexer = Lexer(str(rules_path))
        lexer.tokenize("int main() {}")

if __name__ == "__main__":
    main()
