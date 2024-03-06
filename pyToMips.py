import os
from CharIndex import CharIndex

inter_buffer = ''

with open('./input.py', 'r') as input_file:
    inter_buffer = input_file.readlines()

strings = {
    'new_line': "\\n"
}

char_index = CharIndex(2)

for line_i, line in enumerate(inter_buffer):
    start_index = -1
    end_index = -1

    string = ''
    for char_i, char in enumerate(line):
        if char == '"':
            if start_index == -1:
                start_index = char_i
            else:
                end_index = char_i
                inverted = {strings[v]: v for v in strings}
                if string in inverted:
                    inter_buffer[line_i] = line[:start_index] + f'${inverted[string]}' + line[end_index + 1:]
                    continue
                print(string)
                strings[char_index.get()] = string
                inter_buffer[line_i] = line[:start_index] + f'${char_index.get()}' + line[end_index + 1:]
                char_index.increment()

            continue
        if start_index != -1:
            string += char

def make_text(strs: dict[str, str]):
    print(strs)
    return '\n'.join([
        f'\t{string}: .asciiz "{strs[string]}"' for string in strs
    ])

def make_print(string_character: str):
    return f'''\
\tla $a0, {string_character} # ({string_character} = "{strings[string_character]}")
\tli $v0, 4
\tsyscall

'''

def make_newline():
        return f'''\
\tla $a0, new_line
\tli $v0, 4
\tsyscall

'''

def make_quit(exit_code: int = 0):
    return f'''\
\tli $v0, 17
\tli $a0, {exit_code}
\tsyscall
'''    

commands = []

for line in inter_buffer:
    in_function = False
    function_name_buffer = ''
    parameter_buffer = ''
    for char in line:
        if not in_function:
            if char == '(':
                in_function = True
                continue
            function_name_buffer += char

        if char == ')':
            if function_name_buffer == 'print': 
                commands.append(make_print(parameter_buffer[1:]))
                commands.append(make_newline())
            elif function_name_buffer == 'quit':
                commands.append(make_quit())

            function_name_buffer = ''
            parameter_buffer = ''
            in_function = False
            continue

        if in_function:
            parameter_buffer += char

with open('./out.mips', 'w+') as out:
    out.write(f'''
.text
main:
{''.join(commands)}
.data
{make_text(strings)}
''')
    print(commands)

os.system('spim ./out.mips')