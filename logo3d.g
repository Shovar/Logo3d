grammar logo3d;

root
 : program* EOF
 ;

program
 : PROC ID OPAR parametros? CPAR IS func END
 ;

parametros
 : ID (COMA ID)*   
 ;

func
: stat*
;

stat
 : assignment
 | if_stat END
 | (while_stat | for_stat) END
 | read_stat
 | write_stat
 | call_stat
 ;

assignment
 : ID ASSIGN expr 
 ;

if_stat
 : IF condition (ELSE IF condition)* (ELSE func)?
 ;

condition
 : expr THEN func
 ;

while_stat
 : WHILE expr DO func 
 ;

for_stat
 : FOR ID FROM number TO (number|variable) DO func
 ;

read_stat
 : READ ID
 ;

write_stat
 : WRITE expr
 | WRITE ID
 ;

call_stat
 : ID OPAR call_arguments? CPAR
 ;

call_arguments
: (expr COMA)* (expr)
;

expr
 : OPAR expr CPAR						  #ParExpr
 | <assoc=right> expr POW expr            #PowExpr
 | RES expr                               #ResExpr
 | NOT expr                               #NotExpr
 | expr op=(MULT | DIV ) expr          	  #MDExpr
 | expr op=(SUM | RES) expr               #SRExpr
 | expr op=(LTEQ | GTEQ | LT | GT) expr   #CompExpr
 | expr op=(EQ | NEQ) expr                #EqNExpr
 | (number | variable)                    #NumVarExpr
 ;

number
 : (INT | FLOAT)
 ;

variable
 : ID
 ;

EQ : '==';
NEQ : '!=';
NOT : '!';
GT : '>';
LT : '<';
GTEQ : '>=';
LTEQ : '<=';
SUM : '+';
RES : '-';
MULT : '*';
DIV : '/';
POW : '^';

ASSIGN : ':=';
OPAR : '(';
CPAR : ')';
COMA : ',';

TRUE : 'true';
FALSE : 'false';
IF : 'IF';
THEN : 'THEN';
ELSE : 'ELSE';
WHILE : 'WHILE';
FOR : 'FOR';
FROM : 'FROM';
TO : 'TO';
DO : 'DO';

PROC : 'PROC';
IS : 'IS';

READ : '>>';
WRITE : '<<';

END : 'END';


INT
 : [0-9]+
 | RES?[1-9][0-9]*
 ;

ID
 : [a-zA-Z_0-9]+
 ;

FLOAT
 : [0-9]+ '.' [0-9]* 
 | '.' [0-9]+
 ;

COMMENT
 : '//' ~[\r\n]* -> skip
 ;

WS
 : [ \t\r\n] -> skip
 ;
