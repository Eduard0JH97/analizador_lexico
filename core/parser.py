class Parser:
    def __init__(self, tokens, lenguaje="C"):
        self.tokens = [t for t in tokens if t[0] not in ['DESCONOCIDO', 'ESPACIO']]
        self.pos = 0
        self.errores = []
        self.lenguaje = lenguaje

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("EOF", "")

    def advance(self):
        self.pos += 1

    def match(self, expected_type, expected_val=None):
        token_type, token_val = self.current_token()
        val_matches = (expected_val is None) or (
            token_val.upper() == expected_val.upper() if self.lenguaje == "SQL" else token_val == expected_val
        )
        if token_type == expected_type and val_matches:
            self.advance()
            return True
        return False

    def expect(self, expected_type, expected_val=None, context=""):
        token_type, token_val = self.current_token()
        val_matches = (expected_val is None) or (
            token_val.upper() == expected_val.upper() if self.lenguaje == "SQL" else token_val == expected_val
        )
        if token_type == expected_type and val_matches:
            self.advance()
            return True
        else:
            expected_str = expected_val if expected_val else expected_type
            found_str = token_val if token_val else token_type
            self.errores.append(f"Error Sintactico {context}: Se esperaba '{expected_str}', pero se encontro '{found_str}'")
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
            token_type, token_val = self.current_token()
            if token_type == "PALABRA_RESERVADA" and token_val in ["int", "float", "double", "String", "boolean"]:
                self.advance()
                if self.expect("IDENTIFICADOR", context="en declaracion de variable"):
                    if self.match("SIMB_ESPECIAL", "="):
                        if not (self.match("NUMERO_ENTERO") or self.match("IDENTIFICADOR")):
                            self.errores.append("Error Sintactico: Se esperaba un valor despues de '='")
                    self.expect("SIMB_ESPECIAL", ";", context="al final de la declaracion")
            elif token_type == "IDENTIFICADOR":
                self.advance()
                if self.expect("SIMB_ESPECIAL", "=", context="en asignacion"):
                    if not (self.match("IDENTIFICADOR") or self.match("NUMERO_ENTERO")):
                        self.errores.append("Error Sintactico: Se esperaba valor a asignar")
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
            token_type, token_val = self.current_token()
            if token_type == "PALABRA_RESERVADA" and token_val.upper() == "SELECT":
                self.advance()
                if not (self.match("SIMB_ESPECIAL", "*") or self.match("IDENTIFICADOR")):
                    self.errores.append("Error Sintactico en SELECT: Se esperaba columna o '*'")
                self.expect("PALABRA_RESERVADA", "FROM", context="en consulta SELECT")
                self.expect("IDENTIFICADOR", context="especificando tabla en FROM")
                if self.match("PALABRA_RESERVADA", "WHERE"):
                    self.expect("IDENTIFICADOR", context="en clausula WHERE")
                    if self.current_token()[0] in ["OP_RELACIONAL", "SIMB_ESPECIAL"]:
                        self.advance()
                    self.match("NUMERO_ENTERO") or self.match("IDENTIFICADOR")
                self.expect("SIMB_ESPECIAL", ";", context="al final de la sentencia SQL")
            else:
                self.advance()
        return self.errores

    # Gramatica Python (Asignacion, def, if con dos puntos)
    def parse_python(self):
        while self.current_token()[0] != "EOF":
            token_type, token_val = self.current_token()
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
                    if not (self.match("IDENTIFICADOR") or self.match("NUMERO_ENTERO")):
                        self.errores.append("Error Sintactico: Se esperaba valor a asignar")
            else:
                self.advance()
        return self.errores
