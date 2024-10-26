from enum import Enum, auto
from typing import List, Optional, Any, Dict
from dataclasses import dataclass
import os

# Token types
class TokenType(Enum):
    # Keywords
    PROGRAM = auto()
    BEGIN = auto()
    END = auto()
    FUNC = auto()
    RETURN = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    DO = auto()
    IN = auto()
    CLASS = auto()
    TRY = auto()
    EXCEPT = auto()
    USE = auto()
    DISPLAY = auto()
    
    # Types
    NUM = auto()
    STR = auto()
    BOOL = auto()
    LIST = auto()
    
    # Literals
    NUMBER = auto()
    STRING = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    
    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    
    # Other
    IDENTIFIER = auto()
    COMMENT = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source else None
        
        # Keywords mapping
        self.keywords = {
            'PROGRAM': TokenType.PROGRAM,
            'BEGIN': TokenType.BEGIN,
            'END': TokenType.END,
            'func': TokenType.FUNC,
            'return': TokenType.RETURN,
            'if': TokenType.IF,
            'then': TokenType.THEN,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'do': TokenType.DO,
            'in': TokenType.IN,
            'class': TokenType.CLASS,
            'try': TokenType.TRY,
            'except': TokenType.EXCEPT,
            'use': TokenType.USE,
            'display': TokenType.DISPLAY,
            'num': TokenType.NUM,
            'str': TokenType.STR,
            'bool': TokenType.BOOL,
            'list': TokenType.LIST,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE
        }

    def advance(self):
        self.pos += 1
        self.column += 1
        self.current_char = self.source[self.pos] if self.pos < len(self.source) else None
        
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
                self.column = 0
            self.advance()

    def read_number(self) -> Token:
        result = ''
        start_column = self.column
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
            
        return Token(TokenType.NUMBER, result, self.line, start_column)

    def read_identifier(self) -> Token:
        result = ''
        start_column = self.column
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
            
        # Check if it's a keyword
        token_type = self.keywords.get(result, TokenType.IDENTIFIER)
        return Token(token_type, result, self.line, start_column)

    def read_string(self) -> Token:
        result = ''
        start_column = self.column
        self.advance()  # Skip opening quote
        
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
            
        if self.current_char == '"':
            self.advance()  # Skip closing quote
            
        return Token(TokenType.STRING, result, self.line, start_column)

    def read_comment(self) -> Optional[Token]:
        if self.current_char == '#':
            comment = ''
            start_column = self.column
            
            while self.current_char and self.current_char != '\n':
                comment += self.current_char
                self.advance()
                
            return Token(TokenType.COMMENT, comment, self.line, start_column)
        
        elif self.current_char == '/' and self.peek() == '*':
            comment = ''
            start_column = self.column
            self.advance()  # Skip /
            self.advance()  # Skip *
            
            while self.current_char:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # Skip *
                    self.advance()  # Skip /
                    break
                    
                comment += self.current_char
                if self.current_char == '\n':
                    self.line += 1
                    self.column = 0
                self.advance()
                
            return Token(TokenType.COMMENT, comment, self.line, start_column)
            
        return None

    def peek(self) -> Optional[str]:
        peek_pos = self.pos + 1
        return self.source[peek_pos] if peek_pos < len(self.source) else None

    def get_next_token(self) -> Token:
        while self.current_char:
            # Handle whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            # Handle comments
            comment_token = self.read_comment()
            if comment_token:
                return comment_token
                
            # Handle numbers
            if self.current_char.isdigit():
                return self.read_number()
                
            # Handle identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
                
            # Handle strings
            if self.current_char == '"':
                return self.read_string()
                
            # Handle operators and punctuation
            if self.current_char == '+':
                token = Token(TokenType.PLUS, '+', self.line, self.column)
                self.advance()
                return token
                
            if self.current_char == '-':
                token = Token(TokenType.MINUS, '-', self.line, self.column)
                self.advance()
                return token
                
            if self.current_char == '*':
                token = Token(TokenType.MULTIPLY, '*', self.line, self.column)
                self.advance()
                return token
                
            if self.current_char == '/':
                token = Token(TokenType.DIVIDE, '/', self.line, self.column)
                self.advance()
                return token
                
            if self.current_char == '=':
                start_column = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQUALS, '==', self.line, start_column)
                return Token(TokenType.ASSIGN, '=', self.line, start_column)
                
            if self.current_char == '(':
                token = Token(TokenType.LPAREN, '(', self.line, self.column)
                self.advance()
                return token
                
            if self.current_char == ')':
                token = Token(TokenType.RPAREN, ')', self.line, self.column)
                self.advance()
                return token
                
            if self.current_char == '[':
                token = Token(TokenType.LBRACKET, '[', self.line, self.column)
                self.advance()
                return token
                
            if self.current_char == ']':
                token = Token(TokenType.RBRACKET, ']', self.line, self.column)
                self.advance()
                return token
                
            if self.current_char == ',':
                token = Token(TokenType.COMMA, ',', self.line, self.column)
                self.advance()
                return token
                
            if self.current_char == '.':
                token = Token(TokenType.DOT, '.', self.line, self.column)
                self.advance()
                return token
                
            if self.current_char == ':':
                token = Token(TokenType.COLON, ':', self.line, self.column)
                self.advance()
                return token
                
            raise SyntaxError(f"Invalid character '{self.current_char}' at line {self.line}, column {self.column}")
            
        return Token(TokenType.EOF, '', self.line, self.column)

