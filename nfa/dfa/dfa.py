"""
    dfa.dfa
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from dfa.machines import *


class DFAInterp:
    def __init__(self, dfa: dict):
        self._alphabet = dfa["∑"]
        self._start = dfa["q"]
        self._current = self._start
        self._accept_states = dfa["F"]
        self._delta_table = dfa["∂"]
        self.counter = 0
        self._buffer = None
        self.accept_status = False

    def __call__(self, w, report=True):
        self.run(w, report)

    def delta(self, r):
        """
            Performs a transition for a given input r.
        """

        # Throws if r is not in alphabet
        self._is_in_alphabet(r)

        # Gets the transitions of the current state
        curr_trans = self._delta_table.get(self._current)

        if curr_trans:
            self._current = next(filter(lambda t: t[0] == r, curr_trans))[1]
            self.counter += 1

    def _is_in_alphabet(self, r):
        """
            Checks if the given input is in the alphabet
        """
        if r not in self._alphabet:
            raise RuntimeError("Input: {} not in alphabet".format(r))

    def run(self, w, report=True):
        """
            Calls the transition function for each char of the input w and
            report the state of the machine by default.
        """
        self._buffer = w

        for w_p in self._buffer:
            self.delta(int(w_p))

        self.accept_status = self.is_in_accept_state()

        if report:
            self.report()

    def is_in_accept_state(self):
        """
            Check if the current state is one of the acceptance state.
        """
        return self._current in self._accept_states

    def report(self):
        """
            Prints the current status of the machine.
        """
        print("------ DFA Machine Summary ------")
        msg = "After {} transitions, the machine {} the input:\n{}"

        if self.is_in_accept_state():
            print(msg.format(self.counter, "accepts", self._buffer))
        else:
            print(msg.format(self.counter, "rejects", self._buffer))


if __name__ == '__main__':
    interp = DFAInterp(DFA1)

    interp("001101")
