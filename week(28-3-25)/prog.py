from collections import defaultdict
import re


class SLRParser:
    def __init__(self):
        self.grammar = {}
        self.terminals = set()
        self.non_terminals = set()
        self.lr0_items = []
        self.action_table = defaultdict(dict)
        self.goto_table = defaultdict(dict)
        self.reductions = {}
        self.start_symbol = None


    def input_grammar(self):
        n = int(input("Enter number of productions: "))
        for _ in range(n):
            line = input("Enter production (e.g., A->BC|a): ").replace(" ", "")
            lhs, rhs = line.split("->")
            rhs = rhs.split("|")
            self.grammar[lhs] = [list(self.tokenize_symbols(r)) for r in rhs]
            self.non_terminals.add(lhs)


            for production in rhs:
                for symbol in self.tokenize_symbols(production):
                    if symbol.islower() or not symbol.isalpha():
                        self.terminals.add(symbol)


        self.start_symbol = list(self.grammar.keys())[0]
        self.terminals.add("$")


        augmented_start = self.start_symbol + "'"
        self.grammar[augmented_start] = [[self.start_symbol]]
        self.start_symbol = augmented_start
        self.non_terminals.add(augmented_start)


    def tokenize_symbols(self, production):
        return re.findall(r'[A-Z]+|.', production)


    def generate_lr0_items(self):
        def closure(items):
            closure_set = set(items)
            added = True


            while added:
                added = False
                new_items = set(closure_set)


                for lhs, production, dot_pos in closure_set:
                    if dot_pos < len(production):
                        symbol = production[dot_pos]
                        if symbol in self.non_terminals:
                            for rule in self.grammar[symbol]:
                                item = (symbol, tuple(rule), 0)
                                if item not in new_items:
                                    new_items.add(item)
                                    added = True


                closure_set = new_items


            return closure_set


        def goto(state, symbol):
            next_state = set()
            for lhs, production, dot_pos in state:
                if dot_pos < len(production) and production[dot_pos] == symbol:
                    next_state.add((lhs, production, dot_pos + 1))
            return closure(next_state)


        start_item = (self.start_symbol, tuple(self.grammar[self.start_symbol][0]), 0)
        self.lr0_items = [closure({start_item})]
        states_map = {frozenset(self.lr0_items[0]): 0}


        index = 0
        while index < len(self.lr0_items):
            state = self.lr0_items[index]
            symbols = set()


            for lhs, production, dot_pos in state:
                if dot_pos < len(production):
                    symbols.add(production[dot_pos])


            for symbol in symbols:
                next_state = goto(state, symbol)
                if next_state and frozenset(next_state) not in states_map:
                    states_map[frozenset(next_state)] = len(self.lr0_items)
                    self.lr0_items.append(next_state)


            index += 1


        for state_index, state in enumerate(self.lr0_items):
            for lhs, production, dot_pos in state:
                if dot_pos < len(production):
                    symbol = production[dot_pos]
                    next_state = goto(state, symbol)
                    if symbol in self.terminals:
                        self.action_table[state_index][symbol] = f"S{states_map[frozenset(next_state)]}"
                    else:
                        self.goto_table[state_index][symbol] = states_map[frozenset(next_state)]
                else:
                    if lhs == self.start_symbol:
                        self.action_table[state_index]['$'] = 'ACC'
                    else:
                        rule_num = len(self.reductions) + 1
                        self.reductions[rule_num] = (lhs, production)
                        follow_set = self.compute_follow(lhs)
                        for terminal in follow_set:
                            self.action_table[state_index][terminal] = f"R{rule_num}"


    def compute_follow(self, symbol):
        follow_set = set()
        if symbol == self.start_symbol:
            follow_set.add("$")


        for lhs, productions in self.grammar.items():
            for production in productions:
                for i, sym in enumerate(production):
                    if sym == symbol:
                        if i + 1 < len(production):
                            next_sym = production[i + 1]
                            if next_sym in self.terminals:
                                follow_set.add(next_sym)
                        else:
                            follow_set |= self.compute_follow(lhs)
        return follow_set


    def print_parsing_table(self):
        print("\nParsing Table:")
        headers = sorted(self.terminals | (self.non_terminals - {self.start_symbol}))
        print(f"{'State':<8} " + " ".join(f"{h:<8}" for h in headers))
        print("-" * (10 + 9 * len(headers)))


        for state in sorted(self.action_table.keys() | self.goto_table.keys()):
            row = [f"{state:<8}"]
            for symbol in headers:
                value = self.action_table.get(state, {}).get(symbol, self.goto_table.get(state, {}).get(symbol, ""))
                row.append(f"{str(value):<8}")
            print(" ".join(row))


    def parse_input(self):
        input_string = self.tokenize_symbols(input("\nEnter input string to parse: ")) + ["$"]
        stack = [(0, "")]  # Track states with symbols
        pointer = 0


        print("\nParsing Steps:")
        print(f"{'Stack':<30} {'Input':<20} {'Action':<20}")
        print("-" * 70)


        while True:
            state, symbol = stack[-1]
            current_input = input_string[pointer]
            action = self.action_table.get(state, {}).get(current_input, "ERROR")
            print(f"${''.join([f'{s[1]}{s[0]}' for s in stack]):<30} {''.join(input_string[pointer:]):<20} {action:<20}")
            if action == "ERROR":
                print("\nParsing error! String Rejected.")
                return False
            if "S" in action:
                new_state = int(action[1:])
                stack.append((new_state, current_input))
                pointer += 1
            elif action.startswith("R"):
                rule_num = int(action[1:])
                lhs, rhs = self.reductions[rule_num]
                for _ in range(len(rhs)):
                    stack.pop()
                top_state = stack[-1][0]
                stack.append((self.goto_table[top_state][lhs], lhs))
            elif action == "ACC":
                print("\nString Accepted.")
                return True
            else:
                print("\nParsing error! String Rejected.")
                return False


# Run the parser
parser = SLRParser()
parser.input_grammar()
parser.generate_lr0_items()
parser.print_parsing_table()
parser.parse_input()
