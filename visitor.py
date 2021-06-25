from antlr4 import *
from turtle3d import Turtle3D
import sys

if __name__ is not None and "." in __name__:
    from .logo3dParser import logo3dParser
    from .logo3dVisitor import logo3dVisitor
else:
    from logo3dParser import logo3dParser
    from logo3dVisitor import logo3dVisitor


class EvalVisitor(logo3dVisitor):
    # Inicializo el visitor
    def __init__(self, inicial):
        # Inicializo la tortuga
        self.turtle = None
        # Inicializo una lista de diccionarios para las variables locales de cada procedimiento
        self.memory = []
        # Inicializo un diccionario para guardar cada procedimiento con su especificación y sus argumentos
        self.procs = {}
        self.ini = True

        # Compruebo los argumentos que han entrado como input, si no hay ninguno se ejecutará la función 'main',
        # De otra forma se lee el nombre de la función y el valor entrado para sus argumentos si tiene
        if len(inicial) == 0:
            self.inicial = 'main'
            self.arguments = []
        else:
            self.inicial = inicial[0]
            if len(inicial) > 0:
                self.arguments = inicial[1:len(inicial)]

    # Evaluación del Root
    def visitRoot(self, ctx):
        self.visitChildren(ctx)
        main_proc = self.procs.get(self.inicial)    # Tomo como procedimiento principal el especificado en la ejecución
        # Si no existe o el numero de argumentos no es válido salta una excepción
        if main_proc is None:
            raise Exception('Proc ' + self.inicial + ' does not exist')

        if main_proc[1] == [] and self.arguments != []:
            raise Exception('Non-identical number of arguments given to the function ' + self.inicial + ' definition')

        # Se crea un diccionario de variables locales para el procedimiento a ejecutar y si tiene argumentos se añaden a éste
        local_vars = {}
        if len(self.arguments) > 0:
            args = self.arguments
            for arg in args:
                arg = float(arg) if '.' in arg else int(arg)

            # Cojo el argumento del procedimiento y le asigno el valor entrado
            for name, value in zip(main_proc[1], [arg for arg in args]):
                local_vars[name] = value
        # Se añade a la pila de diccionarios el diccionario que corresponde a las variables locales del procedimiento actual, una vez finaliza se elimina de la pila
        self.memory.append(local_vars)
        self.visit(main_proc[0])
        self.memory.pop()

        if not self.ini:
            self.turtle.delete()
        return

    # Evaluación del program
    def visitProgram(self, ctx):
        # Cojo los argumentos del procedimiento
        func_args = [arg for arg in ctx.parametros().getText().split(',')] if ctx.parametros() else []
        # Si el procedimiento ya ha sido definido, salta una excepción
        if ctx.ID().getText() in self.procs:
            raise Exception('Proc ' + ctx.ID().getText() + ' already defined')
        # Guardo en el diccionario de procedimientos, el procedimiento a visitar, su función y sus argumentos
        self.procs[ctx.ID().getText()] = (ctx.func(), func_args)

    # Evaluación de la asignación
    def visitAssignment(self, ctx):
        g = ctx.getChildren()
        l = [next(g) for i in range(3)]
        # Almaceno la asignación en el diccionario de variables locales del último procedimiento (el actual)
        self.memory[- 1][ctx.ID().getText()] = self.visit(l[2])

    # Evaluacion de la lectura
    def visitRead_stat(self, ctx):
        # Almaceno el elemento leído por la entrada estandar en el diccionario de variables locales actuales
        self.memory[-1][ctx.ID().getText()] = float(input('? '))

    # Evaluación de la escritura
    def visitWrite_stat(self, ctx):
        # Si se trata de la escritura de una expresión, se evalúa primero y luego se escribe
        # En caso contrario, se busca la variable a ecribir en el diccionario de variables locales actuales
        if ctx.ID() is None:
            print(self.visit(ctx.expr()))
        else:
            if self.memory[-1].get(ctx.ID().getText()) is None:
                raise Exception(ctx.ID().getText() + ' does not exist')
            print(self.memory[-1].get(ctx.ID().getText()))

    # Evaluación del condicional
    def visitIf_stat(self, ctx):
        conditions = ctx.condition()
        evaluated = False
        result = 0
        # Compruevo si se cumplen todas las condiciones del IF, si se cumple se lleva a cabo, caso contrario
        # Se hace el siguiente elemento del condicional(else if o else) si hay
        for cond in conditions:
            evaluated_condition = self.visit(cond.expr())
            if evaluated_condition is True:
                evaluated = True
                result = self.visit(cond.func())
                break
        if evaluated is False and ctx.func() is not None:
            result = self.visit(ctx.func())

        return result

    # Evaluación del while
    def visitWhile_stat(self, ctx):
        expr = self.visit(ctx.expr())
        while expr is True:
            result = self.visit(ctx.func())
            expr = self.visit(ctx.expr())

    # Evaluación del for
    def visitFor_stat(self, ctx):
        g = ctx.getChildren()
        l = [next(g) for i in range(8)]
        init = self.visit(l[3])
        finish = self.visit(l[5])
        if isinstance(init, int) and isinstance(finish, int):
            self.memory[-1][l[1].getText()] = init
            while self.memory[-1].get(l[1].getText()) <= finish:
                self.visit(l[7])
                self.memory[-1][l[1].getText()] = self.memory[-1].get(l[1].getText()) + 1
        else:
            for var in self.memory[-1].keys():
                if finish == var:
                    finish = float(self.memory[-1].get(var))

            if isinstance(init, int) and isinstance(finish, int):
                self.memory[-1][l[1].getText()] = init
                while self.memory[-1].get(l[1].getText()) <= finish:
                    self.visit(l[7])
                    self.memory[-1][l[1].getText()] = self.memory[-1].get(l[1].getText()) + 1
            else:
                raise ValueError('Range definition must be integer')

    # Evaluación de la llamada a un procedimiento
    def visitCall_stat(self, ctx):
        func = self.procs.get(ctx.ID().getText())
        # Saltan excepciones si el procedimiento no existe, no se han introducido argumentos cuando se necesitan o bien no hay el mismo número
        # de argumentos que en la definicion del procedimiento
        if not func:
            # Compruebo que sea una de las funciones de la tortuga
            call_args = ctx.call_arguments().expr()
            if ctx.ID().getText() == 'color':
                if len(call_args) == 3:
                    if self.ini:
                        self.turtle = Turtle3D()
                        self.ini = False
                    return self.turtle.color(self.visit(call_args[0]), self.visit(call_args[1]), self.visit(call_args[2]))
                else:
                    raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')
            elif ctx.ID().getText() == 'forward':
                if len(call_args) == 1:
                    if self.ini:
                        self.turtle = Turtle3D()
                        self.ini = False
                    return self.turtle.forward(self.visit(call_args[0]))
                else:
                    raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')
            elif ctx.ID().getText() == 'backward':
                if len(call_args) == 1:
                    if self.ini:
                        self.turtle = Turtle3D()
                        self.ini = False
                    return self.turtle.backward(self.visit(call_args[0]))
                else:
                    raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')
            elif ctx.ID().getText() == 'up':
                if len(call_args) == 1:
                    if self.ini:
                        self.turtle = Turtle3D()
                        self.ini = False
                    return self.turtle.up(self.visit(call_args[0]))
                else:
                    raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')
            elif ctx.ID().getText() == 'down':
                if len(call_args) == 1:
                    if self.ini:
                        self.turtle = Turtle3D()
                        self.ini = False
                    return self.turtle.down(self.visit(call_args[0]))
                else:
                    raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')
            elif ctx.ID().getText() == 'left':
                if len(call_args) == 1:
                    if self.ini:
                        self.turtle = Turtle3D()
                        self.ini = False
                    return self.turtle.left(self.visit(call_args[0]))
                else:
                    raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')
            elif ctx.ID().getText() == 'right':
                if len(call_args) == 1:
                    if self.ini:
                        self.turtle = Turtle3D()
                        self.ini = False
                    return self.turtle.right(self.visit(call_args[0]))
                else:
                    raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')
            elif ctx.ID().getText() == 'hide':
                if len(call_args) == 0:
                    if self.ini:
                        self.turtle = Turtle3D()
                        self.ini = False
                    return self.turtle.hide()
                else:
                    raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')
            elif ctx.ID().getText() == 'show':
                if len(call_args) == 0:
                    if self.ini:
                        self.turtle = Turtle3D()
                        self.ini = False
                    return self.turtle.show()
                else:
                    raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')
            elif ctx.ID().getText() == 'home':
                if len(call_args) == 0:
                    if self.ini:
                        self.turtle = Turtle3D()
                        self.ini = False
                    return self.turtle.home()
                else:
                    raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')

            raise NameError('Function ' + ctx.ID().getText() + ' not found in memory')

        if len(func[1]) > 0 and not ctx.call_arguments():
            raise Exception('No arguments were given to the function ' + ctx.ID().getText())

        if ctx.call_arguments():
            call_args = ctx.call_arguments().expr()

            if len(call_args) != len(func[1]):
                raise Exception('Non-identical number of arguments given to the function ' + ctx.ID().getText() + ' definition')
            # Cojo el argumento del procedimiento y le asigno el valor especificado en la llamada

            local_vars = {}
            for name, value in zip(func[1], [self.visit(arg) for arg in call_args]):
                local_vars[name] = value
        # Se añade a la pila de diccionarios el diccionario que corresponde a las variables locales del procedimiento actual, una vez finaliza se elimina de la pila
        self.memory.append(local_vars)
        result = self.visit(func[0])
        self.memory.pop()

        for name in func[1]:
            if name in self.procs:
                del self.procs[name]

        return result

    # Evaluación de la expresión con parentesis .
    def visitParExpr(self, ctx):
        return self.visit(ctx.expr())

    # Evaluación de la suma o resta.
    def visitSRExpr(self, ctx):
        g = ctx.getChildren()
        l = [next(g) for i in range(3)]

        left = self.visit(l[0])
        right = self.visit(l[2])
        # Si son números se aplica la operación directamente, si no lo son; se trata de buscar en el diccionario de variables locales y
        # y si no aparecen, salta una excepción.
        if(isinstance(left, (int, float)) and isinstance(right, (int, float))):
            if (logo3dParser.symbolicNames[l[1].getSymbol().type] == "SUM"):
                return left + right
            else:
                return left - right
        else:
            for var in self.memory[-1].keys():
                if left == var:
                    left = float(self.memory[-1].get(var))

                if right == var:
                    right = float(self.memory[-1].get(var))
            print(self.memory[-1].keys())
            if(isinstance(left, (int, float)) and isinstance(right, (int, float))):
                if (logo3dParser.symbolicNames[l[1].getSymbol().type] == "SUM"):
                    return left + right
                else:
                    return left - right
            else:
                raise ValueError('Could not convert string to a number')

    # Evaluación de la multiplicación o división.
    def visitMDExpr(self, ctx: logo3dParser.MDExprContext):
        g = ctx.getChildren()
        l = [next(g) for i in range(3)]

        left = self.visit(l[0])
        right = self.visit(l[2])

        # Si son números se aplica la operación directamente, si no lo son; se trata de buscar en el diccionario de variables locales y
        # y si no aparecen, salta una excepción.
        if(isinstance(left, (int, float)) and isinstance(right, (int, float))):
            if (logo3dParser.symbolicNames[l[1].getSymbol().type] == "MULT"):
                return left * right
            else:
                if right == 0:
                    raise ZeroDivisionError('division by zero')
                return left / right
        else:
            for var in self.memory[-1].keys():
                if left == var:
                    left = float(self.memory[-1].get(var))

                if right == var:
                    right = float(self.memory[-1].get(var))

        if(isinstance(left, (int, float)) and isinstance(right, (int, float))):
            if (logo3dParser.symbolicNames[l[1].getSymbol().type] == "MULT"):
                return left * right
            else:
                if right == 0:
                    raise ZeroDivisionError('division by zero')
                return left / right
        else:
            raise ValueError('Could not convert string to a number')

    # Evaluación de la elevación.
    def visitPowExpr(self, ctx):
        g = ctx.getChildren()
        l = [next(g) for i in range(3)]
        left = self.visit(l[0])
        right = self.visit(l[2])
        # Si son números se aplica la operación directamente, si no lo son; se trata de buscar en el diccionario de variables locales y
        # y si no aparecen, salta una excepción.

        if(isinstance(left, (int, float)) and isinstance(right, (int, float))):
            return left ** right
        else:
            for var in self.memory[-1].keys():
                if left == var:
                    left = float(self.memory[-1].get(var))

                if right == var:
                    right = float(self.memory[-1].get(var))

        if(isinstance(left, (int, float)) and isinstance(right, (int, float))):
            return left ** right
        else:
            raise ValueError('Could not convert string to a number')

    # Evaluación de comparaciones.
    def visitCompExpr(self, ctx: logo3dParser.CompExprContext):
        g = ctx.getChildren()
        l = [next(g) for i in range(3)]
        if (logo3dParser.symbolicNames[l[1].getSymbol().type] == "LTEQ"):
            return self.visit(l[0]) <= self.visit(l[2])
        elif (logo3dParser.symbolicNames[l[1].getSymbol().type] == "GTEQ"):
            return self.visit(l[0]) >= self.visit(l[2])
        elif (logo3dParser.symbolicNames[l[1].getSymbol().type] == "GT"):
            return self.visit(l[0]) > self.visit(l[2])
        elif (logo3dParser.symbolicNames[l[1].getSymbol().type] == "LT"):
            return self.visit(l[0]) < self.visit(l[2])
        else:
            raise SyntaxError('Unknown operator')

    # Evaluación de igualdades o desigualdades.
    def visitEqNExpr(self, ctx: logo3dParser.EqNExprContext):
        g = ctx.getChildren()
        l = [next(g) for i in range(3)]
        if (logo3dParser.symbolicNames[l[1].getSymbol().type] == "EQ"):
            return self.visit(l[0]) == self.visit(l[2])
        elif (logo3dParser.symbolicNames[l[1].getSymbol().type] == "NEQ"):
            return self.visit(l[0]) != self.visit(l[2])
        else:
            raise SyntaxError('Unknown operator')

    # Evaluación de una expresión negativa.
    def visitResExpr(self, ctx: logo3dParser.ResExprContext):
        g = ctx.getChildren()
        l = [next(g) for i in range(2)]
        expr = self.visit(l[1])
        if isintance(expr, (int, float)):
            return -expr
        else:
            raise ValueError('Could not convert string to a number')

    # Evaluación del negado a una expresión.
    def visitNotExpr(self, ctx: logo3dParser.NotExprContext):
        g = ctx.getChildren()
        l = [next(g) for i in range(2)]
        var = self.visit(l[1])
        if isintance(var, bool):
            return not var
        elif isintance(var, (int, float)):
            if var != 0:
                return False
            else:
                return True
        else:
            raise ValueError('Could not convert variable to boolean')

    # Evaluación del tipo número.
    def visitNumber(self, ctx):
        num = ctx.getText()
        return float(num) if '.' in num else int(num)

    # Evaluación del tipo variable.
    def visitVariable(self, ctx):
        if self.memory[-1].get(ctx.getText()) is not None:
            num = self.memory[-1].get(ctx.getText())
            if isinstance(num, (int, float)):
                return num
            elif isinstance(num, bool):
                return num
            else:
                return float(num)
        else:
            return ctx.getText().strip('\'"')
