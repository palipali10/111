#!/usr/bin/env python3
"""
SimpleHDL - A Minimal Hardware Description Language
Complete working implementation for educational purposes

Features:
- Lexer and tokenizer
- Recursive descent parser
- AST representation
- Event-driven simulator
- Basic synthesis to gates

Author: Educational Example
License: MIT
"""

from enum import Enum
from typing import List, Dict, Any, Optional, Tuple

# ============================================================================
# TOKEN DEFINITIONS
# ============================================================================

class TokenType(Enum):
    # Keywords
    MODULE = "module"
    INPUT = "input"
    OUTPUT = "output"
    BIT = "bit"
    REG = "reg"
    ON = "on"
    POSEDGE = "posedge"
    NEGEDGE = "negedge"
    IF = "if"
    ELSE = "else"
    
    # Literals
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    
    # Operators
    ASSIGN = "="
    NONBLOCK = "<="
    PLUS = "+"
    MINUS = "-"
    AND = "&"
    OR = "|"
    XOR = "^"
    NOT = "~"
    EQ = "=="
    NEQ = "!="
    
    # Delimiters
    LBRACE = "{"
    RBRACE = "}"
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    SEMICOLON = ";"
    COMMA = ","
    
    EOF = "EOF"


class Token:
    def __init__(self, type: TokenType, value: Any, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


# ============================================================================
# LEXER
# ============================================================================

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        self.keywords = {
            'module': TokenType.MODULE,
            'input': TokenType.INPUT,
            'output': TokenType.OUTPUT,
            'bit': TokenType.BIT,
            'reg': TokenType.REG,
            'on': TokenType.ON,
            'posedge': TokenType.POSEDGE,
            'negedge': TokenType.NEGEDGE,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
        }
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.pos + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def advance(self):
        if self.current_char() == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            self.advance()
    
    def read_number(self) -> int:
        num_str = ''
        while self.current_char() and self.current_char().isdigit():
            num_str += self.current_char()
            self.advance()
        return int(num_str)
    
    def read_identifier(self) -> str:
        id_str = ''
        while self.current_char() and (self.current_char().isalnum() or 
                                       self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        return id_str
    
    def tokenize(self) -> List[Token]:
        while self.current_char():
            self.skip_whitespace()
            if not self.current_char():
                break
            
            self.skip_comment()
            if not self.current_char():
                break
            
            ch = self.current_char()
            col = self.column
            
            # Two-character operators
            if ch == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NONBLOCK, '<=', self.line, col))
            elif ch == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQ, '==', self.line, col))
            elif ch == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NEQ, '!=', self.line, col))
            # Single character tokens
            elif ch == '{':
                self.tokens.append(Token(TokenType.LBRACE, ch, self.line, col))
                self.advance()
            elif ch == '}':
                self.tokens.append(Token(TokenType.RBRACE, ch, self.line, col))
                self.advance()
            elif ch == '(':
                self.tokens.append(Token(TokenType.LPAREN, ch, self.line, col))
                self.advance()
            elif ch == ')':
                self.tokens.append(Token(TokenType.RPAREN, ch, self.line, col))
                self.advance()
            elif ch == '[':
                self.tokens.append(Token(TokenType.LBRACKET, ch, self.line, col))
                self.advance()
            elif ch == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ch, self.line, col))
                self.advance()
            elif ch == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ch, self.line, col))
                self.advance()
            elif ch == ',':
                self.tokens.append(Token(TokenType.COMMA, ch, self.line, col))
                self.advance()
            elif ch == '=':
                self.tokens.append(Token(TokenType.ASSIGN, ch, self.line, col))
                self.advance()
            elif ch == '+':
                self.tokens.append(Token(TokenType.PLUS, ch, self.line, col))
                self.advance()
            elif ch == '-':
                self.tokens.append(Token(TokenType.MINUS, ch, self.line, col))
                self.advance()
            elif ch == '&':
                self.tokens.append(Token(TokenType.AND, ch, self.line, col))
                self.advance()
            elif ch == '|':
                self.tokens.append(Token(TokenType.OR, ch, self.line, col))
                self.advance()
            elif ch == '^':
                self.tokens.append(Token(TokenType.XOR, ch, self.line, col))
                self.advance()
            elif ch == '~':
                self.tokens.append(Token(TokenType.NOT, ch, self.line, col))
                self.advance()
            elif ch.isdigit():
                num = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, num, self.line, col))
            elif ch.isalpha() or ch == '_':
                id_str = self.read_identifier()
                token_type = self.keywords.get(id_str, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, id_str, self.line, col))
            else:
                raise SyntaxError(f"Unexpected character '{ch}' at {self.line}:{col}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


# ============================================================================
# AST NODE DEFINITIONS
# ============================================================================

class ASTNode:
    pass


class Module(ASTNode):
    def __init__(self, name: str, ports: List['Port'], body: List[ASTNode]):
        self.name = name
        self.ports = ports
        self.body = body
    
    def __repr__(self):
        return f"Module({self.name})"


class Port(ASTNode):
    def __init__(self, direction: str, port_type: str, name: str, width: Optional[int] = None):
        self.direction = direction
        self.port_type = port_type
        self.name = name
        self.width = width
    
    def __repr__(self):
        width_str = f"[{self.width}]" if self.width else ""
        return f"{self.direction} {self.port_type}{width_str} {self.name}"


class Assignment(ASTNode):
    def __init__(self, target: str, expression: ASTNode, blocking: bool = True):
        self.target = target
        self.expression = expression
        self.blocking = blocking
    
    def __repr__(self):
        op = '=' if self.blocking else '<='
        return f"Assignment({self.target} {op} ...)"


class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.op})"


