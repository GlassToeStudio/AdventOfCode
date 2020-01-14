from .instruction import Instruction


class Int_Computer:

    def __init__(self, intcode, input_from_queue=False, output_to_queue=False):
        self.IO_queue = []
        self.__relative_base__ = [0]
        self.__instruction_pointer__ = 0
        self.__instructions__ = {}
        self.__intcode__ = self.__load_program__(intcode)

        add_instruction = Instruction(self.__add_operation__, 3)
        mult_instruction = Instruction(self.__mul_operation__, 3)
        if input_from_queue:
            input_instruction = Instruction(self.__automated_input_operation__, 1)
        else:
            input_instruction = Instruction(self.__input_operation__, 1)
        if output_to_queue:
            output_instruction = Instruction(self.__automated_output_operation__, 1)
        else:
            output_instruction = Instruction(self.__output_operation__, 1)
        jump_if_true_instruction = Instruction(self.__jump_if_true_operation__, 2)
        jump_if_false_instruction = Instruction(self.__jump_if_false_operation__, 2)
        less_than_instruction = Instruction(self.__less_than_operation__, 3)
        equals_instruction = Instruction(self.__equals_operation__, 3)
        adjust_base_instruction = Instruction(self.__adjust_relative_base__, 1)
        halt_instruction = Instruction(self.__halt_operation__, 0)

        self.__instructions__ = {
            1: add_instruction,
            2: mult_instruction,
            3: input_instruction,
            4: output_instruction,
            5: jump_if_true_instruction,
            6: jump_if_false_instruction,
            7: less_than_instruction,
            8: equals_instruction,
            9: adjust_base_instruction,
            99: halt_instruction
        }


    # intcode program helper methods
    def __format_opcode__(self, opcode):
        ''' Return a string value of the opcode with parameter modes added.

        Notes:
            Opcodes are 5 digits, 2 for the opcode, and 3 for the parameter
            modes. Leading zeros are omitted since these are integers.

            For example, opcode 3 would be 00003
            For example, opcode 103 would be 00103

            ABCDE
            1002

            DE - two-digit opcode,      02 == opcode 2
            C - mode of 1st parameter,  0 == position mode
            B - mode of 2nd parameter,  1 == immediate mode
            A - mode of 3rd parameter,  0 == default

        Args:
            opcode (int): The two digit opcode

        Returns:
            string: Value of the opcode with parameter modes added
        '''

        sopcode = str(opcode)
        length = len(sopcode)
        for _ in range(length, 5):
            sopcode = f"{0}{sopcode}"
        return sopcode


    def __read_full_opcode__(self, opcode):
        ''' Return an integer value of the opcode:

        Notes:
            Opcodes are 5 digits, 2 for the opcode, and 3 for the parameter
            modes. Leading zeros are omitted since these are integers.

            For example, opcode 3 would be 00003
            For example, opcode 103 would be 00103

            ABCDE
            1002

            DE - two-digit opcode,      02 == opcode 2
            C - mode of 1st parameter,  0 == position mode
            B - mode of 2nd parameter,  1 == immediate mode
            A - mode of 3rd parameter,  0 == default

        Args:
            opcode (int): The string version of the opcode with parameter modes

        Returns:
            int: opcode
        '''

        opcode = int(opcode[-2:])
        return opcode


    def __get_modes__(self, opcode):
        ''' Return an string value of the parameter modes:

        Notes:
            Opcodes are 5 digits, 2 for the opcode, and 3 for the parameter
            modes. Leading zeros are omitted since these are integers.

            For example, opcode 3 would be 00003
            For example, opcode 103 would be 00103

            ABCDE
            1002

            DE - two-digit opcode,      02 == opcode 2
            C - mode of 1st parameter,  0 == position mode
            B - mode of 2nd parameter,  1 == immediate mode
            A - mode of 3rd parameter,  0 == default

        Args:
            opcode (int): The string version of the opcode with parameter modes

        Returns:
            string: parameter modes
        '''

        return opcode[0:3]


    def __get_read_param_by_mode__(self, mode, param, codes):
        ''' Return the values of the given parameters based on their position mode.

        Notes:
            0, position mode, which causes the parameter to be interpreted as a
            position - if the parameter is 50, its value is the value stored
            at address 50 in memory.

            1, immediate mode. In immediate mode, a parameter is interpreted
            as a value - if the parameter is 50, its value is simply 50.

            Parameters that an instruction writes to will never be in immediate
            mode.

        Args:
            mode (int): The parameter mode for the instruction
            param (int): The parameter for the instruction.
            codes (int): The intcode program

        Returns:
            int: paramter based on parameter mode
        '''

        # Position mode: codes[param]
        if mode == '0':
            self.__check_valid_location__(codes, param)
            p = codes[param]
        # immediate_mode: param
        elif mode == '1':
            p = param
        # Relative position mode;
        else:
            self.__check_valid_location__(codes, self.__relative_base__[0] + param)
            p = codes[self.__relative_base__[0] + param]
        return p


    def __get_write_param_by_mode__(self, mode, param, codes):
        ''' Return the values of the given parameters based on their position mode.

        Notes:
            0, position mode, which causes the parameter to be interpreted as a
            position - if the parameter is 50, its value is the value stored
            at address 50 in memory.

            1, immediate mode. In immediate mode, a parameter is interpreted
            as a value - if the parameter is 50, its value is simply 50.

            Parameters that an instruction writes to will never be in immediate
            mode.

        Args:
            mode (int): The parameter mode for the instruction
            param (int): The parameter for the instruction.
            codes (int): The intcode program

        Returns:
            int: paramter based on parameter mode
        '''

        # Position mode: codes[param]
        if mode == '0':
            self.__check_valid_location__(codes, param)
            p = param
        # Relative position mode;
        else:
            self.__check_valid_location__(codes, self.__relative_base__[0] + param)
            p = self.__relative_base__[0] + param
        return p


    def __check_valid_location__(self, codes, param):
        if param >= 0 and codes.get(param, 0) == 0:
            codes[param] = 0


    def __load_program__(self, intcode):
        program = {}
        for i in range(len(intcode)):
            program[i] = intcode[i]
        return program


    # Operations:
    def __add_operation__(self, codes, params, modes, **kwargs):
        ''' Adds together numbers read from two positions, params[0] and params[1]
            and stores the result in a third position, params[2].

        Args:
            codes (int[]): The intcode program
            params (int[]): The parameters for the instruction.
            modes (int[]): The parameter modes for the instruction.

        Returns:
            int: opcode instruction 1
        '''

        param_1 = self.__get_read_param_by_mode__(modes[2], params[0], codes)
        param_2 = self.__get_read_param_by_mode__(modes[1], params[1], codes)
        param_3 = self.__get_write_param_by_mode__(modes[0], params[2], codes)
        codes[param_3] = param_1 + param_2
        return 1


    def __mul_operation__(self, codes, params, modes, **kwargs):
        ''' Multiplies together numbers read from two positions, params[0] and
        params[1] and stores the result in a third position, params[2].

        Args:
            codes (int[]): The intcode program
            params (int[]): The parameters for the instruction.
            modes (int[]): The parameter modes for the instruction.

        Returns:
            int: opcode instruction 2
        '''

        param_1 = self.__get_read_param_by_mode__(modes[2], params[0], codes)
        param_2 = self.__get_read_param_by_mode__(modes[1], params[1], codes)
        param_3 = self.__get_write_param_by_mode__(modes[0], params[2], codes)
        codes[param_3] = param_1 * param_2
        return 2


    def __input_operation__(self, codes, params, modes, **kwargs):
        ''' Prompt the user for input and store the value at the given location.

        Notes:
            Takes a single integer as input (from the console) and saves
            it to the position given by its only parameter.
            For example, the instruction 3,50
            would take an input value and store it at address 50.

        Args:
            codes (int[]): The intcode program
            params (int[]): The parameters for the instruction.

        Returns:
            int: opcode instruction 3
        '''

        user_input = int(input("\t -- Please input a variable: "))
        param_1 = self.__get_write_param_by_mode__(modes[2], params[0], codes)
        codes[param_1] = user_input
        return 3


    def __automated_input_operation__(self, codes, params, modes, **kwargs):
        ''' Modify a value at location in the intcode program with the next
        available value in the input queue.

        Notes:
            Takes a single integer as input (from the input queue) and saves
            it to the position given by its only parameter.
            For example, the instruction 3,50
            would take an input value and store it at address 50.

        Args:
            codes (int[]): The intcode program
            params (int[]): The parameters for the instruction.

        Returns:
            int: opcode instruction 3
        '''

        param_1 = self.__get_write_param_by_mode__(modes[2], params[0], codes)
        codes[param_1] = self.IO_queue.pop()
        return 3


    def __output_operation__(self, codes, params, modes, **kwargs):
        ''' Print to the console, the output of the given instruction.

        Notes:
            Outputs the value of its only parameter. (to the console)
            For example, the instruction 4,50 would output the value at
            address 50.

        Args:
            codes (int[]): The intcode program
            params (int[]): The parameters for the instruction.

        Prints to console:
            the value at the given location

        Returns:
            int: opcode instruction 4
        '''

        param_1 = self.__get_read_param_by_mode__(modes[2], params[0], codes)
        print(f"\t -- The value is {param_1}")
        return 4


    def __automated_output_operation__(self, codes, params, modes, **kwargs):
        ''' Add the value from the intcode program at location params[0] to the
        input_queue

        Notes:
            Outputs the value of its only parameter. (to the input queue)
            For example, the instruction 4,50 would output the value at
            address 50.

        Args:
            codes (int[]): The intcode program
            params (int[]): The parameters for the instruction.

        Returns:
            int: opcode instruction 4
        '''

        param_1 = self.__get_read_param_by_mode__(modes[2], params[0], codes)
        self.IO_queue.append(param_1)
        return 4


    def __jump_if_true_operation__(self, codes, params, modes, address):
        ''' If the first parameter params[0] is non-zero, it sets the instruction
        pointer to the value from the second parameter params[1]. Otherwise,
        it does nothing.

        Args:
            codes (int[]): The intcode program
            params (int[]): The parameters for the instruction.
            modes (int[]): The parameter modes for the instruction.

        Returns:
            int: opcode instruction 5
        '''

        param_1 = self.__get_read_param_by_mode__(modes[2], params[0], codes)
        param_2 = self.__get_read_param_by_mode__(modes[1], params[1], codes)

        if param_1 != 0:
            self.__instructions__[5].update_steps(param_2 - address)
        else:
            self.__instructions__[5].update_steps(len(params) + 1)
        return 5


    def __jump_if_false_operation__(self, codes, params, modes, address):
        ''' If the first parameter param[0] is zero, it sets the instruction
        pointer to the value from the second parameter params[1].
        Otherwise, it does nothing.

        Args:
            codes (int[]): The intcode program
            params (int[]): The parameters for the instruction.
            modes (int[]): The parameter modes for the instruction.

        Returns:
            int: opcode instruction 6
        '''

        param_1 = self.__get_read_param_by_mode__(modes[2], params[0], codes)
        param_2 = self.__get_read_param_by_mode__(modes[1], params[1], codes)

        if param_1 == 0:
            self.__instructions__[6].update_steps(param_2 - address)
        else:
            self.__instructions__[6].update_steps(len(params) + 1)

        return 6


    def __less_than_operation__(self, codes, params, modes, **kwargs):
        ''' If the first parameter params[0] is less than the second
        parameter params[1], it stores 1 in the position given by the third
        parameter params[2]. Otherwise, it stores 0.

        Args:
            codes (int[]): The intcode program
            params (int[]): The parameters for the instruction.
            modes (int[]): The parameter modes for the instruction.

        Returns:
            int: opcode instruction 7
        '''

        param_1 = self.__get_read_param_by_mode__(modes[2], params[0], codes)
        param_2 = self.__get_read_param_by_mode__(modes[1], params[1], codes)
        param_3 = self.__get_write_param_by_mode__(modes[0], params[2], codes)
        if param_1 < param_2:
            codes[param_3] = 1
        else:
            codes[param_3] = 0
        return 7


    def __equals_operation__(self, codes, params, modes, **kwargs):
        ''' If the first parameter params[0] is equal to the second
        parameter params[1], it stores 1 in the position given by the third
        parameter params[2]. Otherwise, it stores 0. 0.

        Args:
            codes (int[]): The intcode program
            params (int[]): The parameters for the instruction.
            modes (int[]): The parameter modes for the instruction.

        Returns:
            int: opcode instruction 8
        '''

        param_1 = self.__get_read_param_by_mode__(modes[2], params[0], codes)
        param_2 = self.__get_read_param_by_mode__(modes[1], params[1], codes)
        if param_1 == param_2:
            if modes[0] == '0':
                codes[params[2]] = 1
            else:
                codes[self.__relative_base__[0] + params[2]] = 1
        else:
            if modes[0] == '0':
                codes[params[2]] = 0
            else:
                codes[self.__relative_base__[0] + params[2]] = 0
        return 8


    def __adjust_relative_base__(self, codes, params, modes, **kwargs):
        param_1 = self.__get_read_param_by_mode__(modes[2], params[0], codes)
        self.__relative_base__[0] = self.__relative_base__[0] + param_1
        return


    def __halt_operation__(self, **kwargs):
        ''' Halts the program.

        Returns:
            int: opcode instruction 99
        '''

        return 99


    # Main
    def run(self):
        ''' Run the intcode program ;)

        Yeilds:
            opcode instruction

        '''

        while (self.__instruction_pointer__ < len(self.__intcode__)):
            full_opcode = self.__format_opcode__(self.__intcode__[self.__instruction_pointer__])
            opcode = self.__read_full_opcode__(full_opcode)
            modes = self.__get_modes__(full_opcode)
            params = self.__instructions__[opcode].get_params(self.__intcode__, self.__instruction_pointer__)
            r = self.__instructions__[opcode].execute(
                self.__intcode__,
                params,
                modes,
                self.__instruction_pointer__
                )
            self.__instruction_pointer__ += self.__instructions__[opcode].steps
            yield r
