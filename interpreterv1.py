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
        
        # print(statement_elem)
        # Statement (vardef)
        if statement_elem.elem_type == "vardef":
            if statement_elem.get("name") in self.vars_to_vals:
                super().error(ErrorType.NAME_ERROR, f"Variable {statement_elem.get('name')} defined more than once",)
            self.vars_to_vals[statement_elem.dict["name"]] = None

        # Statement (assignment)
        elif statement_elem.elem_type == "=":
            if "expression" not in statement_elem.dict:
                super().error(ErrorType.NAME_ERROR,"ERROR: Statement element has no expression.")
            if statement_elem.get("name") not in self.vars_to_vals:
                super().error(ErrorType.NAME_ERROR, f"Variable {statement_elem.get('name')} not defined",)

            if self.trace_output:
                print("Statement is assignment.")
            # print(statement_elem.get("expression"))
            value = self.run_expression(statement_elem.get("expression"))
            self.vars_to_vals[statement_elem.get("name")] = value

        # Statment (fcall)
        elif statement_elem.elem_type == "fcall":
            if "args" not in statement_elem.dict:
                super().error(ErrorType.NAME_ERROR,"ERROR: Statement element has no args.")
            if self.trace_output:
                print("Statement is fcall.")
            self.run_fcall(statement_elem)
        
        else:
            super().error(ErrorType.NAME_ERROR, "It's Not a valid statement",)
        # print(self.vars_to_vals)

    def run_expression(self, expr_elem):

        Operators = { "-" : lambda x, y: x - y, "+" : lambda x, y: x + y,}

        VAR = ["var"]
        VALUE = ["string","int"]
        EXPR = ["fcall", "+", "-"]

        result = None
        if expr_elem.elem_type in VAR:
            if "name" not in expr_elem.dict:
                super().error(ErrorType.NAME_ERROR, "Variable expression has no name.")
            if self.trace_output:
                print(f"Evaluating variable with name {expr_elem.get('name')}.")
            var_name = expr_elem.get("name")

            if var_name not in self.vars_to_vals:
                super().error(ErrorType.NAME_ERROR, f"Variable {var_name} has not been defined")
            
            result = self.vars_to_vals[var_name]

        elif expr_elem.elem_type in VALUE:
            if "val" not in expr_elem.dict:
                super().error(ErrorType.NAME_ERROR, "ERROR: Value expression has no val.")
            if self.trace_output:
                print(f'Evaluting value w val {expr_elem.dict["val"]}.')
            result = expr_elem.get("val")  

        elif expr_elem.elem_type in EXPR:
            if expr_elem.elem_type in Operators:
                if "op1" not in expr_elem.dict or "op2" not in expr_elem.dict:
                    super.error(ErrorType.NAME_ERROR,"Expression no valid op1 or op2.")

                op1 = self.run_expression(expr_elem.dict["op1"])
                op2 = self.run_expression(expr_elem.dict["op2"])

                if self.trace_output:
                    print(f"Evaluting operator expression {expr_elem.elem_type} {op1} {op2}.")

                if not isinstance(op1, int) or not isinstance(op2, int):
                    super().error(ErrorType.TYPE_ERROR,"Incompatible types for arithmetic operation",
                    )

                result =  Operators[expr_elem.elem_type](op1, op2)

            elif expr_elem.elem_type == "fcall":
                result = self.run_fcall(expr_elem)

            else:
                super().error(ErrorType.NAME_ERROR,"ERROR: Expression is not operator or fcall.")

        else:
            super().error(ErrorType.NAME_ERROR,"expression type is not the acceptable one.")

        return result

    def run_fcall(self, fcall_elem):
        func_list = ["print", "inputi"]

        if fcall_elem.elem_type != "fcall" or "name" not in fcall_elem.dict or "args" not in fcall_elem.dict:
            super().error(ErrorType.NAME_ERROR, " invalid fcall element.")
        if fcall_elem.get("name") not in func_list:
                super().error(ErrorType.NAME_ERROR, f"Function {fcall_elem.get('name')} not defined",)

        if self.trace_output:
            print(f'Perform function call {fcall_elem.dict["name"]}')

        if fcall_elem.get("name") == "print":
            string_print = ""
            args = fcall_elem.get("args")
            for item in args:
                string_print += str(self.run_expression(item))
            super().output(string_print)

        elif fcall_elem.dict["name"] == "inputi":
            args = fcall_elem.get("args")
            if len(args) > 1:
                super().error(ErrorType.NAME_ERROR,f"inputi() function do not take more than parameter",)
            else:
                if len(args)==1:
                    prompt = str(self.run_expression(args[0]))
                    super().output(prompt)
                input = int(super().get_input())
                return input
        else:
            super().error(ErrorType.NAME_ERROR,f'No matching function.',)

        return None

def main():
    test_program = """func main() {
        var x;
        var y;
        var z;

        x = 5 + 2;
        var word;
        word = "hello";
        print(word);
        
        y = 12;
        z = y - (x + (5 - 2));
    }"""

    new_interpreter = Interpreter(console_output = True, inp = None, trace_output = False)
    new_interpreter.run(test_program)

if __name__ == "__main__":
   main()