from collections import deque
from isreachable import parse_grammar, find_reachable_nonterminals, filter_reachable_grammar

def derivation_to_nonterminal(productions, start_symbol, target_nonterminal, max_steps=10):
    queue = deque()
    queue.append((start_symbol, [start_symbol]))

    visited = set()

    while queue:
        current, path = queue.popleft()
        if (current, len(path)) in visited:
            continue
        visited.add((current, len(path)))
        if target_nonterminal in current:
            return ' -> '.join(path)
        if len(path) > max_steps:
            continue

        for i, symbol in enumerate(current):
            if symbol in productions:
                for prod in productions[symbol]:
                    new_string = current[:i] + prod + current[i + 1:]
                    queue.append((new_string, path + [new_string]))
    return None

#небольшой примерчик
grammar_lines = [
    "S→AB|CD",
    "A→EF",
    "G→AD",
    "C→c"
]
productions = parse_grammar(grammar_lines)
start_symbol = 'S'

reachable = find_reachable_nonterminals(productions, start_symbol)
print("Достижимые нетерминалы:", reachable)

for nt in sorted(reachable):
    derivation = derivation_to_nonterminal(productions, start_symbol, nt)
    print(f"Пример вывода для {nt}: {derivation if derivation else 'Не найдено'}")

filtered = filter_reachable_grammar(productions, reachable)
print("\nГрамматика без недостижимых нетерминалов:")
for nt in filtered:
    prod_str = ' | '.join(filtered[nt])
    print(f"{nt} → {prod_str}")
