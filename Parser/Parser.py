from Lexer.LexerEnum import LexerEnum
from Lexer.LexerQueue import LexerQueue
from Lexer.LexerToken import LexerToken
from Lexer.LexerHash import LexerHash
from .ParserTree import ParserTree

from Interpreter.Variable.Variable import VariableConstantType, VariableDeclarationCast

from enum import Enum, unique


class ParserVariable(LexerToken):
    def __init__(self, value):
        super(ParserVariable, self).__init__(value.getToken(), value.getValue())

    @staticmethod
    def isVariable(object):
        return compareToken(object, [LexerEnum.id, LexerEnum.integer, LexerEnum.float, LexerEnum.boolean])
    
    def isStoreVariable(self):
        return compareToken(self, LexerEnum.id)
    
class ParserOperator(LexerToken):
    def __init__(self, value):
        super(ParserOperator, self).__init__(value.getToken(), value.getValue())

    @staticmethod
    def isOperator(object):
        return compareToken(object, [LexerEnum.operator, LexerEnum.logical, LexerEnum.logical_operator])

class ParserPFixOperator(LexerToken):
    def __init__(self, value):
        super(ParserPFixOperator, self).__init__(value.getToken(), value.getValue())

    @staticmethod
    def isPFixOperator(object):
        return compareToken(object, LexerEnum.operator_pfix)

@unique
class ParserFixType(Enum):
    none = 0
    prefix = 1
    posfix = 2

    @staticmethod
    def isPrefix(object):
        return ParserFixType.prefix
    
    @staticmethod
    def isPosfix(object):
        if object.getValue() != "!":
            return ParserFixType.posfix

        return ParserFixType.none

class ParserAssigment(ParserOperator):
    def __init__(self, value):
        super(ParserAssigment, self).__init__(value)
    
    @staticmethod
    def isAssigment(object):
        return compareToken(object, LexerEnum.assigment)

class ParserOperation:
    first = 0
    operator = 0
    second = 0

    def __init__(self, first, second, operator):
        self.first = first
        self.second = second
        self.operator = operator
    
class ParserFixOperation:
    variable = 0
    operator = 0
    fixType = 0
    
    def __init__(self, variable, operator, fixType):
        self.variable = variable
        self.operator = operator
        self.fixType = fixType

class ParserOperationFixParcial:
    first = 0
    second = 0

    def __init__(self, first, second):
        self.first = first
        self.second = second

class ParserOperationAssigment(ParserOperation):
    def __init__(self, first, second, operator):
        super(ParserOperationAssigment, self).__init__(first, second, operator)

class ParserLineBlock:
    def __init__(self):
        return

    @staticmethod
    def isLineBlock(object):
        return object.getValue() == '('

class ParserLineBlockUnstack:
    value = 0
    before = 0

    def __init__(self):
        self.value = 0

    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
    
    def getBefore(self):
        return self.before

    def setBefore(self, value):
        self.before = value

    @staticmethod
    def isLineBlockUnstack(object):
        return object.getValue() == ')'

class ParserKeyword:
    def __init__(self):
        return

class ParserBlock:
    block = 0
    
    def __init__(self):
        return
    
    def setBlock(self, block):
        self.block = block

    @staticmethod
    def isBlock(object):
        return object.getValue() == "{"
    
    @staticmethod
    def isCloseBlock(object):
        return object.getValue() == '}'

class ParserIf(ParserBlock):
    value = 0

    elseBlock = 0

    def __init__(self, value):
        self.value = value
        super(ParserIf, self).__init__()

    @staticmethod
    def isElseBlock(object):
        return object.getValue() == "else"

    @staticmethod
    def isIfBlock(object):
        return object.getValue() == "if"

class ParserElse(ParserBlock):
    ifBlock = 0

    def __init__(self):
        super(ParserElse, self).__init__()

class ParserWhile(ParserBlock):
    value = 0

    def __init__(self, value):
        self.value = value
        super(ParserWhile, self).__init__()
    
    @staticmethod
    def isWhileBlock(object):
        return object.getValue() == "while"

class ParserFor(ParserBlock):
    value = 0

    def __init__(self, value):
        self.value = value
        super(ParserFor, self).__init__()
    
    @staticmethod
    def isForBlock(object):
        return object.getValue() == "for"

class ParserOperatorForIn():
    value = 0

    def __init__(self, value):
        self.value = value
    
    @staticmethod
    def isInOperator(object):
        return object.getValue() == "in"

class ParserDeclarationVariable:
    variable = 0
    type = 0
    varType = 0

    def __init__(self, variable, type, varType):
        self.variable = variable
        self.type = type
        self.varType = varType
    
    @staticmethod
    def isDeclarationVariable(object):
        return VariableConstantType.isConstantType(object.getValue())

