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

def seleccionar_archivo_fuente() -> str:
    directorio_tests = pathlib.Path("tests")
    archivos_txt = sorted(list(directorio_tests.glob("*.txt"))) if directorio_tests.exists() else []

    while True:
        print("\n--- Seleccion de Archivo Fuente (.txt) ---")
        if archivos_txt:
            print("Archivos disponibles en carpeta 'tests/':")
            for i, archivo in enumerate(archivos_txt, start=1):
                print(f"  {i}. {archivo.name}")
            print(f"  {len(archivos_txt) + 1}. Ingresar otra ruta manualmente")
            print(f"  0. Cancelar y regresar al menu de lenguajes")
            
            opcion = input(f"Seleccione un archivo (0-{len(archivos_txt) + 1}): ").strip()
            
            if opcion == "0":
                return ""
                
            if opcion.isdigit():
                indice = int(opcion)
                if 1 <= indice <= len(archivos_txt):
                    return str(archivos_txt[indice - 1])
                elif indice == len(archivos_txt) + 1:
                    ruta = input("Ingrese la ruta del archivo fuente (.txt): ").strip()
                    if pathlib.Path(ruta).is_file():
                        return ruta
                    print(f"\n[!] Ruta invalida: '{ruta}' no es un archivo valido o no existe. Intente nuevamente.")
                    continue
            print("\n[!] Opcion invalida. Intente de nuevo.")
        else:
            ruta = input("Ingrese la ruta del archivo fuente (.txt) (o '0' para volver): ").strip()
            if ruta == "0":
                return ""
            if pathlib.Path(ruta).is_file():
                return ruta
            print(f"\n[!] Ruta invalida: '{ruta}' no existe. Intente de nuevo.")

def analizar_archivo(ruta_txt: str, lexer: Lexer, lenguaje: str):
    try:
        codigo = leer_archivo(ruta_txt)
        print(f"\n[+] Analizando archivo: {ruta_txt}")
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
        print(f"\n[Error durante el analisis]: {e}")

def main():
    while True:
        print("\n" + "=" * 45)
        print("         ANALIZADOR MULTILENGUAJE")
        print("=" * 45)
        print("1. C")
        print("2. Java")
        print("3. SQL")
        print("4. Python")
        print("0. Salir del programa")
        
        opcion = input("Seleccione una opcion (0-4): ").strip()
        
        if opcion == "0":
            print("\nFinalizando ejecucion del programa. ¡Hasta pronto!")
            break
            
        if opcion not in OPCIONES_LENGUAJES:
            print("\n[!] Opcion no valida. Seleccione un numero del 0 al 4.")
            continue

        lenguaje, ruta_reglas = OPCIONES_LENGUAJES[opcion]
        reglas_path = pathlib.Path(ruta_reglas)
        if not reglas_path.exists():
            print(f"\n[!] Error: No existe el archivo de configuracion {ruta_reglas}")
            continue

        lexer = Lexer(str(reglas_path))
        print(f"\n--> Modo activo: {lenguaje}")

        ruta_txt = seleccionar_archivo_fuente()
        if not ruta_txt:
            continue

        analizar_archivo(ruta_txt, lexer, lenguaje)

        input("\nPresione [ENTER] para continuar...")

if __name__ == "__main__":
    main()
