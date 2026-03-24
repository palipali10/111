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

    Lexer(string source){
        this->source = source
    }

    static const char currentChar(){
        if(this->pos >= (this->source).size())
            return NULL;
        return (this->source)[this->pos];
    }

    string peek(int offset = 1){
        int peekPos = this->pos + offset;
        if(peekPos >= (this->source).size())
        return this->source[peekPos];
    }

    void advance(){
        if(this->currentChar == '\n'){
            this->line+=1;
            this->column+=1;
        }else{
            this->column+=1;
        }
        this->pos+=1;
    }

    void skipWhitespace(){
        while(this->currentChar && (this->currentChar.isspace())){
            this->advance();
        }
    }

    void skipComment(){
        if(this->currentChar == '/' && this->peek() == '/'){
            while(this->currentChar && this->currentChar != '\n'){
                this->advance();
            }
            this->advance();
        }
    }






};


