from collections import defaultdict

def compute_first(grammar, symbol, first):
    if symbol in first:
        return first[symbol]
    first[symbol] = set()
   
    if not symbol.isupper():  
        first[symbol].add(symbol)
        return first[symbol]
   
    for production in grammar[symbol]:
        for char in production:
            char_first = compute_first(grammar, char, first)
            first[symbol] |= (char_first - {'ε'})
            if 'ε' not in char_first:
                break
        else:
            first[symbol].add('ε')
   
    return first[symbol]

def compute_follow(grammar, start_symbol, first, follow):
    follow[start_symbol].add('$')  
   
    while True:
        updated = False
       
        for non_terminal, productions in grammar.items():
            for production in productions:
                trailer = follow[non_terminal].copy()
               
                for symbol in reversed(production):
                    if symbol.isupper():
                        if not (follow[symbol] >= trailer):
                            follow[symbol] |= trailer
                            updated = True
                       
                        if 'ε' in first[symbol]:
                            trailer |= (first[symbol] - {'ε'})
                        else:
                            trailer = first[symbol]
                    else:
                        trailer = {symbol}
       
        if not updated:
            break

def main():
    grammar = defaultdict(list)
    num_rules = int(input("Enter the number of grammar rules: "))
    for _ in range(num_rules):
        rule = input("Enter production (e.g., A->BC|a): ").replace(" ", "")
        lhs, rhs = rule.split("->")
        rhs_productions = rhs.split("|")
        grammar[lhs].extend(rhs_productions)
   
    first = {}
    follow = defaultdict(set)
   
    for non_terminal in grammar:
        compute_first(grammar, non_terminal, first)
   
    start_symbol = next(iter(grammar))
    compute_follow(grammar, start_symbol, first, follow)
   
    print("\nFirst Sets:")
    for non_terminal, values in first.items():
        if non_terminal.isupper():
            print(f"First({non_terminal}) = {values}")
   
    print("\nFollow Sets:")
    for non_terminal, values in follow.items():
        print(f"Follow({non_terminal}) = {values}")

if __name__ == "__main__":
    main() 