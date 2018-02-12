
"""
    This DFA recognize w over ∑ s.t. it ends in a 1.
"""
DFA1 = {
    "∑" : [0, 1],
    "q": "q0",
    "F": ["q0"],
    "∂" : {
        "q0": [(0, "q1"), (1, "q0")],
        "q1": [(0, "q1"), (1, "q0")],
    }
}
