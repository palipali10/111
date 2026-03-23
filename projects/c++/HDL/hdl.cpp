#include <iostream>
using namespace std;


https://www.thevfdcollective.com/blog/2018/11/26/oop-in-plain-c

/*
            


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



class Token{
    public:
        static const char type;
        int line;
        int column;

    void display(){
        cout << type << " " << line << " " << column << endl;
    }
};

class Lexer{
    public:
        string source;
        int pos = 0;
        int line = 1;
        int column = 1;
        Token *tokenArray[];

        keywords = {
           tokenString[tokenType.MODULE],
           tokenString[tokenType.INPUT],
           tokenString[tokenType.OUTPUT],
           tokenString[tokenType.BIT],
           tokenString[tokenType.REG],
           tokenString[tokenType.ON],
           tokenString[tokenType.POSEDGE],
        }

    Lexer(string source){
        this->source = source
    }

    string currentChar(this, ){
        if(this->pos >= len(this->source))
            return NULL;
        return this->source[this->pos];
    }




};