# AST Node classes
class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    description: Optional[str]
    author: Optional[str]
    date: Optional[str]
    body: List[ASTNode]

@dataclass
class FunctionDecl(ASTNode):
    name: str
    params: List[tuple[str, str]]  # [(name, type), ...]
    return_type: Optional[str]
    body: List[ASTNode]

@dataclass
class VariableDecl(ASTNode):
    name: str
    type: Optional[str]
    value: ASTNode

@dataclass
class Assignment(ASTNode):
    target: str
    value: ASTNode

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: TokenType
    right: ASTNode

@dataclass
class Number(ASTNode):
    value: float

@dataclass
class String(ASTNode):
    value: str

@dataclass
class Boolean(ASTNode):
    value: bool

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class Display(ASTNode):
    value: ASTNode

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        
    def error(self, message: str):
        raise SyntaxError(f"{message} at line {self.current_token.line}, column {self.current_token.column}")
        
    def eat(self, token_type: TokenType):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, got {self.current_token.type}")
            
    def parse_program(self) -> Program:
        description = None
        author = None
        date = None
        
        self.eat(TokenType.PROGRAM)
        self.eat(TokenType.BEGIN)
        
        # Parse optional metadata
        while self.current_token.type == TokenType.IDENTIFIER:
            metadata_type = self.current_token.value.upper()
            self.eat(TokenType.IDENTIFIER)
            value = self.current_token.value
            self.eat(TokenType.STRING)
            
            if metadata_type == 'DESCRIPTION':
                description = value
            elif metadata_type == 'AUTHOR':
                author = value
            elif metadata_type == 'DATE':
                date = value
                
        body = []
        while self.current_token.type != TokenType.PROGRAM:
            if self.current_token.type == TokenType.EOF:
                self.error("Unexpected end of file")
                
            statement = self.parse_statement()
            if statement:  # Skip None returns (like comments)
                body.append(statement)
                
        self.eat(TokenType.PROGRAM)
        self.eat(TokenType.END)
        
        return Program(description, author, date, body)
        
    def parse_statement(self) -> Optional[ASTNode]:
        if self.current_token.type == TokenType.COMMENT:
            self.eat(TokenType.COMMENT)
            return None
            
        if self.current_token.type == TokenType.FUNC:
            return self.parse_function()
            
        if self.current_token.type in [TokenType.NUM, TokenType.STR, TokenType.BOOL, TokenType.LIST]:
            return self.parse_variable_declaration()
            
        if self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()
            
        if self.current_token.type == TokenType.DISPLAY:
            return self.parse_display()
            
        self.error(f"Unexpected token {self.current_token.type}")

    def parse_function(self) -> FunctionDecl:
        self.eat(TokenType.FUNC)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # Parse parameters
        self.eat(TokenType.LPAREN)
        params = []
        
        while self.current_token.type != TokenType.RPAREN:
            param_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            if self.current_token.type == TokenType.COLON:
                self.eat(TokenType.COLON)
                param_type = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
            else:
                param_type = None
                
            params.append((param_name, param_type))
            
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                
        self.eat(TokenType.RPAREN)
        
        # Parse return type
        return_type = None
        if self.current_token.type == TokenType.RETURN:
            self.eat(TokenType.RETURN)
            return_type = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
        # Parse body
        body = []
        while self.current_token.type != TokenType.END:
            statement = self.parse_statement()
            if statement:
                body.append(statement)
                
        self.eat(TokenType.END)
        
        return FunctionDecl(name, params, return_type, body)

    def parse_variable_declaration(self) -> VariableDecl:
        var_type = self.current_token.value
        self.eat(self.current_token.type)
        
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.ASSIGN)
        value = self.parse_expression()
        
        return VariableDecl(name, var_type, value)

    def parse_assignment(self) -> Assignment:
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.ASSIGN)
        value = self.parse_expression()
        
        return Assignment(name, value)

    def parse_expression(self) -> ASTNode:
            node = self.parse_term()

            while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
                operator = self.current_token.type
                self.eat(operator)
                right = self.parse_term()
                node = BinaryOp(node, operator, right)

            return node

    def parse_term(self) -> ASTNode:
        node = self.parse_factor()
        
        while self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            operator = self.current_token.type
            self.eat(operator)
            right = self.parse_factor()
            node = BinaryOp(node, operator, right)
            
        return node
        
    def parse_factor(self) -> ASTNode:
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(float(token.value))
            
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token.value)
            
        elif token.type in [TokenType.TRUE, TokenType.FALSE]:
            self.eat(token.type)
            return Boolean(token.type == TokenType.TRUE)
            
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Identifier(token.value)
            
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return node
            
        self.error(f"Unexpected factor token: {token.type}")
        
    def parse_display(self) -> Display:
        self.eat(TokenType.DISPLAY)
        value = self.parse_expression()
        return Display(value)

