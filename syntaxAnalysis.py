import csv
from SymbolTable import *
from lexicalAnalyser import *


class Parser:
    def __init__(self, parsing_table_file):
        self.parsing_table = self.load_parsing_table(parsing_table_file)
        self.state_stack = [0]
        self.input_stack = []
        #{identifier, value}
        self.symbol_table = {}
        self.current_expression_value = None
        self.current_variable_stack = []
        #print(self.parsing_table)

    def load_parsing_table(self, parsing_table_file):
        parsing_table = {}
        with open(parsing_table_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for row in reader:
                state = int(row[0])
                parsing_table[state] = {}
                for index, action in enumerate(row[0:]):
                    if action:
                        parsing_table[state][headers[index]] = action
        return parsing_table

    def parse(self, tokens):
        self.input_stack = tokens
        while self.input_stack:
            
            current_token_data = self.input_stack[0]
            current_token = current_token_data['label']

            if current_token == "REJECTED":
                self.error(f"Syntax error at line {current_token_data['line']}: {current_token_data['identifier']}")
                return
            current_state = self.state_stack[-1]
            #print(current_state)

            #GAMBIARRA FEIA
            if current_token == 'var':
                self.current_variable_stack.append(current_token_data)

            action = self.parsing_table.get(current_state, {}).get(current_token, None)
            if action is None:
                self.error(f"Unexpected token {current_token} at line {current_token_data['line']}")
                return
            #print(action)

            if action.startswith('s'):
                self.shift(int(action[1:]))
            elif action.startswith('r'):
                if not self.reduce(int(action[1:])):
                    return
            elif action == 'acc':
                print("Input accepted.")
                #print(self.symbol_table.table)
                return
            else:
                self.error(f"Invalid action {action}")
                return

    def shift(self, state):
        self.state_stack.append(state)
        token = self.input_stack.pop(0)
        #print(token)
        #self.symbol_table.add_symbol(token, {'line': self.current_line})

    def reduce(self, production):
        if production == 0:
            # E' -> S
            self.state_stack.pop()  # Pop S
            self.state_stack.append(self.goto(self.state_stack[-1], 'E\''))

        elif production == 1:
            # S -> epsilon
            self.state_stack.append(self.goto(self.state_stack[-1], 'S'))
            pass

        elif production == 2:
            # S -> E S
            self.state_stack.pop()  # Pop S
            self.state_stack.pop()  # Pop E
            self.state_stack.append(self.goto(self.state_stack[-1], 'S'))

        elif production == 3:
            # S -> C S
            self.state_stack.pop()  # Pop S
            self.state_stack.pop()  # Pop C
            self.state_stack.append(self.goto(self.state_stack[-1], 'S'))

        elif production == 4:
            # E -> let var = E ;
            self.state_stack.pop()  # Pop ;
            self.state_stack.pop()  # Pop E
            self.state_stack.pop()  # Pop =
            self.state_stack.pop()  # Pop var
            self.state_stack.pop()  # Pop let
            self.state_stack.append(self.goto(self.state_stack[-1], 'E'))

            #add var id to the self.symbol_table if ti doesnt exist
            current_variable_data = self.current_variable_stack.pop()
            current_variable = current_variable_data['identifier']
            if current_variable in self.symbol_table.keys():
                self.error(f"Tried to Reassign variable at line {current_variable_data['line']}")
                return False
            else:
                self.symbol_table[current_variable] = self.current_expression_value

                
        elif production == 5:
            # E -> true
            self.state_stack.pop()  # Pop true
            self.state_stack.append(self.goto(self.state_stack[-1], 'E'))
            #current_expression_value = true
            self.current_expression_value = True

        elif production == 6:
            # E -> false
            self.state_stack.pop()  # Pop false
            self.state_stack.append(self.goto(self.state_stack[-1], 'E'))
            #current_expression_value = false
            self.current_expression_value = False

        elif production == 7:
            # E -> var
            self.state_stack.pop()  # Pop var
            self.state_stack.append(self.goto(self.state_stack[-1], 'E'))

            #if var not in self.table throw error
            current_variable_data = self.current_variable_stack.pop()
            current_variable = current_variable_data['identifier']
            if current_variable in self.symbol_table.keys():
                self.current_expression_value = self.symbol_table[current_variable]
            else:
                self.error(f"Tried to Invoke No Declared Variable at line {current_variable_data['line']}")
                return False


            #current_expression_value = var -> value

        elif production == 8:
            # C -> if E { E }
            self.state_stack.pop()  # Pop }
            self.state_stack.pop()  # Pop E
            self.state_stack.pop()  # Pop {
            self.state_stack.pop()  # Pop E
            self.state_stack.pop()  # Pop if
            self.state_stack.append(self.goto(self.state_stack[-1], 'C'))

        return True

    def goto(self, state, symbol):
        # This function will return the new state after a reduction.
        action = self.parsing_table.get(state, {}).get(symbol, None)
        if action is None:
            self.error(f"Unexpected goto {symbol}")
            return state
        return int(action)

    def error(self, message):
        print(f"Syntax Error: {message}")

# Example usage
#tokens path
path = "entradas/tokens/t1.txt"
parsing_table_file = 'parsing_table.csv'
automato = AFD("entradas/in")

lexer = Lexer(automato)
tokens = lexer.processTokens(path)

parser = Parser(parsing_table_file)
parser.parse(tokens)

print(parser.symbol_table)