class ParserDeclarationExplicit:
    def __init__(self):
        return
    
    @staticmethod
    def isExplicit(object):
        return object.getValue() == ":"

class ParserVariableType:
    type = 0

    def __init__(self, type):
        self.type = type
    
    @staticmethod
    def isVariableType(object):
        return object.getToken() == LexerEnum.primitive
    
class ParserBreak:
    def __init__(self):
        return

    @staticmethod
    def isBreak(object):
        return object.getValue() == "break"

class ParserOperatorRange:
    operator = 0

    def __init__(self, operator):
        self.operator = operator

    @staticmethod
    def isForRange(object):
        return object.getToken() == LexerEnum.operator_range    

class ParserOperatorForRange:
    first = 0
    last = 0
    operator = 0

    def __init__(self, operator, first, last):
        self.operator = operator
        self.first = first
        self.last = last

    def isRangeMounted(self):
        return self.first and type(self.first) == ParserVariable and self.last and type(self.last) == ParserVariable and self.operator and type(self.operator) == ParserOperatorRange

class ParserForInRange:
    variable = 0
    operator = 0
    range = 0

    def __init__(self, variable, operator, range):
        self.variable = variable
        self.operator = operator
        self.range = range

class ParserEmpty:
    def __init__(self):
        return

class ParserError:
    def __init__(self):
        return

class ParserMerge:
    def merge(first, second):
        ParserMerge.printObject(first)
        ParserMerge.printObject(second)
        print()

        if type(second) == ParserError:
            return second

        if type(first) == ParserError:
            return first

        if type(second) == ParserEmpty:
            if type(first) == ParserOperator:
                return ParserError()
            return first

        if type(first) == ParserAssigment:
            if type(second) == ParserVariable:
                return ParserOperationAssigment(0, second, first)
            
            if type(second) == ParserOperation and second.first:
                return ParserOperationAssigment(0, second, first)

            if type(second) == ParserFixOperation:
                return ParserOperationAssigment(0, second, first)
        
        if type(first) == ParserOperator:
            if type(second) == ParserVariable:
                return ParserOperation(0, second, first)
                
            if type(second) == ParserFixOperation:
                return ParserOperation(0, second, first)
            
            if type(second) == ParserOperation and second.first:
                return ParserOperation(0, second, first)

        if type(first) == ParserVariable:
            if type(second) == ParserOperationAssigment:
                if not first.isStoreVariable():
                    return ParserError()
                second.first = first
                return second

            if type(second) == ParserOperation and not second.first:
                second.first = first
                return second
            
            if type(second) == ParserDeclarationVariable and type(second.variable) == ParserOperationAssigment:
                if not first.isStoreVariable():
                    return ParserError()
                second.variable = ParserMerge.merge(first, second.variable)
                return second

            if type(second) == ParserOperatorForRange and not second.first:
                second.first = first
                return second
            
            if type(second) == ParserForInRange and not second.variable:
                if not first.isStoreVariable():
                    return ParserError()

                second.variable = first
                return second
            
            if type(second) == ParserPFixOperator:
                fixType = ParserFixType.isPosfix(second)
                if fixType != ParserFixType.none:
                    return ParserFixOperation(first, second, fixType)

            if type(second) == ParserOperationFixParcial:
                if type(second.first) == ParserPFixOperator and type(second.second) == ParserOperation and not second.second.first:
                    second.second.first = ParserMerge.merge(first, second.first)
                    return second.second
        
        if type(first) == ParserLineBlock:
            if type(second) == ParserLineBlockUnstack:
                if second.getValue():
                    if type(second.getValue()) == ParserOperation and not second.getValue().first:
                        return ParserError()

                    if second.getBefore():
                        return ParserMerge.merge(second.getValue(), second.getBefore())
                    return second.getValue()
                return ParserEmpty()

        if type(second) == ParserLineBlockUnstack:
            if not second.getValue():
                second.setValue(first)
                return second
            
            second.setValue(ParserMerge.merge(first, second.getValue()))
            return second
        
        if type(first) == ParserLineBlockUnstack:
            if type(second) == ParserOperation and not second.first:
                first.setBefore(second)
                return first
        
        if type(first) == ParserOperation:
            if type(second) == ParserOperation and not second.first and first.first and first.second:
                second.first = first
                return second
            
        if type(first) == ParserPFixOperator:
            if type(second) == ParserVariable and second.isStoreVariable():
                fixType = ParserFixType.isPrefix(first)
                if fixType != ParserFixType.none:
                    return ParserFixOperation(first, second, fixType)
                
            if type(second) == ParserOperation and not second.first:
                return ParserOperationFixParcial(first, second)

        if type(first) == ParserFixOperation:
            if type(second) == ParserOperation and not second.first and second.operator and second.second:
                second.first = first
                return second

        if type(first) == ParserIf:
            if type(second) == LexerQueue:
                first.setBlock(second)
                return first

            if type(second) == ParserElse:
                first.elseBlock = second
                return first

        if type(first) == ParserElse:
            if type(second) == LexerQueue:
                first.setBlock(second)
                return first
            if type(second) == ParserIf:
                first.ifBlock = second
                return first

        if type(first) == ParserVariableType:
            if type(second) == ParserOperationAssigment:
                return ParserDeclarationVariable(second, first, 0)

        if type(first) == ParserDeclarationExplicit:
            if type(second) == ParserDeclarationVariable:
                if second.variable and second.type:
                    return second

        if type(first) == ParserWhile:
            if type(second) == LexerQueue:
                first.setBlock(second)
                return first

        if type(first) == ParserOperatorRange:
            if type(second) == ParserVariable:
                return ParserOperatorForRange(first, 0, second)

        if type(first) == ParserOperatorForIn:
            if type(second) == ParserOperatorForRange and second.isRangeMounted():
                return ParserForInRange(0, first, second)

        if type(first) == ParserFor:
            if type(second) == LexerQueue:
                first.setBlock(second)
                return first

        return ParserError()

    @staticmethod
    def printObject(object):
        if not object:
            print("_ParserMerge<" , end="")
            print(object, end="")
            print(">")
            return
        
        print("_ParserMerge" , end="")
        print(object)

