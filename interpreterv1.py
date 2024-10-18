from intbase import *
from element import *
from brewparse import *

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase's constructor
        # Initialize needed variable
        self.trace_output = trace_output
        self.vars = {}
        if self.trace_output:
            print("Interpreter initialized.")