# Symbol Table for tracking variables and their types
class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Any] = {}
        self.parent: Optional[SymbolTable] = None
        
    def define(self, name: str, symbol_type: str, value: Any = None):
        self.symbols[name] = {"type": symbol_type, "value": value}
        
    def lookup(self, name: str) -> Optional[Dict[str, Any]]:
        symbol = self.symbols.get(name)
        if symbol is None and self.parent:
            return self.parent.lookup(name)
        return symbol

# Code Generator
class CodeGenerator:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.output = []
        self.indent_level = 0
        
    def indent(self):
        self.indent_level += 1
        
    def dedent(self):
        self.indent_level -= 1
        
    def emit(self, code: str):
        self.output.append("    " * self.indent_level + code)
        
    def visit(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
        
    def generic_visit(self, node: ASTNode):
        raise Exception(f'No visit_{type(node).__name__} method')
        
    def visit_Program(self, node: Program):
        self.emit("# Generated Python code")
        if node.description:
            self.emit(f"# Description: {node.description}")
        if node.author:
            self.emit(f"# Author: {node.author}")
        if node.date:
            self.emit(f"# Date: {node.date}")
        self.emit("")
        
        for statement in node.body:
            self.visit(statement)
            
        return "\n".join(self.output)
        
    def visit_FunctionDecl(self, node: FunctionDecl):
        params = ", ".join(name for name, _ in node.params)
        self.emit(f"def {node.name}({params}):")
        self.indent()
        
        # Add parameter type hints as comments
        for name, param_type in node.params:
            if param_type:
                self.emit(f"# Parameter {name}: {param_type}")
                
        if node.return_type:
            self.emit(f"# Returns: {node.return_type}")
            
        for statement in node.body:
            self.visit(statement)
            
        self.dedent()
        self.emit("")
        
    def visit_VariableDecl(self, node: VariableDecl):
        value = self.visit(node.value)
        self.symbol_table.define(node.name, node.type, value)
        self.emit(f"{node.name} = {value}")
        
    def visit_Assignment(self, node: Assignment):
        value = self.visit(node.value)
        self.emit(f"{node.target} = {value}")
        
    def visit_BinaryOp(self, node: BinaryOp):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        op_map = {
            TokenType.PLUS: "+",
            TokenType.MINUS: "-",
            TokenType.MULTIPLY: "*",
            TokenType.DIVIDE: "/"
        }
        
        return f"({left} {op_map[node.operator]} {right})"
        
    def visit_Number(self, node: Number):
        return str(node.value)
        
    def visit_String(self, node: String):
        return f'"{node.value}"'
        
    def visit_Boolean(self, node: Boolean):
        return str(node.value)
        
    def visit_Identifier(self, node: Identifier):
        return node.name
        
    def visit_Display(self, node: Display):
        value = self.visit(node.value)
        self.emit(f"print({value})")

# Main Compiler class that puts everything together
class NovaScriptCompiler:
    def __init__(self):
        self.lexer = None
        self.parser = None
        self.code_generator = None
        
    def compile(self, source_code: str) -> str:
        try:
            # Lexical analysis
            self.lexer = Lexer(source_code)
            
            # Parsing
            self.parser = Parser(self.lexer)
            ast = self.parser.parse_program()
            
            # Code generation
            self.code_generator = CodeGenerator()
            python_code = self.code_generator.visit(ast)
            
            return python_code
            
        except Exception as e:
            return f"Compilation error: {str(e)}"

def main():
    filename = input("Please enter the name of the file to be executed: ").strip()

    # Check if a filename was provided
    if not filename:
        print("Error: No filename provided.")
        return

    # Check if the file exists
    if not os.path.isfile(filename):
        print(f"Error: The file '{filename}' does not exist.")
        return

    # Attempt to open and read the file
    try:
        with open(filename, 'r') as file:
            source_code = file.read()
    except IOError as e:
        print(f"Error: Unable to read the file '{filename}'. {e}")
        return

    # Check if the source code is empty
    if not source_code:
        print("Error: No code found in the file.")
        return


    compiler = NovaScriptCompiler()
    python_code = compiler.compile(source_code)

    execute = True

    if execute:
        try:
            exec(python_code)
        except Exception as e:
            print(f"Error while executing code : {e}")
    else:
        return

if __name__ == "__main__":
    main()
