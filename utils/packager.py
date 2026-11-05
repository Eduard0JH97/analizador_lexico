import zipfile
from pathlib import Path

# Configuracion de directorios y archivo de salida
ROOT_DIR = Path(__file__).resolve().parent.parent
ZIP_NAME = 'analizador_lexico_entrega.zip'
OUTPUT_ZIP = ROOT_DIR / ZIP_NAME

# Carpetas y archivos a excluir de forma estricta
EXCLUDED_DIRS = {'.git', '.antigravity', '.vscode', '__pycache__'}
EXCLUDED_FILES = {
    '.cursorrules',
    'a_lexico.md',
    'autómatas.md',
    'automatas.md',
}

# Elementos a incluir explicitamente
EXPLICIT_TARGETS = [
    'core',
    'rules',
    'tests',
    'utils',
    'ejecutar_analizador.bat',
    'main.py',
    'README.md',
]


def collect_files():
  files_to_pack = []
  for target_name in EXPLICIT_TARGETS:
    target_path = ROOT_DIR / target_name
    if not target_path.exists():
      continue

    if target_path.is_file():
      if (
          target_path.name not in EXCLUDED_FILES
          and not target_path.name.endswith('.pyc')
          and not target_path.name.endswith('.zip')
      ):
        files_to_pack.append(target_path)
    elif target_path.is_dir():
      for file_path in target_path.rglob('*'):
        if file_path.is_file():
          # Descartar si alguna carpeta padre esta en la lista de exclusion
          if any(part in EXCLUDED_DIRS for part in file_path.parts):
            continue
          # Descartar archivos excluidos o extensiones no deseadas
          if file_path.name in EXCLUDED_FILES:
            continue
          if file_path.suffix.lower() in ['.pyc', '.zip']:
            continue
          files_to_pack.append(file_path)

  # Ordenar de forma determinista
  files_to_pack.sort(key=lambda p: str(p.relative_to(ROOT_DIR)).lower())
  return files_to_pack


def create_package():
  files_to_pack = collect_files()

  # Eliminar archivo zip anterior si existe
  if OUTPUT_ZIP.exists():
    OUTPUT_ZIP.unlink()

  print(f'Iniciando empaquetado seguro en: {OUTPUT_ZIP.name}\n')
  print('=' * 65)
  print('LISTADO COMPLETO DE ARCHIVOS EMPAQUETADOS (AUDITORIA):')
  print('=' * 65)

  with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_path in files_to_pack:
      rel_path = file_path.relative_to(ROOT_DIR).as_posix()
      zipf.write(file_path, arcname=rel_path)
      print(f' [+] {rel_path}')

  print('=' * 65)
  print(f'Total de archivos empaquetados: {len(files_to_pack)}')
  print(f'Archivo generado exitosamente: {OUTPUT_ZIP.name}')
  print(f'Tamano del archivo ZIP: {OUTPUT_ZIP.stat().st_size} bytes\n')


if __name__ == '__main__':
  create_package()
