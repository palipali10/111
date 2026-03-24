#include <stdio.h>

https://www.thevfdcollective.com/blog/2018/11/26/oop-in-plain-c

/*
    notes:
        hdl
            hardware description language
            simulator
            something that writes directly to hardware
            


*/

enum tokenType{
    MODULE,
    INPUT,
    OUTPUT,
    BIT,
    REG,
    ON,
    POSEDGE,
    NEGEDGE,
    IF,
    ELSE,
    IDENTIFIER,
    NUMBER,
    ASSIGN,
    NONBLOCK,
    PLUS,
    MINUS,
    AND,
    OR,
    XOR,
    NOT,
    EQ,
    NEQ
};
 
static const char *tokenString[] = {
    "module", "input", "output", "bit", "reg",
    "on", "posedge", "negedge", "if", "else", 
    "IDENTIFIER", "NUMBER", "=", "<=", "+", "-", "&", 
    "|", "^", "~", "==", "!=", "{", "}", "(", ")", "[", "]", ";", ",", "EOF"
};

typedef struct Token{
    enum tokenType;

    void (*__init__)(struct Student *this);

} Token;


/*
typedef struct Lexer 
typedef struct ASTNode:
typedef struct Port 
typedef struct Assignment
typedef struct BinaryOp
typedef struct UnaryOp
typedef struct Identifier
typedef struct Number
typedef struct AlwaysBlock
typedef struct IfStatement
typedef struct RegDeclaration
typedef struct Parser 
typedef struct Signal 
typedef struct Simulator 
*/


int main(){



    return 0;
}