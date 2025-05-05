def epsilon_closure(state, nfa):
    closure, stack = set(), [state]
    while stack:
        s = stack.pop()
        if s not in closure:
            closure.add(s)
            stack.extend(nfa.get(s, {}).get('ε', []))
    return closure


n = int(input("No. of states: "))
nfa = {}
for _ in range(n):
    state = input("State: ")
    eps = input(f"ε-transitions from {state} (comma-separated or blank): ").split(',')
    nfa[state] = {'ε': [s.strip() for s in eps if s.strip()]}

start = input("Compute ε-closure of: ")
if start in nfa:
    result = epsilon_closure(start, nfa)
    print(f"ε-closure({start}) = {{ {', '.join(sorted(result))} }}")
else:
    print("State not in NFA.")
