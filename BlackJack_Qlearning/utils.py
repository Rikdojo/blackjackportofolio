import numpy as np

def argmax(Q, s):
    actions = [a for (state, a) in Q if state == s]
    if not actions:
        return None
    values = [Q[(s, a)] for a in actions]
    max_index = np.argmax(values)
    return actions[max_index]