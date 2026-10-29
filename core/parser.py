class Parser:
    def __init__(self, tokens):
        # Filtramos tokens DESCONOCIDOS y ESPACIOS (si los hubiera)
        self.tokens = [t for t in tokens if t[0] not in ['DESCONOCIDO', 'ESPACIO']]
        self.pos = 0
        self.errores = []

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("EOF", "")

    def advance(self):
        self.pos += 1

    def match(self, expected_type, expected_val=None):
        token_type, token_val = self.current_token()
        if token_type == expected_type and (expected_val is None or token_val == expected_val):
            self.advance()
            return True
        return False

    def expect(self, expected_type, expected_val=None, context=""):
        token_type, token_val = self.current_token()
        if token_type == expected_type and (expected_val is None or token_val == expected_val):
            self.advance()
            return True
        else:
            expected_str = expected_val if expected_val else expected_type
            found_str = token_val if token_val else token_type
            self.errores.append(f"Error Sintactico {context}: Se esperaba '{expected_str}', pero se encontro '{found_str}'")
            return False

    def parse(self):
        while self.current_token()[0] != "EOF":
            token_type, token_val = self.current_token()
            
            if token_type == "PALABRA_RESERVADA" and token_val in ["int", "float"]:
                self.parse_declaracion()
            elif token_type == "IDENTIFICADOR":
                self.parse_asignacion()
            elif token_type == "PALABRA_RESERVADA" and token_val == "if":
                self.parse_if()
            else:
                self.advance() # Avanzar para evitar ciclos infinitos con tokens sueltos
                
        return self.errores

    # REGLA 1: Declaración (ej. int x = 5;)
    def parse_declaracion(self):
        self.advance() # consumimos el tipo de dato
        if self.expect("IDENTIFICADOR", context="en declaracion de variable"):
            if self.match("SIMB_ESPECIAL", "="):
                if not (self.match("NUMERO_ENTERO") or self.match("IDENTIFICADOR")):
                    self.errores.append("Error Sintactico: Se esperaba un valor despues de '='")
            self.expect("SIMB_ESPECIAL", ";", context="al final de la declaracion")

    # REGLA 2: Asignación (ej. x = y * 2;)
    def parse_asignacion(self):
        self.advance() # consumimos el ID
        if self.expect("SIMB_ESPECIAL", "=", context="en asignacion"):
            if self.match("IDENTIFICADOR") or self.match("NUMERO_ENTERO"):
                # Opcional: operador aritmético y otro valor
                if self.current_token()[0] in ["OP_ARITMETICO"]:
                    self.advance()
                    if not (self.match("IDENTIFICADOR") or self.match("NUMERO_ENTERO")):
                        self.errores.append("Error Sintactico: Expresion matematica incompleta")
            else:
                self.errores.append("Error Sintactico: Se esperaba un valor a asignar")
            self.expect("SIMB_ESPECIAL", ";", context="al final de la instruccion")

    # REGLA 3: Estructura If (ej. if (x > 5) { ... })
    def parse_if(self):
        self.advance() # consumimos 'if'
        self.expect("SIMB_ESPECIAL", "(", context="despues de 'if'")
        
        # Saltamos hasta cerrar el paréntesis (condición simple)
        while self.current_token()[0] != "EOF" and self.current_token()[1] != ")":
            self.advance()
            
        self.expect("SIMB_ESPECIAL", ")", context="cerrando condicion 'if'")
        self.expect("SIMB_ESPECIAL", "{", context="abriendo bloque 'if'")
        
        # Procesamos el interior recursivamente
        while self.current_token()[0] != "EOF" and self.current_token()[1] != "}":
            token_type, token_val = self.current_token()
            if token_type == "IDENTIFICADOR":
                self.parse_asignacion()
            elif token_type == "PALABRA_RESERVADA" and token_val in ["int", "float"]:
                self.parse_declaracion()
            elif token_type == "PALABRA_RESERVADA" and token_val == "if":
                self.parse_if()
            else:
                self.advance()
                
        self.expect("SIMB_ESPECIAL", "}", context="cerrando bloque 'if'")
