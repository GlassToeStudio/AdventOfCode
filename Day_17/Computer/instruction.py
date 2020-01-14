import math


class Instruction:

    def __init__(self, operation_fn, num_params):
        self.__num_parameters__ = num_params
        self.__operation_fn__ = operation_fn
        self.steps = 0
        self.update_steps(num_params + 1 if num_params > 0 else math.inf)

    def get_params(self, intcodes, address):
        p = []
        start = address + 1
        end = start + self.__num_parameters__
        for i in range(start, end):
            p.append(intcodes[i])
        return p

    def update_steps(self, steps):
        self.steps = steps

    def execute(self, intcodes=[],  params=[], modes=[],  address=0):
        r = self.__operation_fn__(
            codes=intcodes, params=params, modes=modes, address=address)
        return r
