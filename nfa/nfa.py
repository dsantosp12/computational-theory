"""
    nfa.nfa
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from functools import reduce
from itertools import combinations

from machines import *
from dfa.dfa import DFAInterp

E = "epsilon"


class NFAInterp:
    def __init__(self, nfa: dict):
        self._nfa = nfa
        self._alphabet = nfa["∑"]
        self._start = nfa["q"]
        self._current = self._start
        self._accept_states = nfa["F"]
        self._delta_table = nfa["∂"]
        self.counter = 0
        self._buffer = None
        self.accept_status = 0

    def __call__(self, w, report=True):
        self.run(w, report)

    def _delta(self, r):
        new_set = set([])

        r = int(r)

        for st in self._current:
            row = self._delta_table[st]

            cells = list(filter(lambda it: it[0] == r or it[0] == E, row))

            counter = 0
            for it in cells:
                if it[0] == E:
                    try:
                        cells[counter][1].remove(st)
                    except KeyError:
                        pass
                    else:
                        break
                counter += 1

            new_set = new_set.union(
                reduce(
                    lambda acc, it: acc.union(it[1]),
                    cells, set([])
                )
            )
        self._current = new_set

    def _is_in_alphabet(self, r):
        pass

    def run(self, w, report):
        self._buffer = w

        for c in w:
            self._delta(c)
            self.counter += 1

        self.accept_status = self.is_in_accept_state()

        if report:
            self.report()

    def is_in_accept_state(self):
        return self._current.intersection(self._accept_states) != set([])

    def report(self):
        print("------ NFA Machine Summary ------")
        msg = ("After %d transitions, the machine {} the input:\n{}" %
               self.counter)

        if self.accept_status:
            print(msg.format("accepts", self._buffer))
            print("The machine current state(s): {}".format(self._current))
        else:
            print(msg.format("rejects", self._buffer))


class NFAtoDFACompiler:
    def __init__(self, nfa):
        self._src = nfa
        self._alphabet = nfa["∑"] + [E]
        self._accept_states = nfa["F"]
        self._start = nfa["q"]

        self._states = self._get_states_from(nfa["∂"])
        self._build_pre_transition_table([n for n in nfa["∂"]])
        self._build_post_transition_table()
        self._update_accept_states()

    @staticmethod
    def _get_states_from(table):
        return list(map(lambda it: set(it),
                        [x for length in range(len(table) + 1)
                         for x in combinations(table, length)]))

    def _build_pre_transition_table(self, states):
        def get_transition(r, w):
            return next(
                map(lambda it: (it[0], it[1] or {"ø"}),
                    filter(lambda it: it[0] == w, self._src["∂"][r])
                    )
            )

        self._transition_pre_table = {}

        # Remove the empty set
        try:
            states.remove(set([]))
        except ValueError:
            pass
        else:
            self._transition_pre_table = {
                "ø": [(w, {"ø"}) for w in self._alphabet]
            }

        for states_set in states:
            for st in states_set:
                self._transition_pre_table[
                    self._set_to_name(states_set)
                ] = reduce(
                    lambda acc, it:
                        acc + [get_transition(st, it)],
                    self._alphabet,
                    []
                )

    def _build_post_transition_table(self):
        def get_epsilon_transition(t, w):
            if w == E:
                return {"ø"}

            state = next(filter(lambda it: it[0] == w, t[1]))[1]

            if state == {"ø"}:
                return state

            return next(filter(lambda it: it[0] == E,
                        self._transition_pre_table[state.pop()]))[1]

        def merge_transitions(trans):
            merged_transitions = []
            for w in self._alphabet[:-1]:
                filtered = list(filter(lambda it: it[0] == w, trans))

                if len(filtered) > 1:
                    count = 0
                    for t in filtered:
                        count += 1
                        if t[1] != "ø":
                            merged_transitions.append(t)
                            break

                        if count > 1:
                            merged_transitions.append(t)
                else:
                    merged_transitions.append(next(filtered))
            return merged_transitions

        self._transition_table = {}
        unique_state = []
        for t_st in self._transition_pre_table.items():
            self._transition_table[t_st[0]] = []
            for w in self._alphabet[:-1]:
                e_t = get_epsilon_transition(t_st, w)

                e_t_name = self._set_to_name(e_t)

                self._transition_table[t_st[0]].append((w, e_t_name))

                if self._transition_table.get(e_t_name) is None \
                        and e_t != {"ø"}:
                    unique_state.append(e_t)

        for states in unique_state:
            state_name = self._set_to_name(states)
            transitions = []
            for state in states:
                for w in self._alphabet[:-1]:
                    t = next(filter(lambda it: it[0] == w,
                                    self._transition_table[state]))
                    transitions.append(t)

            if len(transitions) > len(self._alphabet) - 1:
                self._transition_table[state_name] = merge_transitions(
                    transitions
                )
            else:
                self._transition_table[state_name] = transitions

    @staticmethod
    def _set_to_name(s):
        return reduce(lambda acc, it: acc + "," + it, list(s))

    def __call__(self):
        """
            Returns a DFA
        :param dfa:
        :return:
        """
        return {
            "∑": self._alphabet,
            "q": self._start.pop(),
            "F": list(self._accept_states),
            "∂": self._transition_table
        }

    def _update_accept_states(self):
        ac_st = list(self._accept_states)[0]

        for key in self._transition_table:
            if ac_st in key:
                self._accept_states = self._accept_states.union({key})


if __name__ == '__main__':
    w = "10010110"

    # NFAInterp(NFA3)(w)

    dfa = NFAtoDFACompiler(NFA3)()

    DFAInterp(dfa)(w)