class Parser:
    queue = 0

    def __init__(self, queue):
        self.queue = queue.copy()
        self.queue.needsPersist(True)

    @staticmethod
    def isEndline(object):
        return object.getToken() == LexerEnum.endline or object.getValue() == ';'
    
    @staticmethod
    def toParse(object, callback, types, notFound):
        for type in types:            
            if type == ParserLineBlockUnstack and ParserLineBlockUnstack.isLineBlockUnstack(object):
                return ParserMerge.merge(ParserLineBlockUnstack(), callback())

            if type == ParserLineBlock and ParserLineBlock.isLineBlock(object):
                return ParserMerge.merge(ParserLineBlock(), callback())
            
            if type == ParserVariable and ParserVariable.isVariable(object):
                return ParserMerge.merge(ParserVariable(object), callback())
            
            if type == ParserOperator and ParserOperator.isOperator(object):
                return ParserMerge.merge(ParserOperator(object), callback())

            if type == ParserAssigment and ParserAssigment.isAssigment(object):
                return ParserMerge.merge(ParserAssigment(object), callback())
            
            if type == ParserKeyword and Parser.isKeyword(object):
                return ParserKeyword()
            
            if type == ParserBlock and ParserBlock.isBlock(object):
                return ParserEmpty()

            if type == ParserDeclarationExplicit and ParserDeclarationExplicit.isExplicit(object):
                return ParserMerge.merge(ParserDeclarationExplicit(), callback())

            if type == ParserVariableType and ParserVariableType.isVariableType(object):
                return ParserMerge.merge(ParserVariableType(object), callback())

            if type == ParserOperatorRange and ParserOperatorRange.isForRange(object):
                return ParserMerge.merge(ParserOperatorRange(object), callback())

            if type == ParserOperatorForIn and ParserOperatorForIn.isInOperator(object):
                return ParserMerge.merge(ParserOperatorForIn(object), callback())
            
            if type == ParserPFixOperator and ParserPFixOperator.isPFixOperator(object):
                return ParserMerge.merge(ParserPFixOperator(object), callback())
            
        return notFound()

    def execute(self):
        if self.queue.isEmpty():
            return ParserEmpty()
    
        object = self.queue.getHead()
        self.queue.toRight()
        
        if Parser.isEndline(object):
            return ParserEmpty()

        parsed = Parser.toParse(object, self.execute, [
            ParserLineBlockUnstack,
            ParserLineBlock,
            ParserVariable,
            ParserOperator,
            ParserPFixOperator,
            ParserAssigment,
            ParserKeyword,
        ], ParserError)
        
        if type(parsed) == ParserKeyword:
            return Parser.keywordMerge(self.executeKeyword(object), self.execute)

        return parsed

    def executeKeyword(self, keyword):
        if ParserIf.isIfBlock(keyword):
            return self.isIfValid(Parser.isMergeValid(self.blockIf()))
        
        if ParserBreak.isBreak(keyword):
            return ParserBreak()

        if ParserWhile.isWhileBlock(keyword):
            return self.isWhileValid(Parser.isMergeValid(self.blockIf()))

        if ParserFor.isForBlock(keyword):
            return self.isForValid(Parser.isMergeValid(self.blockFor()))
        
        if ParserDeclarationVariable.isDeclarationVariable(keyword):
            return self.isDeclarationValid(keyword, Parser.isMergeValid(self.declarationLine()))

    # ParserDeclarationVariable
    # ParserOperationAssigment
    def isDeclarationValid(self, keyword, merged):
        if type(merged) == ParserOperationAssigment:
            return ParserDeclarationVariable(merged, VariableDeclarationCast.auto, VariableConstantType.toConstantType(keyword))
        if type(merged) == ParserDeclarationVariable:
            merged.varType = VariableConstantType.toConstantType(keyword)
            return merged

        return ParserError()

    def isWhileValid(self, merged):
        if type(merged) == ParserError:
            return merged
        
        if type(merged) == ParserEmpty:
            return ParserError()

        return ParserMerge.merge(ParserWhile(merged), self.block())
    
    def isForValid(self, merged):
        if type(merged) == ParserError:
            return merged
        
        if type(merged) == ParserEmpty:
            return ParserError()

        if type(merged) != ParserForInRange:
            return ParserError()

        return ParserMerge.merge(ParserFor(merged), self.block())        

    def isIfValid(self, merged):
        if type(merged) == ParserError:
            return merged
        
        if type(merged) == ParserEmpty:
            return ParserError()

        merged = ParserMerge.merge(ParserIf(merged), self.block())
        
        if type(merged) == ParserIf:
            if ParserIf.isElseBlock(self.queue.getHead()):
                self.queue.toRight()

                if ParserBlock.isBlock(self.queue.getHead()):
                    self.queue.toRight()
                    return ParserMerge.merge(merged, ParserMerge.merge(ParserElse(), self.block()))
                
                if ParserIf.isIfBlock(self.queue.getHead()):
                    self.queue.toRight()
                    return ParserMerge.merge(merged, ParserMerge.merge(ParserElse(), self.isIfValid(Parser.isMergeValid(self.blockIf()))))
                
                return ParserError()

        return merged

    def blockIf(self):
        if self.queue.isEmpty():
            return ParserError()
    
        object = self.queue.getHead()
        self.queue.toRight()

        return Parser.toParse(object, self.blockIf, [
            ParserBlock,
            ParserLineBlockUnstack,
            ParserLineBlock,
            ParserVariable,
            ParserOperator,
            ParserPFixOperator
        ], ParserError)

    def blockFor(self):
        if self.queue.isEmpty():
            return ParserError()
    
        object = self.queue.getHead()
        self.queue.toRight()

        return Parser.toParse(object, self.blockFor, [
            ParserBlock,
            ParserVariable,
            ParserOperatorRange,
            ParserOperatorForIn
        ], ParserError)

    def declarationLine(self):    
        if self.queue.isEmpty():
            return ParserEmpty()
    
        object = self.queue.getHead()
        self.queue.toRight()

        if Parser.isEndline(object):
            return ParserEmpty()

        return Parser.toParse(object, self.declarationLine, [
            ParserLineBlockUnstack,
            ParserLineBlock,
            ParserVariable,
            ParserDeclarationExplicit,
            ParserVariableType,
            ParserOperator,
            ParserPFixOperator,
            ParserAssigment
        ], ParserError)
        
    def block(self):
        object = self.queue.getHead()
        instructions = LexerQueue()

        while object and not ParserBlock.isCloseBlock(object):
            line = Parser.isMergeValid(self.execute())
            
            if type(line) == ParserError:
                instructions = line
                break

            if type(line) != ParserEmpty:
                instructions.insert(line)

            object = self.queue.getHead()

        if not object:
            return ParserError()

        self.queue.toRight()
        return instructions        
        
    @staticmethod
    def isKeyword(object):
        return object.getToken() == LexerEnum.keyword

    @staticmethod
    def notAccepted(merged, types):
        for _type in types:
            if type(merged) == _type:
                return ParserError()
            
        return ParserEmpty()

    @staticmethod
    def isMergeValid(merged):
        if type(merged) == ParserOperation and not merged.first:
            return ParserError()

        if type(merged) == ParserOperationAssigment and not merged.first:
            return ParserError()
        
        notAccepted = Parser.notAccepted(merged, [
            ParserOperationFixParcial,
            ParserPFixOperator,
            ParserLineBlockUnstack,
            ParserLineBlock,
        ])
        
        if type(notAccepted) == ParserError:
            return notAccepted

        return merged
    
    @staticmethod
    def keywordMerge(merged, callback):
        if type(merged) == ParserDeclarationVariable:
            return merged

        return ParserMerge.merge(merged, callback())

    @staticmethod
    def run():
        parser = Parser(LexerQueue.shared())
        instructions = LexerQueue()

        while not parser.queue.isEmpty():
            line = Parser.isMergeValid(parser.execute())
            if type(line) == ParserError:
                print(line)
                quit()
                break

            instructions.insert(line)
        
        print("Lista de Instruções")
        instructions.verbose(showContent=False)
        quit()

def compareToken(object, values):
    return LexerEnum.compare(object, values)