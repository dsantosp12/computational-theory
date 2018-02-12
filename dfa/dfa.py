"""
    dfa.dfa
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from machines import *


class DFAInterp:
    def __init__(self, m: dict):
        self._alphabet = m["∑"]
        self._start = m["q"]
        self._current = self._start
        self._accept_states = m["F"]
        self._delta_table = m["∂"]
        self.counter = 0
        self._buffer = None
        self.accept_status = False

    def __call__(self, w, report=True):
        self.run(w, report)

    def delta(self, r):
        """
        :param r: input
        :return: str -> state
        """
        if r not in self._alphabet:
            raise RuntimeError("Input: {} not in alphabet".format(r))

        curr_trans = self._delta_table.get(self._current)

        if curr_trans:
            self._current = next(filter(lambda t: t[0] == r, curr_trans))[1]
            self.counter += 1

    def run(self, w, report=True):
        self._buffer = w

        for w_p in self._buffer:
            self.delta(int(w_p))

        self.accept_status = self.is_in_accept_state()

        if report:
            self.report()

    def is_in_accept_state(self):
        return self._current in self._accept_states

    def report(self):
        print("------ Machine Summary ------")
        msg = "After {} transitions, the machine {} the input:\n{}"

        if self.is_in_accept_state():
            print(msg.format(self.counter, "accepts", self._buffer))
        else:
            print(msg.format(self.counter, "rejects", self._buffer))


if __name__ == '__main__':
    interp = DFAInterp(DFA1)

    interp("001101")