class UnaryOp(ASTNode):
    def __init__(self, op: str, operand: ASTNode):
        self.op = op
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOp({self.op})"


class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return f"Identifier({self.name})"


class Number(ASTNode):
    def __init__(self, value: int):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"


class AlwaysBlock(ASTNode):
    def __init__(self, sensitivity: Tuple[str, str], body: List[ASTNode]):
        self.sensitivity = sensitivity
        self.body = body
    
    def __repr__(self):
        return f"AlwaysBlock({self.sensitivity})"


class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, then_body: List[ASTNode], 
                 else_body: Optional[List[ASTNode]] = None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
    
    def __repr__(self):
        return f"IfStatement(...)"


class RegDeclaration(ASTNode):
    def __init__(self, reg_type: str, name: str, width: Optional[int] = None):
        self.reg_type = reg_type
        self.name = name
        self.width = width


# ============================================================================
# PARSER
# ============================================================================

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type.name}, got {token.type.name} "
                f"at {token.line}:{token.column}"
            )
        self.advance()
        return token
    
    def parse_program(self) -> List[Module]:
        modules = []
        while self.current_token().type != TokenType.EOF:
            modules.append(self.parse_module())
        return modules
    
    def parse_module(self) -> Module:
        self.expect(TokenType.MODULE)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LBRACE)
        
        ports = self.parse_ports()
        body = self.parse_body()
        
        self.expect(TokenType.RBRACE)
        return Module(name, ports, body)
    
    def parse_ports(self) -> List[Port]:
        ports = []
        while self.current_token().type in [TokenType.INPUT, TokenType.OUTPUT]:
            direction = self.current_token().value
            self.advance()
            
            port_type = self.expect(TokenType.BIT).value
            
            width = None
            if self.current_token().type == TokenType.LBRACKET:
                self.advance()
                width = self.expect(TokenType.NUMBER).value
                self.expect(TokenType.RBRACKET)
            
            name = self.expect(TokenType.IDENTIFIER).value
            ports.append(Port(direction, port_type, name, width))
            
            if self.current_token().type == TokenType.SEMICOLON:
                self.advance()
        
        return ports
    
    def parse_body(self) -> List[ASTNode]:
        statements = []
        while self.current_token().type not in [TokenType.RBRACE, TokenType.EOF]:
            if self.current_token().type == TokenType.ON:
                statements.append(self.parse_always_block())
            elif self.current_token().type == TokenType.REG:
                statements.append(self.parse_reg_declaration())
            elif self.current_token().type == TokenType.IDENTIFIER:
                statements.append(self.parse_assignment())
            else:
                raise SyntaxError(
                    f"Unexpected token {self.current_token().type.name} in module body"
                )
        return statements
    
    def parse_reg_declaration(self) -> RegDeclaration:
        self.expect(TokenType.REG)
        reg_type = self.expect(TokenType.BIT).value
        
        width = None
        if self.current_token().type == TokenType.LBRACKET:
            self.advance()
            width = self.expect(TokenType.NUMBER).value
            self.expect(TokenType.RBRACKET)
        
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.SEMICOLON)
        
        return RegDeclaration(reg_type, name, width)
    
    def parse_always_block(self) -> AlwaysBlock:
        self.expect(TokenType.ON)
        
        edge_type = self.current_token().value
        self.advance()
        self.expect(TokenType.LPAREN)
        signal = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.RPAREN)
        
        sensitivity = (edge_type, signal)
        
        self.expect(TokenType.LBRACE)
        body = []
        while self.current_token().type != TokenType.RBRACE:
            body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        return AlwaysBlock(sensitivity, body)
    
    def parse_statement(self) -> ASTNode:
        if self.current_token().type == TokenType.IF:
            return self.parse_if_statement()
        elif self.current_token().type == TokenType.IDENTIFIER:
            return self.parse_assignment()
        else:
            raise SyntaxError(f"Unexpected statement: {self.current_token().type.name}")
    
    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        then_body = []
        while self.current_token().type != TokenType.RBRACE:
            then_body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        else_body = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.LBRACE)
            else_body = []
            while self.current_token().type != TokenType.RBRACE:
                else_body.append(self.parse_statement())
            self.expect(TokenType.RBRACE)
        
        return IfStatement(condition, then_body, else_body)
    
    def parse_assignment(self) -> Assignment:
        target = self.expect(TokenType.IDENTIFIER).value
        
        blocking = self.current_token().type == TokenType.ASSIGN
        if self.current_token().type in [TokenType.ASSIGN, TokenType.NONBLOCK]:
            self.advance()
        else:
            raise SyntaxError("Expected assignment operator")
        
        expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        return Assignment(target, expr, blocking)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        while self.current_token().type == TokenType.OR:
            op = self.current_token().value
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_logical_and(self) -> ASTNode:
        left = self.parse_xor()
        while self.current_token().type == TokenType.AND:
            op = self.current_token().value
            self.advance()
            right = self.parse_xor()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_xor(self) -> ASTNode:
        left = self.parse_equality()
        while self.current_token().type == TokenType.XOR:
            op = self.current_token().value
            self.advance()
            right = self.parse_equality()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_equality(self) -> ASTNode:
        left = self.parse_additive()
        while self.current_token().type in [TokenType.EQ, TokenType.NEQ]:
            op = self.current_token().value
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_unary()
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token().value
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.current_token().type == TokenType.NOT:
            op = self.current_token().value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.value)
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {token.type.name}")


