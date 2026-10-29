import pathlib
from core.lexer import Lexer
from core.parser import Parser
from utils.file_reader import leer_archivo

OPCIONES_LENGUAJES = {
    "1": ("C", "rules/c_rules.json"),
    "2": ("Java", "rules/java_rules.json"),
    "3": ("SQL", "rules/sql_rules.json"),
    "4": ("Python", "rules/python_rules.json")
}

def main():
    print("=== Analizador Multilenguaje ===")
    print("Seleccione el lenguaje a analizar:")
    print("1. C")
    print("2. Java")
    print("3. SQL")
    print("4. Python")
    
    opcion = input("Opcion (1-4): ").strip()
    if opcion not in OPCIONES_LENGUAJES:
        print("Opcion no valida.")
        return

    lenguaje, ruta_reglas = OPCIONES_LENGUAJES[opcion]
    reglas_path = pathlib.Path(ruta_reglas)
    if not reglas_path.exists():
        print(f"Error: No existe el archivo de configuracion {ruta_reglas}")
        return

    lexer = Lexer(str(reglas_path))
    print(f"\nModo activo: {lenguaje}")

    ruta_txt = input("Ingrese la ruta del archivo fuente (.txt): ").strip()

    try:
        codigo = leer_archivo(ruta_txt)
        print("\n--- [1] Analisis Lexico ---")
        tokens = lexer.tokenize(codigo)

        errores_lexicos = 0
        for tipo, valor in tokens:
            if tipo != "ESPACIO":
                print(f"{tipo:<20} -> {valor}")
            if tipo == "DESCONOCIDO":
                print(f"  [!] ERROR LEXICO: Caracter no admitido '{valor}'")
                errores_lexicos += 1

        if errores_lexicos > 0:
            print(f"\nSe detuvo el analisis: se encontraron {errores_lexicos} error(es) lexicos.")
            return

        print("\n--- [2] Analisis Sintactico ---")
        parser = Parser(tokens, lenguaje=lenguaje)
        errores_sintacticos = parser.parse()

        if not errores_sintacticos:
            print("Analisis sintactico finalizado con EXITO (0 errores).")
        else:
            for err in errores_sintacticos:
                print(f"[!] {err}")

    except Exception as e:
        print(f"\n[Error]: {e}")

if __name__ == "__main__":
    main()
