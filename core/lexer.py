import json
import pathlib
import re

class Lexer:
    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)
        self._build_regex()
        
    def _load_rules(self, path: str) -> dict:
        file_path = pathlib.Path(path)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def _build_regex(self):
        # Ordenar símbolos de mayor a menor longitud para match exacto (ej. '==' antes que '=')
        simbolos = sorted(self.rules.get('simbolos', []), key=len, reverse=True)
        escaped_simbolos = [re.escape(s) for s in simbolos]
        
        # Ensamblar las partes de la expresión regular dinámica
        regex_parts = [
            r'(?P<NUMERO>\d+)',
            r'(?P<SIMBOLO>' + '|'.join(escaped_simbolos) + r')',
            r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)',
            r'(?P<ESPACIO>[\s\t\n]+)',
            r'(?P<DESCONOCIDO>.)' # Captura cualquier caracter que no encaje
        ]
        self.token_regex = re.compile('|'.join(regex_parts))

    def tokenize(self, source_code: str):
        tokens = []
        for match in self.token_regex.finditer(source_code):
            tipo = match.lastgroup
            valor = match.group(tipo)
            
            if tipo == 'ESPACIO':
                continue
                
            # Validar si un ID es en realidad una palabra reservada del JSON
            if tipo == 'ID' and valor in self.rules.get('palabras_reservadas', []):
                tipo = 'RESERVADA'
                
            tokens.append((tipo, valor))
        return tokens
