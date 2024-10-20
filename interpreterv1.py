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
        num = len(ast.get("functions"))

        if ast.elem_type == 'program':
            for i in range(num):
                if ast.get("functions")[i].get("name") == "main":
                    main_found = True
                    break
            if not main_found:
                super().error(ErrorType.NAME_ERROR,
                          "No main() function was found",
                )
            for i in range(num):
                if ast.get("functions")[i].get("name") == "main":
                    self.run_function(ast.get("functions")[i])

    def run_function(self, func_element):
        if func_element.elem_type != "func" or "name" not in func_element.dict or  "statements" not in func_element.dict:
            super().error(ErrorType.NAME_ERROR,"ERROR: Running run_function_ on invalid function element.")

        if self.trace_output:
            print(f'Running function: {func_element.dict["name"]}.')
        for statement in func_element.dict["statements"]:
            self.run_statement(statement)
    
    def run_statement(self, statement_elem):
        if statement_elem.elem_type not in ["vardef","=", "fcall"] or "name" not in statement_elem.dict:
            super().error(ErrorType.NAME_ERROR,"ERROR: Running run_statement on invalid statement element.")

        if self.trace_output:
            print(f'Running statement {statement_elem.elem_type} {statement_elem.dict["name"]}.')
        if statement_elem.elem_type == "vardef":
            if statement_elem.get("name") in self.vars_to_vals:
                super().error(ErrorType.NAME_ERROR, f"Variable {statement_elem.get('name')} defined more than once",)
            self.vars_to_vals[statement_elem.dict["name"]] = None

        # Statement logic (assignment)
        if statement_elem.elem_type == "=":
            if "expression" not in statement_elem.dict:
                super().error(ErrorType.NAME_ERROR,"ERROR: Statement element has no expression.")
                exit()
            if self.trace_output:
                print("Statement is assignment.")
            value = self.get_expr(statement_elem.get("expression"))
            self.vars_to_vals[statement_elem.get("name")] = value

        # Statment logic (fcall)
        if statement_elem.elem_type == "fcall":
            # Verify fcall structure
            if "args" not in statement_elem.dict:
                super().error(ErrorType.NAME_ERROR,"ERROR: Statement element has no args.")
                exit()
            # Trace output
            if self.trace_output:
                print("Statement is fcall.")
            # Fcall logic
            self.run_fcall(statement_elem)


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

    new_interpreter = Interpreter(console_output = True, inp = None, trace_output = False)
    new_interpreter.run(test_program)

if __name__ == "__main__":
   main()