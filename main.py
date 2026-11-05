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
        print("\n--- Codigo Fuente a Analizar ---")
        print("-" * 45)
        print(codigo.strip())
        print("-" * 45)
        print("\n--- [1] Analisis Lexico ---")
        tokens = lexer.tokenize(codigo)

        errores_lexicos = 0
        for tipo, valor, linea, columna in tokens:
            if tipo != "ESPACIO":
                pos_str = f"[Línea {linea}, Col {columna}]"
                print(f"{pos_str:<22} {tipo:<20} -> {valor}")
            if tipo == "DESCONOCIDO":
                print(f"  [!] ERROR LEXICO [Línea {linea}, Col {columna}]: Caracter no admitido '{valor}'")
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

def verificacion_rapida():
    pruebas = [
        ("C", "rules/c_rules.json", "tests/c_valido.txt"),
        ("Java", "rules/java_rules.json", "tests/java_valido.txt"),
        ("SQL", "rules/sql_rules.json", "tests/sql_valido.txt"),
        ("Python", "rules/python_rules.json", "tests/python_valido.txt")
    ]

    print("\n" + "=" * 80)
    print("                    VERIFICACIÓN RÁPIDA DE PRUEBAS BASE")
    print("=" * 80)
    print(f"{'Lenguaje':<10} {'Archivo':<28} {'Tokens':<10} {'Estado':<10} {'Errores Detectados'}")
    print("-" * 80)

    total_pasadas = 0
    detalles_fallos = []

    for lenguaje, ruta_reglas, ruta_txt in pruebas:
        ruta_archivo = pathlib.Path(ruta_txt)
        if not ruta_archivo.exists():
            alt = ruta_txt.replace("_valido.txt", "_correcto.txt")
            if pathlib.Path(alt).exists():
                ruta_archivo = pathlib.Path(alt)
                ruta_txt = alt

        if not pathlib.Path(ruta_reglas).exists():
            print(f"{lenguaje:<10} {ruta_txt:<28} {'N/A':<10} {'FALLÓ':<10} Reglas no encontradas ({ruta_reglas})")
            detalles_fallos.append((lenguaje, [f"No existe el archivo de reglas: {ruta_reglas}"]))
            continue

        if not ruta_archivo.exists():
            print(f"{lenguaje:<10} {ruta_txt:<28} {'N/A':<10} {'FALLÓ':<10} Archivo no encontrado ({ruta_txt})")
            detalles_fallos.append((lenguaje, [f"No existe el archivo de prueba: {ruta_txt}"]))
            continue

        try:
            codigo = leer_archivo(str(ruta_archivo))
            lexer = Lexer(ruta_reglas)
            tokens = lexer.tokenize(codigo)

            tokens_utiles = [t for t in tokens if t[0] != "ESPACIO"]
            cant_tokens = len(tokens_utiles)

            errores_lex = [
                f"[Línea {linea}, Col {col}] Carácter no admitido '{val}'"
                for tipo, val, linea, col in tokens
                if tipo == "DESCONOCIDO"
            ]

            errores_sint = []
            if not errores_lex:
                parser = Parser(tokens, lenguaje=lenguaje)
                errores_sint = parser.parse()

            total_errores = errores_lex + errores_sint

            if not total_errores:
                estado = "PASÓ"
                resumen_err = "0 errores"
                total_pasadas += 1
            else:
                estado = "FALLÓ"
                resumen_err = f"{len(total_errores)} error(es)"
                detalles_fallos.append((lenguaje, total_errores))

            print(f"{lenguaje:<10} {ruta_txt:<28} {cant_tokens:<10} {estado:<10} {resumen_err}")

        except Exception as e:
            estado = "FALLÓ"
            print(f"{lenguaje:<10} {ruta_txt:<28} {'-':<10} {estado:<10} Excepción: {e}")
            detalles_fallos.append((lenguaje, [str(e)]))

    print("-" * 80)
    print(f"Resultado: {total_pasadas}/{len(pruebas)} pruebas superadas.")
    if detalles_fallos:
        print("\n[!] Detalle de errores detectados:")
        for lang, errs in detalles_fallos:
            print(f"  * {lang}:")
            for err in errs:
                print(f"      - {err}")
    print("=" * 80)

def main():
    while True:
        print("\n" + "=" * 45)
        print("         ANALIZADOR MULTILENGUAJE")
        print("=" * 45)
        print("1. C")
        print("2. Java")
        print("3. SQL")
        print("4. Python")
        print("5. Verificación Rápida (Ejecutar pruebas base)")
        print("0. Salir del programa")
        
        opcion = input("Seleccione una opcion (0-5): ").strip()
        
        if opcion == "0":
            print("\nFinalizando ejecucion del programa. ¡Hasta pronto!")
            break

        if opcion == "5":
            verificacion_rapida()
            input("\nPresione [ENTER] para continuar...")
            continue
            
        if opcion not in OPCIONES_LENGUAJES:
            print("\n[!] Opcion no valida. Seleccione un numero del 0 al 5.")
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
