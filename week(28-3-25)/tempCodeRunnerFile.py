from collections import defaultdict

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
        """ Takes grammar input from the user and augments it. """
        n = int(input("Enter number of productions: "))
        print("Enter the productions (use '|' for multiple rules, space-separated):")
        
        for _ in range(n):
            line = input().strip().split("->")
            lhs = line[0].strip()
            rhs = line[1].strip().split("|")
            self.grammar[lhs] = [r.strip().split() for r in rhs]
            self.non_terminals.add(lhs)

            for production in rhs:
                for symbol in production.split():
                    if not symbol.isupper():
                        self.terminals.add(symbol)

        self.start_symbol = list(self.grammar.keys())[0]
        self.terminals.add("$")  

        # Augment the grammar
        augmented_start = self.start_symbol + "'"
        self.grammar[augmented_start] = [[self.start_symbol]]
        self.start_symbol = augmented_start
        self.non_terminals.add(augmented_start)

    def generate_lr0_items(self):
        """ Generate LR(0) items from the grammar. """
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
        """ Compute FOLLOW set for a given non-terminal. """
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
        """ Print the parsing table in a structured format. """
        terminals = sorted(self.terminals)
        non_terminals = sorted(self.non_terminals)
        headers = ["State"] + terminals + non_terminals

        print(f"\n{'State':<8}", end="")
        for header in headers[1:]:
            print(f"{header:^8}", end="")
        print("\n" + "-" * (8 + 9 * len(headers[1:])))

        for state in sorted(set(self.action_table.keys()).union(set(self.goto_table.keys()))):
            print(f"{state:<8}", end="")

            for terminal in terminals:
                action = self.action_table.get(state, {}).get(terminal, "")
                print(f"{action:^8}", end="")

            for non_terminal in non_terminals:
                goto = self.goto_table.get(state, {}).get(non_terminal, "")
                if goto:
                    goto = f"G{goto}"
                print(f"{goto:^8}", end="")

            print()

    def parse_input(self):
        """ Parse a given input string step-by-step like the handwritten example. """
        input_string = input("\nEnter input string to parse: ") + "$"
        stack = [0]
        pointer = 0

        print(f"\n{'Stack':<20} {'T/P':<20} {'Action':<20} {'Goto':<20} {'Passes Action'}")
        print("-" * 100)

        step = 1

        while True:
            state = stack[-1]
            symbol = input_string[pointer]

            if symbol in self.action_table[state]:
                action = self.action_table[state][symbol]
                stack_content = "$" + "".join(str(s) for s in stack)
                remaining_input = input_string[pointer:]
                goto_state = ""

                if "S" in action:
                    stack.append(int(action[1:]))
                    pointer += 1
                    print(f"{stack_content:<20} {remaining_input:<20} {'Shift':<20} {goto_state:<20} {'-'}")
                
                elif "R" in action:
                    rule_num = int(action[1:])
                    lhs, rhs = self.reductions[rule_num]

                    for _ in range(len(rhs)):
                        stack.pop()

                    new_state = self.goto_table[stack[-1]].get(lhs, None)
                    if new_state is not None:
                        stack.append(new_state)
                        goto_state = f"({stack[-2]},{lhs})={new_state}"

                    print(f"{stack_content:<20} {remaining_input:<20} {'Reduce':<20} {goto_state:<20} {lhs} → {' '.join(rhs)}")
                
                elif action == "ACC":
                    print(f"{stack_content:<20} {remaining_input:<20} {'ACCEPTED':<20} {'-':<20} {'-'}")
                    return True

            else:
                print(f"{stack_content:<20} {input_string[pointer:]:<20} {'ERROR!':<20} {'-':<20} {'-'}")
                return False
            
            step += 1

# Run the parser
parser = SLRParser()
parser.input_grammar()
parser.generate_lr0_items()
parser.print_parsing_table()
parser.parse_input()