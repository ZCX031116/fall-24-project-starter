from intbase import *
from element import *
from brewparse import *

class Interpreter(InterpreterBase):
    '''
    Constructor built using InterpreterBase as inherited from intbase

    Args:
    console_output: where output of an interpreted program should be directed to
    inp: parameter is used for testing scripts.
    trace_output: help in debugging. Set to true if you want to be able to use python print
    '''
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp) 
        self.trace_output = trace_output
        self.vars_to_vals = {} # map for holding all variables | key: variable name; val: value
        if self.trace_output:
            print("Interpreter initialized.")

    def run(self, program):
        ast = parse_program(program)
        if self.trace_output:
            print("Received AST from parser.")
        self.vars_to_vals = {}
        main_found = False
        if ast.elem_type == "program":
            # Find finctions
            if "functions" in ast.dict:
                for func_elem in ast.dict["functions"]:
                    # Get main function
                    if func_elem.dict.get("name", None) == "main":
                        self.do_function(func_elem)
                        main_found = True
                        break
            if not main_found:
                super().error(ErrorType.NAME_ERROR,
                          "No main() function was found",
                )


def main():
    test_program = """func main() {
        var x;
        var y;
        var z;
        var a;
        var b;
        var a_str;
        var magic_num;
        var magic_num_no_prompt;

        x = 5 + 6;
        y = 10;
        z = (x + (1 - 3)) - y;
        a_str = "this is a string";

        print(10);
        print("hello world!");
        print("The sum is: ", x);
        print("the answer is: ", x + (y - 5), "!");
        print("hi", inputi("enter your number: "), "there");

        magic_num = inputi("enter a magic number: "); 
        print("magic_num: ", magic_num);
        magic_num_no_prompt = inputi();
        print("magic_num_no_prompt + 19: ", magic_num_no_prompt + 19);

        a = 4 + inputi("enter a number: ");
        b = 3 - (3 + (2 + inputi()));    
        print(a + b);
    }"""

    new_interpreter = Interpreter(console_output = True, inp = None, trace_output = True)
    new_interpreter.run(test_program)

# if __name__ == "__main__":
#    main()