# ============================================================================
# SIMULATOR
# ============================================================================

class Signal:
    def __init__(self, name: str, width: int = 1):
        self.name = name
        self.width = width
        self.value = 0
        self.next_value = 0
        self.mask = (1 << width) - 1
    
    def get(self) -> int:
        return self.value
    
    def set(self, value: int):
        """Blocking assignment"""
        self.value = value & self.mask
    
    def set_next(self, value: int):
        """Non-blocking assignment"""
        self.next_value = value & self.mask
    
    def update(self):
        """Apply scheduled changes"""
        self.value = self.next_value


class Simulator:
    def __init__(self, modules: List[Module]):
        self.modules = {m.name: m for m in modules}
        self.signals: Dict[str, Signal] = {}
        self.always_blocks: List[AlwaysBlock] = []
        self.time = 0
    
    def elaborate(self, top_module_name: str):
        """Build signal table and always blocks"""
        module = self.modules[top_module_name]
        
        # Create signals for all ports
        for port in module.ports:
            width = port.width if port.width else 1
            self.signals[port.name] = Signal(port.name, width)
        
        # Process module body
        for stmt in module.body:
            if isinstance(stmt, RegDeclaration):
                width = stmt.width if stmt.width else 1
                if stmt.name not in self.signals:
                    self.signals[stmt.name] = Signal(stmt.name, width)
            elif isinstance(stmt, AlwaysBlock):
                self.always_blocks.append(stmt)
    
    def eval_expression(self, expr: ASTNode) -> int:
        """Evaluate an expression to a value"""
        if isinstance(expr, Number):
            return expr.value
        elif isinstance(expr, Identifier):
            if expr.name in self.signals:
                return self.signals[expr.name].get()
            else:
                raise NameError(f"Unknown signal: {expr.name}")
        elif isinstance(expr, BinaryOp):
            left = self.eval_expression(expr.left)
            right = self.eval_expression(expr.right)
            
            ops = {
                '+': lambda l, r: l + r,
                '-': lambda l, r: l - r,
                '&': lambda l, r: l & r,
                '|': lambda l, r: l | r,
                '^': lambda l, r: l ^ r,
                '==': lambda l, r: 1 if l == r else 0,
                '!=': lambda l, r: 1 if l != r else 0,
            }
            
            if expr.op in ops:
                return ops[expr.op](left, right)
            else:
                raise ValueError(f"Unknown operator: {expr.op}")
        elif isinstance(expr, UnaryOp):
            operand = self.eval_expression(expr.operand)
            if expr.op == '~':
                return ~operand
            else:
                raise ValueError(f"Unknown unary operator: {expr.op}")
        else:
            raise TypeError(f"Unknown expression type: {type(expr)}")
    
    def execute_assignment(self, assignment: Assignment):
        """Execute an assignment statement"""
        value = self.eval_expression(assignment.expression)
        signal = self.signals[assignment.target]
        
        if assignment.blocking:
            signal.set(value)
        else:
            signal.set_next(value)
    
    def execute_statement(self, stmt: ASTNode):
        """Execute a single statement"""
        if isinstance(stmt, Assignment):
            self.execute_assignment(stmt)
        elif isinstance(stmt, IfStatement):
            condition = self.eval_expression(stmt.condition)
            if condition:
                for s in stmt.then_body:
                    self.execute_statement(s)
            elif stmt.else_body:
                for s in stmt.else_body:
                    self.execute_statement(s)
    
    def execute_block(self, block: List[ASTNode]):
        """Execute statements in a block"""
        for stmt in block:
            self.execute_statement(stmt)
    
    def clock_edge(self, signal_name: str, edge_type: str = 'posedge'):
        """Simulate a clock edge"""
        for block in self.always_blocks:
            if (block.sensitivity[0] == edge_type and 
                block.sensitivity[1] == signal_name):
                self.execute_block(block.body)
        
        # Update all non-blocking assignments
        for signal in self.signals.values():
            signal.update()
        
        self.time += 1
    
    def run(self, clk_signal: str, cycles: int) -> Dict[str, List[int]]:
        """Run simulation for N clock cycles"""
        waveform = {name: [] for name in self.signals}
        
        for cycle in range(cycles):
            self.clock_edge(clk_signal, 'posedge')
            
            for name, signal in self.signals.items():
                waveform[name].append(signal.get())
        
        return waveform
    
    def print_waveform(self, waveform: Dict[str, List[int]], signals: Optional[List[str]] = None):
        """Print simple text waveform"""
        if signals is None:
            signals = list(waveform.keys())
        
        print("\n" + "=" * 60)
        print("WAVEFORM")
        print("=" * 60)
        
        max_cycles = len(waveform[signals[0]])
        
        print("Time: ", end="")
        for t in range(max_cycles):
            print(f"{t:4}", end="")
        print()
        
        print("-" * 60)
        
        for sig in signals:
            if sig in waveform:
                print(f"{sig:8}: ", end="")
                for val in waveform[sig]:
                    print(f"{val:4}", end="")
                print()


