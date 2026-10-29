import pathlib

def leer_archivo(ruta: str) -> str:
    ruta_obj = pathlib.Path(ruta)
    if not ruta_obj.exists():
        raise FileNotFoundError(f"El archivo no existe en la ruta: {ruta}")
    if ruta_obj.suffix != '.txt':
        raise ValueError("El archivo debe tener extensión .txt")
        
    with open(ruta_obj, 'r', encoding='utf-8') as f:
        return f.read()
