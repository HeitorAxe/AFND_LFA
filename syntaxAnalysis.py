import csv

# Define a symbol table class
class SymbolTable:
    def __init__(self):
        self.table = {}

    def add_symbol(self, token, attributes):
        self.table[token] = attributes

    def get_symbol(self, token):
        return self.table.get(token, None)

    def update_symbol(self, token, attributes):
        if token in self.table:
            self.table[token].update(attributes)

class Parser:
    def __init__(self, parsing_table_file):
        self.parsing_table = self.load_parsing_table(parsing_table_file)
        self.symbol_table = SymbolTable()
        self.state_stack = [0]
        self.input_stack = []
        self.current_line = 1

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
            current_token = self.input_stack[0]
            current_state = self.state_stack[-1]
            #print(current_state, current_token)
            if current_token == '\n':
                self.current_line += 1
                self.input_stack.pop(0)
                continue
            action = self.parsing_table.get(current_state, {}).get(current_token, None)
            #print(action)
            if action is None:
                self.error(f"Unexpected token {current_token}")
                return

            if action.startswith('s'):
                self.shift(int(action[1:]))
            elif action.startswith('r'):
                self.reduce(int(action[1:]))
            elif action == 'acc':
                print("Input accepted.")
                print(self.symbol_table.table)
                return
            else:
                self.error(f"Invalid action {action}")
                return

    def shift(self, state):
        self.state_stack.append(state)
        token = self.input_stack.pop(0)
        self.symbol_table.add_symbol(token, {'line': self.current_line})

    def reduce(self, production):
        if production == 0:
            # E' -> S
            self.state_stack.pop()  # Pop S
            self.state_stack.append(self.goto(self.state_stack[-1], 'E\''))

        elif production == 1:
            # S -> E S
            self.state_stack.pop()  # Pop S
            self.state_stack.pop()  # Pop E
            self.state_stack.append(self.goto(self.state_stack[-1], 'S'))

        elif production == 2:
            # S -> epsilon
            self.state_stack.append(self.goto(self.state_stack[-1], 'S'))
            pass

        elif production == 3:
            # E -> let A
            self.state_stack.pop()  # Pop A
            self.state_stack.pop()  # Pop let
            self.state_stack.append(self.goto(self.state_stack[-1], 'E'))

        elif production == 4:
            # E -> true
            self.state_stack.pop()  # Pop true
            self.state_stack.append(self.goto(self.state_stack[-1], 'E'))

        elif production == 5:
            # E -> false
            self.state_stack.pop()  # Pop false
            self.state_stack.append(self.goto(self.state_stack[-1], 'E'))

        elif production == 6:
            # E -> if C
            self.state_stack.pop()  # Pop C
            self.state_stack.pop()  # Pop if
            self.state_stack.append(self.goto(self.state_stack[-1], 'E'))

        elif production == 7:
            # E -> var
            self.state_stack.pop()  # Pop var
            self.state_stack.append(self.goto(self.state_stack[-1], 'E'))

        elif production == 8:
            # A -> var = E ;
            self.state_stack.pop()  # Pop ;
            self.state_stack.pop()  # Pop E
            self.state_stack.pop()  # Pop =
            self.state_stack.pop()  # Pop var
            self.state_stack.append(self.goto(self.state_stack[-1], 'A'))

        elif production == 9:
            # C -> E { E }
            self.state_stack.pop()  # Pop }
            self.state_stack.pop()  # Pop E
            self.state_stack.pop()  # Pop {
            self.state_stack.pop()  # Pop E
            self.state_stack.append(self.goto(self.state_stack[-1], 'C'))

    def goto(self, state, symbol):
        # This function will return the new state after a reduction.
        action = self.parsing_table.get(state, {}).get(symbol, None)
        if action is None:
            self.error(f"Unexpected goto {symbol}")
            return state
        return int(action)

    def error(self, message):
        print(f"Syntax Error on line {self.current_line}: {message}")

# Example usage
parsing_table_file = 'parsing_table.csv'
tokens = ['let', 'var', '=', 'true', ';', '\n', 'let', 'var', '=', 'false', ';', '$']
parser = Parser(parsing_table_file)
parser.parse(tokens)

