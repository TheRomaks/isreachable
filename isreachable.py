
def parse_grammar(grammar_lines):
    productions = {}
    for line in grammar_lines:
        left, right = line.split('->')
        right_parts = right.replace(' ', '').split('|')
        productions[left.strip()] = right_parts
    return productions

def find_reachable_nonterminals(productions, start_symbol):
    reachable = set()
    stack = [start_symbol]

    while stack:
        current = stack.pop()
        if current in reachable:
            continue
        reachable.add(current)
        if current not in productions:
            continue
        for production in productions[current]:
            for symbol in production:
                if symbol.isupper() and symbol not in reachable:
                    stack.append(symbol)
    return reachable

def filter_reachable_grammar(productions, reachable):
    return {nt: prods for nt, prods in productions.items() if nt in reachable}