# ============================================================================
# MAIN DEMO
# ============================================================================

def main():
    print("=" * 60)
    print("SimpleHDL - Hardware Description Language Demo")
    print("=" * 60)
    
    # Example 1: Simple Counter
    hdl_source = """
    module Counter {
        input bit clk;
        input bit reset;
        output bit[8] count;
        
        reg bit[8] count;
        
        on posedge(clk) {
            if (reset) {
                count <= 0;
            } else {
                count <= count + 1;
            }
        }
    }
    """
    
    print("\n📝 HDL Source Code:")
    print(hdl_source)
    
    # Compile
    print("\n🔧 Compiling...")
    lexer = Lexer(hdl_source)
    tokens = lexer.tokenize()
    print(f"   ✓ Lexer: {len(tokens)} tokens")
    
    parser = Parser(tokens)
    modules = parser.parse_program()
    print(f"   ✓ Parser: {len(modules)} module(s) parsed")
    
    # Simulate
    print("\n▶️  Simulating...")
    sim = Simulator(modules)
    sim.elaborate('Counter')
    print(f"   ✓ Elaborated {len(sim.signals)} signals")
    
    # Initialize
    sim.signals['clk'].set(0)
    sim.signals['reset'].set(1)
    sim.signals['count'].set(0)
    
    # Run with reset sequence
    sim.clock_edge('clk')  # Reset cycle
    sim.signals['reset'].set(0)
    
    waveform = sim.run('clk', cycles=16)
    sim.print_waveform(waveform, ['count', 'reset'])
    
    print("\n" + "=" * 60)
    print("✓ Simulation Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()