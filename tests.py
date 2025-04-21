import pytest
from isreachable import parse_grammar, find_reachable_nonterminals, filter_reachable_grammar
from print_words import derivation_to_nonterminal

grammar1 = [
    "S->AB|b",
    "A->a",
    "B->C",
    "C->c",
    "D->d"
]
expected1_reachable = {"S", "A", "B", "C"}

grammar2 = [
    "S->Aa|b",
    "A->Sb|c",
    "E->f"
]
expected2_reachable = {"S", "A"}

grammar3 = [
    "S->XY",
    "X->xX|Z",
    "Y->y",
    "Z->z",
    "U->V",
    "V->U"
]
expected3_reachable = {"S", "X", "Y", "Z"}


@pytest.mark.parametrize("grammar, start, expected", [
    (grammar1, "S", expected1_reachable),
    (grammar2, "S", expected2_reachable),
    (grammar3, "S", expected3_reachable),
])
def test_find_reachable_and_filter(grammar, start, expected):
    prod = parse_grammar(grammar)
    reachable = find_reachable_nonterminals(prod, start)
    assert reachable == expected

    filtered = filter_reachable_grammar(prod, reachable)
    assert set(filtered.keys()) == expected


@pytest.mark.parametrize("grammar, start, reachable", [
    (grammar1, "S", expected1_reachable),
    (grammar2, "S", expected2_reachable),
    (grammar3, "S", expected3_reachable),
])
def test_derivation_exists_for_reachable(grammar, start, reachable):
    prod = parse_grammar(grammar)
    for nt in reachable:
        deriv = derivation_to_nonterminal(prod, start, nt, max_steps=20)
        assert deriv is not None, f"Нет вывода для {nt}"
        assert nt in deriv.replace(" -> ", ""), f"{nt} не найден в цепочке {deriv}"

    unreachable = set(prod.keys()) - reachable
    for nt in unreachable:
        assert derivation_to_nonterminal(prod, start, nt) is None



