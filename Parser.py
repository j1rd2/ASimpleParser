from Lexer import *
from Translator import *

class Parser:
	lex = None
	token = None

	def __init__(self, filepath):
		self.lex = Lexer(filepath)
		self.token = None

		""" DEFINE FIRST SET """
		self.firstPrimaryExpression = set((Tag.ID, Tag.NUMBER, Tag.TRUE, Tag.FALSE, ord('(')))
		self.firstUnaryExpression = self.firstPrimaryExpression.union( set((ord('-'), ord('!'))) )
		self.firstExtendedMultiplicativeExpression = set((ord('*'), ord('/'), Tag.MOD))
		self.firstMultiplicativeExpression = self.firstUnaryExpression
		self.firstExtendedAdditiveExpression = set((ord('+'), ord('-')))
		self.firstAdditiveExpression = self.firstMultiplicativeExpression
		self.firstExtendedRelationalExpression = set((ord('<'), Tag.LEQ, ord('>'), Tag.GEQ))
		self.firstRelationalExpression = self.firstAdditiveExpression
		self.firstExtendedEqualityExpression = set((ord('='), Tag.NEQ))
		self.firstEqualityExpression = self.firstRelationalExpression
		self.firstExtendedConditionalTerm = set({Tag.AND})
		self.firstConditionalTerm = self.firstEqualityExpression
		self.firstExtendedConditionalExpression = set({Tag.OR})
		self.firstConditionalExpression = self.firstConditionalTerm
		self.firstExpression = self.firstConditionalExpression
		self.firstTextStatement = set({Tag.PRINT})
		self.firstAssigmentStatement = set({Tag.ID})
		self.firstStatement = self.firstAssigmentStatement.union(self.firstTextStatement)
		self.firstStatementSequence = self.firstStatement
		self.firstIdentifierList = set({ord(',')})
		self.firstDeclarationSequence = set({Tag.VAR})
		self.firstProgram = self.firstDeclarationSequence

	def error(self, extra = None):
		text = 'Line ' + str(self.lex.line) + " - " 
		if extra == None:
			text = text + "."
		else:
			text = text + extra
		raise Exception(text)

	def check(self, tag):
		if self.token.tag == tag:
			self.token = self.lex.scan()
			#print("", self.token)
		else:
			text = 'expected '
			if self.token.tag != Tag.ID:
				#print("tag = ", self.token.tag)
				aux = Token(tag)
				text = text + str(aux) + " before " + str(self.token) 
			else:
				text = text + "an identifier before " + str(self.token) 
			self.error(text)
	
	def analize(self):
		self.token = self.lex.scan()
		ast = self.program()
		if self.token.tag == Tag.EOF:
			print("ACCEPTED")
			return ast
		else:
			self.error("unexpected token " + str(self.token))
	
	#<primary-expression> ::= <identifier> || <number> || <true>	|| <false> ||  '(' <expression> ')'
	def primaryExpression(self):
		if self.token.tag in self.firstPrimaryExpression:
			if self.token.tag == Tag.ID:
				name = self.token.value
				line = self.lex.line
				self.check(Tag.ID)
				return Identifier(name, line)
			
			elif self.token.tag == Tag.NUMBER:
				value = self.token.value
				self.check(Tag.NUMBER)
				return Number(value)
			
			elif self.token.tag == Tag.TRUE:
				self.check(Tag.TRUE)
				return Boolean(True)
			
			elif self.token.tag == Tag.FALSE:
				self.check(Tag.FALSE)
				return Boolean(False)
			
			elif self.token.tag == ord('('):
				self.check(ord('('))
				node = self.expression()
				self.check(ord(')'))
				return node
		else:
			self.error("expected a primary expression before " + str(self.token)) 

	#<unary-expression> ::= '-' <unary-expression> || '!' <unary-expression> || <primary-expression>
	def unaryExpression(self):
		if self.token.tag in self.firstUnaryExpression:
			if self.token.tag == ord('-'):
				self.check(ord('-'))
				right = self.unaryExpression()
				return Minus(right)
			
			elif self.token.tag == ord('!'):
				self.check(ord('!'))
				right = self.unaryExpression()
				return Not(right)
			
			else:
				return self.primaryExpression()
		else: 
			self.error("expected an unary expression before " + str(self.token))

	#<extended-multiplicative-expression> ::= '*' <unary-expression> <extended-multiplicative-expression>
	#<extended-multiplicative-expression> ::= '/' <unary-expression> <extended-multiplicative-expression>
	#<extended-multiplicative-expression> ::= MOD <unary-expression> <extended-multiplicative-expression>
	#<extended-multiplicative-expression> ::= ' '
	def extendedMultiplicativeExpression(self):
		if self.token.tag in self.firstExtendedMultiplicativeExpression:
			if self.token.tag == ord('*'):
				self.check(ord('*'))
				self.unaryExpression()
				self.extendedMultiplicativeExpression()
				
			elif self.token.tag == ord('/'):
				self.check(ord('/'))
				self.unaryExpression()
				self.extendedMultiplicativeExpression()

			elif self.token.tag == Tag.MOD:
				self.check(Tag.MOD)
				self.unaryExpression()
				self.extendedMultiplicativeExpression()
		else:
			pass

	#<multiplicative-expression> ::= <unary-expression> <extended-multiplicative-expression>
	def multiplicativeExpression(self):
		if self.token.tag in self.firstMultiplicativeExpression:
			node = self.unaryExpression() # node=left because unaryExp parses the first character

			while self.token.tag in self.firstExtendedMultiplicativeExpression:
				if self.token.tag == ord('*'):
					self.check(ord('*'))
					right = self.unaryExpression()
					node = Multiply(node, right)

				elif self.token.tag == ord('/'):
					self.check(ord('/'))
					right = self.unaryExpression()
					node = Divide(node, right)

				elif self.token.tag == Tag.MOD:
					self.check(Tag.MOD)
					right = self.unaryExpression()
					node = Mod(node, right)
			return node
		else:
			self.error("expected an multiplicative expression before " + str(self.token))

	#<extended-additive-expression> ::= '+' <multiplicative-expression> <extended-additive-expression>
	#<extended-additive-expression> ::= '-' <multiplicative-expression> <extended-additive-expression>
	#<extended-additive-expression> ::= ' '
	def extendedAdditiveExpression(self):
		if self.token.tag in self.firstExtendedAdditiveExpression:
			if self.token.tag == ord('+'):
				self.check(ord('+'))
				self.multiplicativeExpression()
				self.extendedAdditiveExpression()
			elif self.token.tag == ord('-'):
				self.check(ord('-'))
				self.multiplicativeExpression()
				self.extendedAdditiveExpression()
		else:
			pass

	#<additive-expression> ::= <multiplicative-expression> <extended-additive-expression>
	def additiveExpression(self):
		if self.token.tag in self.firstAdditiveExpression:
			node = self.multiplicativeExpression()

			while self.token.tag in self.firstExtendedAdditiveExpression:
				if self.token.tag == ord('+'):
					self.check(ord('+'))
					right = self.multiplicativeExpression();
					node = Add(node, right)
				
				elif self.token.tag == ord('-'):
					self.check(ord('-'))
					right = self.multiplicativeExpression();
					node = Substract(node, right)

			return node
		else:
			self.error("expected an additive expression before " + str(self.token))


	#<extended-relational-expression> := '<' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> ::= '<''=' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> := '>' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> ::= '>''=' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> ::= ' '
	def extendedRelationalExpression(self):
		if self.token.tag in self.firstExtendedRelationalExpression:
			if self.token.tag == ord('<'):
				self.check(ord('<'))
				self.additiveExpression()
				self.extendedRelationalExpression()
			elif self.token.tag == ord('>'):
				self.check(ord('>'))
				self.additiveExpression()
				self.extendedRelationalExpression()
			elif self.token.tag == Tag.LEQ:
				self.check(Tag.LEQ)
				self.additiveExpression()
				self.extendedRelationalExpression()
			elif self.token.tag == Tag.GEQ:
				self.check(Tag.GEQ)
				self.additiveExpression()
				self.extendedRelationalExpression()
		else:
			pass
	
	#<relational-expression> ::= <additive-expression> <extended-relational-expression>
	def relationalExpression(self):
		if self.token.tag in self.firstAdditiveExpression:
			node = self.additiveExpression()
		
			while self.token.tag in self.firstExtendedRelationalExpression:
				if self.token.tag == ord('<'):
					self.check(ord('<'))
					right = self.additiveExpression()
					node = LessThan(node,right)
				elif self.token.tag == Tag.LEQ:
					self.check(Tag.LEQ)
					right = self.additiveExpression()
					node = LessEqual(node,right)
				elif self.token.tag == ord('>'):
					self.check(ord('>'))
					right = self.additiveExpression()
					node = GreaterThan(node,right)
				elif self.token.tag == Tag.GEQ:
					self.check(Tag.GEQ)
					right = self.additiveExpression()
					node = GreaterEqual(node,right)
			return node
		else:
			self.error("expected relational expression before " + str(self.token))


	#<extended-equality-expression> := '=' <relational-expression> <extended-equality-expression>
	#<extended-equality-expression> := '<''>' <relational-expression> <extended-equality-expression>
	#<extended-equality-expression> ::= ' '
	def extendedEqualityExpression(self):
		if self.token.tag in self.firstExtendedEqualityExpression:
			if self.token.tag == ord('='):
				self.check(ord('='))
				self.relationalExpression()
				self.extendedEqualityExpression()
			elif self.token.tag == Tag.NEQ:
				self.check(Tag.NEQ)
				self.relationalExpression()
				self.extendedEqualityExpression()
		else:
			pass

	#<equality-expression> ::= <relational-expression> <extended-equality-expression>
	def equalityExpression(self):
		if self.token.tag in self.firstEqualityExpression:
			node = self.relationalExpression()

			while self.token.tag in self.firstExtendedEqualityExpression:
				if self.token.tag == ord('='):
					self.check(ord('='))
					right = self.relationalExpression()
					node = Equal(node, right)
		
				elif self.token.tag == Tag.NEQ:
					self.check(Tag.NEQ)
					right = self.relationalExpression()
					node = NotEqual(node, right)
			return node 
		else:
			self.error("expected an equality expression before " + str(self.token))

	#<extended-conditional-term> ::= AND <equality-expression> <extended-conditional-term>
	#<extended-boolean-term> ::= ' '
	def extendedConditionalTerm(self):
		if self.token.tag in self.firstExtendedConditionalTerm:
			if self.token.tag == Tag.AND:
				self.check(Tag.AND)
				self.equalityExpression()
				self.extendedConditionalTerm()
		else:
			pass

	#<conditional-term> ::= <equality-expression> <extended-conditional-term>
	def conditionalTerm(self):
		if self.token.tag in self.firstConditionalTerm:
			node = self.equalityExpression()

			while self.token.tag in self.firstExtendedConditionalTerm:
				if self.token.tag == Tag.AND:
					self.check(Tag.AND)
					right = self.equalityExpression()
					node = And(node, right)

			return node
		else:
			self.error("expected an conditional term before " + str(self.token))

	#<extended-conditional-expression> ::= OR <conditional-term> <extended-conditional-expression>
	#<extended-conditional-expression> ::= ' '
	def extendedConditionalExpression(self):
		if self.token.tag in self.firstExtendedConditionalExpression:
			if self.token.tag == Tag.OR:
				self.check(Tag.OR)
				self.conditionalTerm()
				self.extendedConditionalExpression()
		else:
			pass

	#<conditional-expression> ::= <conditional-term> <extended-conditional-expression>
	def conditionalExpression(self):
		if self.token.tag in self.firstConditionalExpression:
			node = self.conditionalTerm()

			while self.token.tag in self.firstExtendedConditionalExpression:
				if self.token.tag == Tag.OR:
					self.check(Tag.OR)
					right = self.conditionalTerm()
					node = Or(node, right)

			return node
		else:
			self.error("expected an conditional expression before " + str(self.token))

	#<expression> ::= <conditional-expression>
	def expression(self):
		if self.token.tag in self.firstExpression:
			return self.conditionalExpression()
		else:
			self.error("expected an expression before " + str(self.token))

	#<text-statement> ::= PRINT '(' <expression> )'
	def textStatement(self):
		if self.token.tag in self.firstTextStatement:
			if self.token.tag == Tag.PRINT:
				self.check(Tag.PRINT)
				self.check(ord('('))
				expression = self.expression()
				self.check(ord(')'))
				return Print(expression)
		else:
			self.error("expected a text statement before " + str(self.token))

	#<assigment-statement> ::= <identifier> ':''=' <expression>
	def assigmentStatement(self):
		if self.token.tag in self.firstAssigmentStatement:
			if self.token.tag == Tag.ID:
				name = self.token.value
				line = self.lex.line
				self.check(Tag.ID)
				self.check(Tag.ASSIGN)
				expression = self.expression()
				return Assignment(name, expression, line)
		else:
			self.error("expected a assigment statement before " + str(self.token))
	
	#<statement> ::= <assignment-statement> | <text-statement>
	def statement(self):
		if self.token.tag in self.firstStatement:
			if self.token.tag in self.firstAssigmentStatement:
				return self.assigmentStatement()
			elif self.token.tag in self.firstTextStatement:
				return self.textStatement()
		else: 
			self.error("expected a statement before " + str(self.token))
	
	#<statement-sequence> ::= <statement> <statement-sequence>
	#<statement-sequence> ::= ' '
	def statementSequence(self):
		statements = []

		while self.token.tag in self.firstStatementSequence:
			statement = self.statement()
			statements.append(statement)
		return statements

	
	#<identifier-list> ::= ',' <identifier> <identifier-list>
	#<identifier-list> ::= ' '
	def identifierList(self):
		names = []

		while self.token.tag in self.firstIdentifierList:
			self.check(ord(','))
			name = self.token.value
			self.check(Tag.ID)
			names.append(name)

		return names

	#<declaration-sequence> ::= VAR <identifier> <identifier-list>
	def declarationSequence(self):
		if self.token.tag in self.firstDeclarationSequence:
			if self.token.tag == Tag.VAR:
				line = self.lex.line
				self.check(Tag.VAR)

				first = self.token.value
				self.check(Tag.ID)

				rest = self.identifierList()
				names = [first] + rest

				return VarDeclaration(names, line)
		else: 
			self.error("expected a declaration sequence before " + str(self.token))

	#<program> ::= <declaration-sequence> <statement-sequence>
	def program(self):
		if self.token.tag in self.firstProgram:
			declaration = self.declarationSequence()
			statements = self.statementSequence()
			return Program([declaration]+statements)
		else: 
			self.error("expected a program before " + str(self.token))
