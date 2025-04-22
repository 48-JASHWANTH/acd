def add_state(result, state):
    """Add a state to the result list if not already added"""
    if state not in result:
        result.append(state)

def display(result, state_name):
    """Display the epsilon closure"""
    print(f"Epsilon closure of {state_name} = {{", end=" ")
    print(", ".join(result), end=" }\n")

def epsilon_closure(transition_table, start_state):
    """Compute epsilon closure of a given state"""
    epsilon_closure_set = []  # Store the epsilon closure set

    # Add the start state to the closure
    add_state(epsilon_closure_set, start_state)
    
    # Process epsilon transitions iteratively
    added = True
    while added:
        added = False
        for state1, input_symbol, state2 in transition_table:
            if (
                state1 in epsilon_closure_set and 
                input_symbol == 'None' and 
                state2 not in epsilon_closure_set
            ):
                add_state(epsilon_closure_set, state2)
                added = True

    return epsilon_closure_set  # Return the closure

def main():
    # Read the number of states
    n = int(input("Enter the number of states: "))
    
    # Auto-generate state names as q0 to q(n-1)
    states = [f"q{i}" for i in range(n)]
    
    # Read the transitions
    transition_table = []
    print("Enter the transition table:")
    
    for state in states:
        transitions = input(
            f"Enter transitions from state {state} "
            "(comma-separated, use 'None' for epsilon): "
        ).split(',')

        for transition in transitions:
            parts = transition.strip().split()
            if len(parts) == 2:
                state1, input_symbol, state2 = state, parts[0], parts[1]
            elif len(parts) == 1:
                state1, input_symbol, state2 = state, 'None', parts[0]

            transition_table.append((state1, input_symbol, state2))
    
    # Compute epsilon closure for each state
    for state in states:
        closure = epsilon_closure(transition_table, state)
        display(closure, state)

if __name__ == "__main__":
    main()
