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
        def procesar_grupo(llave):
            items = sorted(self.rules.get(llave, []), key=len, reverse=True)
            return '|'.join([re.escape(i) for i in items]) if items else '(?!)'
            
        regex_parts = [
            r'(?P<NUMERO_ENTERO>\d+)',
            r'(?P<OP_RELACIONAL>' + procesar_grupo('op_relacionales') + r')',
            r'(?P<OP_LOGICO>' + procesar_grupo('op_logicos') + r')',
            r'(?P<OP_ARITMETICO>' + procesar_grupo('op_aritmeticos') + r')',
            r'(?P<SIMB_ESPECIAL>' + procesar_grupo('simbolos_especiales') + r')',
            r'(?P<IDENTIFICADOR>[a-zA-Z_][a-zA-Z0-9_]*)',
            r'(?P<ESPACIO>[\s\t\n]+)',
            r'(?P<DESCONOCIDO>.)'
        ]
        self.token_regex = re.compile('|'.join(regex_parts))

    def tokenize(self, source_code: str):
        tokens = []
        for match in self.token_regex.finditer(source_code):
            tipo = match.lastgroup
            valor = match.group(tipo)
            
            if tipo == 'ESPACIO':
                continue
                
            if tipo == 'IDENTIFICADOR':
                palabras = self.rules.get('palabras_reservadas', [])
                if valor in palabras or (self.rules.get('lenguaje') == 'SQL' and valor.upper() in palabras):
                    tipo = 'PALABRA_RESERVADA'
                
            tokens.append((tipo, valor))
        return tokens
