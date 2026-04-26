from SymbolTable import *
from Type import *

# --- Main classes --- #

class Node:
    def eval(self, env):
        pass

class Numeric(Node):
    def eval(self, env):
        pass

class Logic(Node):
    def eval(self, env):
        pass

class Void(Node):
    def eval(self, env):
        pass

# --- NUMERIC --- #
class Number(Numeric):
    def __init__(self, value):
        self.value = value
    
    def eval(self, env):
        return self.value

class Identifier(Numeric):
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def eval(self, env):
        result = env.lookup(self.name)
        if result != None:
            (_, value) = result
            return value
        else: 
            text = "Line " + str(self.line) + " - " + self.name + " has not been declared"
            raise Exception(text)

class Minus(Numeric):
    def __init__(self, right):
        self.right = right

    def eval(self, env):
        return -1 * float(self.right.eval(env))
    
class Add(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left + right
    
class Substract(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left - right
    
class Multiply(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left * right
    
class Divide(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        if right == 0:
            raise Exception("Division by zero")
        
        return left / right
    
class Mod(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        if right == 0:
            raise Exception("Modulo by zero")
        
        return left % right

# --- LOGIC --- #

class Boolean(Logic):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value
    
class LessThan(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left < right
    
class LessEqual(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left <= right
    
class GreaterThan(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left > right
    
class GreaterEqual(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left >= right
    
class Equal(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left == right
    
class And(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = bool(self.left.eval(env))
        right = bool(self.right.eval(env))
        return left & right
    
class Or(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = bool(self.left.eval(env))
        right = bool(self.right.eval(env))
        return left | right
    
class NotEqual(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left != right
    
class Not(Logic):
    def __init__(self, right):
        self.right = right
    def eval(self, env):
        right = bool(self.right.eval(env))
        return not right

# --- Functionality Classes --- #

class VarDeclaration(Void):
    """
    This class checks if a variable has already been declared
    """
    def __init__(self, names, line):
        self.names = names
        self.line = line

    def eval(self, env):
        for name in self.names:
            lInserted = env.insert(name)     

            if lInserted == False:
                text = "Line " + str(self.line) + " - " + name + " has already been declared"
                raise Exception(text)
            

class Program(Void):
    def __init__(self, statements):
        self.statements = statements
    
    def eval(self, env):
        for statement in self.statements:
            statement.eval(env)

class Assignment(Void):
    """
    This class assign a value to a variable
    """
    def __init__(self, name, expression, line):
        self.name = name
        self.expression = expression
        self.line = line
    
    def eval(self, env):
        value = self.expression.eval(env)
        updated = env.set(self.name, None, value)
        if updated == False:
            text = "Line " + str(self.line) + " - " + "has not been declared"
            raise Exception(text)

class Print(Void):
    """
    This class prints the value of the evaluated expression
    """
    def __init__(self, expression):
        self.expression = expression

    def eval(self, env):
        value = self.expression.eval(env)
        print(value)