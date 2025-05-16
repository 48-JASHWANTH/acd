from collections import defaultdict

class LL1Parser:
    def __init__(self):
        self.grammar = defaultdict(list)
        self.terminals = set()
        self.non_terminals = set()
        self.first_sets = defaultdict(set)
        self.follow_sets = defaultdict(set)
        self.parse_table = defaultdict(dict)
        self.start_symbol = None

    def input_grammar(self):
        n = int(input("Enter number of productions: "))
        print("Enter the productions (use '|' for multiple rules, space-separated, use 'ε' for epsilon):")

        for _ in range(n):
            line = input().strip().split("->")
            lhs = line[0].strip()
            rhs = line[1].strip().split("|")
            self.non_terminals.add(lhs)

            for production in rhs:
                production = production.split()
                self.grammar[lhs].append(production)
                for symbol in production:
                    if not symbol.isupper() and symbol != 'ε':
                        self.terminals.add(symbol)

        self.start_symbol = list(self.grammar.keys())[0]
        self.terminals.add("$")  

    def compute_first(self):
        for terminal in self.terminals:
            self.first_sets[terminal] = {terminal}

        while True:
            changes = False

            for non_terminal in self.non_terminals:
                for production in self.grammar[non_terminal]:
                    before_change = len(self.first_sets[non_terminal])
                    if production[0] == 'ε':
                        self.first_sets[non_terminal].add('ε')
                    else:
                        for symbol in production:
                            self.first_sets[non_terminal].update(self.first_sets[symbol] - {'ε'})
                            if 'ε' not in self.first_sets[symbol]:
                                break
                        else:
                            self.first_sets[non_terminal].add('ε')

                    if len(self.first_sets[non_terminal]) > before_change:
                        changes = True
            if not changes:
                break

    def compute_follow(self):
        self.follow_sets[self.start_symbol].add("$")

        while True:
            changes = False

            for lhs, productions in self.grammar.items():
                for production in productions:
                    follow_temp = self.follow_sets[lhs].copy()

                    for symbol in reversed(production):
                        if symbol in self.non_terminals:
                            before_change = len(self.follow_sets[symbol])
                            self.follow_sets[symbol].update(follow_temp)
                            if 'ε' in self.first_sets[symbol]:
                                follow_temp.update(self.first_sets[symbol] - {'ε'})
                            else:
                                follow_temp = self.first_sets[symbol]

                            if len(self.follow_sets[symbol]) > before_change:
                                changes = True
                        else:
                            follow_temp = self.first_sets[symbol]
            if not changes:
                break

    def construct_parse_table(self):
        for non_terminal, productions in self.grammar.items():
            for production in productions:
                first = self.get_first(production)

                for terminal in first - {'ε'}:
                    self.parse_table[non_terminal][terminal] = production

                if 'ε' in first:
                    for terminal in self.follow_sets[non_terminal]:
                        self.parse_table[non_terminal][terminal] = production

    def get_first(self, production):
        first = set()

        if production[0] == 'ε':
            return {'ε'}

        for symbol in production:
            first.update(self.first_sets[symbol] - {'ε'})
            if 'ε' not in self.first_sets[symbol]:
                break
        else:
            first.add('ε')

        return first

    def parse(self, input_string):
        stack = ['$', self.start_symbol]
        input_tokens = input_string.split() + ['$']
        index = 0

        print("\nTracing of Parsing Process:")
        print(f"{'Stack':<30}{'Input':<30}{'Action'}")
        print("-" * 70)

        while stack:
            top = stack.pop()
            current_input = input_tokens[index]
            stack_content = ' '.join(reversed(stack))
            input_content = ' '.join(input_tokens[index:])
           
            if top == current_input:
                print(f"{stack_content:<30}{input_content:<30}Match '{current_input}'")
                index += 1
            elif top in self.terminals:
                print(f"{stack_content:<30}{input_content:<30}Error: Unexpected '{current_input}'")
                return "Failed"
            elif top in self.non_terminals:
                production = self.parse_table.get(top, {}).get(current_input)
                if production:
                    rule_str = ' '.join(production)
                    print(f"{stack_content:<30}{input_content:<30}Expand: {top} -> {rule_str}")
                    if production != ['ε']:
                        stack.extend(reversed(production))
                else:
                    print(f"{stack_content:<30}{input_content:<30}Error: No rule for '{top}' with '{current_input}'")
                    return "Failed"
            else:
                print(f"{stack_content:<30}{input_content:<30}Error: Invalid symbol '{top}'")
                return "Failed"

        if index == len(input_tokens):
            return "Success"
        else:
            return "Failed"

    def print_parse_table(self):
        print("\nParse Table:")
        headers = sorted(self.terminals)
        print(f"{'Non-Terminal':<15}", end="")
        for header in headers:
            print(f"{header:<15}", end="")
        print()

        for non_terminal in self.non_terminals:
            print(f"{non_terminal:<15}", end="")
            for terminal in headers:
                rule = self.parse_table[non_terminal].get(terminal, "")
                if rule:
                    rule_str = " ".join(rule)
                    print(f"{rule_str:<15}", end="")
                else:
                    print(f"{'':<15}", end="")
            print()

if __name__ == "__main__":
    parser = LL1Parser()
    parser.input_grammar()
    parser.compute_first()
    parser.compute_follow()
    parser.construct_parse_table()
    parser.print_parse_table()

    input_string = input("\nEnter an input string to parse: ")
    result = parser.parse(input_string)
    print(f"\nResult: {result}")
