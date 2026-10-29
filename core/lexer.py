import json
import pathlib
import re

class Lexer:
    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)
        
    def _load_rules(self, path: str) -> dict:
        file_path = pathlib.Path(path)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def tokenize(self, source_code: str):
        # TODO: Implementar la lógica de escaneo dinámico con Regex
        print(f"Lenguaje configurado: {self.rules.get('lenguaje')}")
        pass

