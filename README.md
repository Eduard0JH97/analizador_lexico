# Analizador Léxico y Sintáctico Multilenguaje

Programa desarrollado en Python capaz de analizar componentes léxicos y diagnosticar errores sintácticos en código fuente de diferentes lenguajes (C, Java, SQL y Python) a partir de archivos externos `.txt`.

---

## 1. Componentes Léxicos Identificados
El analizador clasifica de forma dinámica los componentes en base a configuraciones JSON en `rules/`:
* **Palabras reservadas**: Según el lenguaje seleccionado (`int`, `if`, `SELECT`, `def`, etc.).
* **Identificadores**: Nombres de variables, funciones o tablas (`[a-zA-Z_][a-zA-Z0-9_]*`).
* **Números enteros**: Secuencias de dígitos (`\d+`).
* **Operadores**:
  * Aritméticos: `+`, `-`, `*`, `/`, etc.
  * Relacionales: `>`, `<`, `>=`, `<=`, `==`, `!=`, `<>`.
  * Lógicos: `&&`, `||`, `!`, `AND`, `OR`, `not`.
* **Símbolos especiales**: `;`, `{`, `}`, `(`, `)`, `:`, `=`, etc.

---

## 2. Reglas de Producción Sintáctica (Notación BNF)

### Gramática para C y Java:
1. **Declaración de Variables**:
   `<Declaracion> ::= <Tipo_Dato> <Identificador> [ "=" (<Identificador> | <Numero>) ] ";"`
2. **Asignación de Variables**:
   `<Asignacion>  ::= <Identificador> "=" (<Identificador> | <Numero>) [ <Op_Aritmetico> (<Identificador> | <Numero>) ] ";"`
3. **Sentencia Condicional (If)**:
   `<If_Stmt>     ::= "if" "(" <Condicion> ")" "{" <Cuerpo> "}"`

### Gramática para SQL:
1. **Consulta Simple**:
   `<Select_Stmt> ::= "SELECT" ("*" | <Identificador>) "FROM" <Identificador> [ "WHERE" <Identificador> <Op_Relacional> (<Numero> | <Identificador>) ] ";"`

### Gramática para Python:
1. **Definición de Función**:
   `<Def_Stmt>    ::= "def" <Identificador> "(" ")" ":"`
2. **Estructura If**:
   `<If_Stmt>     ::= "if" <Condicion> ":"`

---

## 3. Instrucciones de Ejecución
1. Abrir terminal en la raíz del proyecto.
2. Ejecutar:
   ```bash
   python main.py
   ```
3. Seleccionar el lenguaje deseado del menú interactivo (1 a 4).
4. Proporcionar la ruta relativa del archivo `.txt` a evaluar (ejemplos listos en carpeta `tests/`):
   * `tests/c_valido.txt` / `tests/c_error.txt`
   * `tests/java_valido.txt` / `tests/java_error.txt`
   * `tests/sql_valido.txt` / `tests/sql_error.txt`
   * `tests/python_valido.txt` / `tests/python_error.txt`

