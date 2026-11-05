class Parser:
    def __init__(self, tokens, lenguaje="C"):
        self.tokens = [t for t in tokens if t[0] not in ['DESCONOCIDO', 'ESPACIO']]
        self.pos = 0
        self.errores = []
        self.lenguaje = lenguaje

    def current_token(self):
        if self.pos < len(self.tokens):
            tok = self.tokens[self.pos]
            if len(tok) >= 4:
                return tok[0], tok[1], tok[2], tok[3]
            elif len(tok) == 2:
                return tok[0], tok[1], 0, 0
            elif len(tok) == 3:
                return tok[0], tok[1], tok[2], 0
        if self.tokens:
            last_tok = self.tokens[-1]
            last_line = last_tok[2] if len(last_tok) >= 4 else 0
            last_col = last_tok[3] if len(last_tok) >= 4 else 0
            return ("EOF", "", last_line, last_col)
        return ("EOF", "", 0, 0)

    def advance(self):
        self.pos += 1

    def match(self, expected_type, expected_val=None):
        token_type, token_val, line, col = self.current_token()
        val_matches = (expected_val is None) or (
            token_val.upper() == expected_val.upper() if self.lenguaje == "SQL" else token_val == expected_val
        )
        if token_type == expected_type and val_matches:
            self.advance()
            return True
        return False

    def expect(self, expected_type, expected_val=None, context=""):
        token_type, token_val, line, col = self.current_token()
        val_matches = (expected_val is None) or (
            token_val.upper() == expected_val.upper() if self.lenguaje == "SQL" else token_val == expected_val
        )
        if token_type == expected_type and val_matches:
            self.advance()
            return True
        else:
            expected_str = expected_val if expected_val else expected_type
            found_str = token_val if token_val else token_type
            context_part = f" {context}" if context else ""
            self.errores.append(f"[Linea {line}, Columna {col}] Error Sintactico{context_part}: Se esperaba '{expected_str}', pero se encontro '{found_str}'")
            return False

    def parse(self):
        if self.lenguaje == "SQL":
            return self.parse_sql()
        elif self.lenguaje == "Python":
            return self.parse_python()
        else:
            return self.parse_c_java()

    # Gramatica C / Java
    def parse_c_java(self):
        while self.current_token()[0] != "EOF":
            token_type, token_val, line, col = self.current_token()
            if token_type == "PALABRA_RESERVADA" and token_val in ["int", "float", "double", "String", "boolean"]:
                self.advance()
                if self.expect("IDENTIFICADOR", context="en declaracion de variable"):
                    if self.match("SIMB_ESPECIAL", "="):
                        _, _, cur_l, cur_c = self.current_token()
                        if not (self.match("NUMERO_ENTERO") or self.match("IDENTIFICADOR")):
                            self.errores.append(f"[Linea {cur_l}, Columna {cur_c}] Error Sintactico: Se esperaba un valor despues de '='")
                    self.expect("SIMB_ESPECIAL", ";", context="al final de la declaracion")
            elif token_type == "IDENTIFICADOR":
                self.advance()
                if self.expect("SIMB_ESPECIAL", "=", context="en asignacion"):
                    _, _, cur_l, cur_c = self.current_token()
                    if not (self.match("IDENTIFICADOR") or self.match("NUMERO_ENTERO")):
                        self.errores.append(f"[Linea {cur_l}, Columna {cur_c}] Error Sintactico: Se esperaba valor a asignar")
                    self.expect("SIMB_ESPECIAL", ";", context="al final de asignacion")
            elif token_type == "PALABRA_RESERVADA" and token_val == "if":
                self.advance()
                self.expect("SIMB_ESPECIAL", "(", context="abriendo condicion if")
                while self.current_token()[0] != "EOF" and self.current_token()[1] != ")":
                    self.advance()
                self.expect("SIMB_ESPECIAL", ")", context="cerrando condicion if")
                self.expect("SIMB_ESPECIAL", "{", context="abriendo bloque if")
                while self.current_token()[0] != "EOF" and self.current_token()[1] != "}":
                    self.advance()
                self.expect("SIMB_ESPECIAL", "}", context="cerrando bloque if")
            else:
                self.advance()
        return self.errores

    # Gramatica SQL (Instrucciones: SELECT ... FROM ... [WHERE ...];)
    def parse_sql(self):
        while self.current_token()[0] != "EOF":
            token_type, token_val, line, col = self.current_token()
            if token_type == "PALABRA_RESERVADA" and token_val.upper() == "SELECT":
                self.advance()
                # Acepta comodín * (ya sea catalogado como OP_ARITMETICO o SIMB_ESPECIAL) o un IDENTIFICADOR
                _, cur_val, cur_l, cur_c = self.current_token()
                cur_type = self.current_token()[0]
                if cur_val == "*" or cur_type == "IDENTIFICADOR":
                    self.advance()
                else:
                    self.errores.append(f"[Linea {cur_l}, Columna {cur_c}] Error Sintactico en SELECT: Se esperaba columna o '*'")
                
                self.expect("PALABRA_RESERVADA", "FROM", context="en consulta SELECT")
                self.expect("IDENTIFICADOR", context="especificando tabla en FROM")
                
                # Clausula WHERE opcional
                token_type, token_val, line, col = self.current_token()
                if token_type == "PALABRA_RESERVADA" and token_val.upper() == "WHERE":
                    self.advance()
                    self.expect("IDENTIFICADOR", context="en clausula WHERE")
                    # Consumir operador relacional o símbolo (=, ==, <>, !=, etc.)
                    while self.current_token()[0] in ["OP_RELACIONAL", "SIMB_ESPECIAL"] and self.current_token()[1] in ["=", "==", "!=", "<>", ">", "<", ">=", "<="]:
                        self.advance()
                    _, _, cur_l, cur_c = self.current_token()
                    if not (self.match("NUMERO_ENTERO") or self.match("IDENTIFICADOR")):
                        self.errores.append(f"[Linea {cur_l}, Columna {cur_c}] Error Sintactico: Se esperaba un valor o identificador de comparacion en WHERE")
                        
                self.expect("SIMB_ESPECIAL", ";", context="al final de la sentencia SQL")
            else:
                self.advance()
        return self.errores

    # Gramatica Python (Asignacion, def, if con dos puntos)
    def parse_python(self):
        while self.current_token()[0] != "EOF":
            token_type, token_val, line, col = self.current_token()
            if token_type == "PALABRA_RESERVADA" and token_val == "def":
                self.advance()
                self.expect("IDENTIFICADOR", context="en nombre de funcion def")
                self.expect("SIMB_ESPECIAL", "(", context="abriendo parametros def")
                self.expect("SIMB_ESPECIAL", ")", context="cerrando parametros def")
                self.expect("SIMB_ESPECIAL", ":", context="al final de cabecera def")
            elif token_type == "PALABRA_RESERVADA" and token_val == "if":
                self.advance()
                while self.current_token()[0] != "EOF" and self.current_token()[1] != ":":
                    self.advance()
                self.expect("SIMB_ESPECIAL", ":", context="al final de condicion if")
            elif token_type == "IDENTIFICADOR":
                self.advance()
                if self.expect("SIMB_ESPECIAL", "=", context="en asignacion"):
                    _, _, cur_l, cur_c = self.current_token()
                    if not (self.match("IDENTIFICADOR") or self.match("NUMERO_ENTERO")):
                        self.errores.append(f"[Linea {cur_l}, Columna {cur_c}] Error Sintactico: Se esperaba valor a asignar")
            else:
                self.advance()
        return self.errores
