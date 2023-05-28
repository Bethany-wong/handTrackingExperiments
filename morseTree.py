morse_tree = {
    'value': '',
    '.': {
        'value': 'E',
        '.': {
            'value': 'I',
            '.': {
                'value': 'S',
                '.': {'value': 'H'},
                '-': {'value': 'V'},
            },
            '-': {
                'value': 'U',
                '.': {'value': 'F'}
            },
        },
        '-': {
            'value': 'A',
            '.': {
                'value': 'R',
                '.': {'value': 'L'},
            },
            '-': {
                'value': 'W',
                '.': {'value': 'P'},
                '-': {'value': 'J'},
            },
        },
    },
    '-': {
        'value': 'T',
        '.': {
            'value': 'N',
            '.': {
                'value': 'D',
                '.': {'value': 'B'},
                '-': {'value': 'X'},
            },
            '-': {
                'value': 'K',
                '.': {'value': 'C'},
                '-': {'value': 'Y'},
            },
        },
        '-': {
            'value': 'M',
            '.': {
                'value': 'G',
                '.': {'value': 'Z'},
                '-': {'value': 'Q'},
            },
            '-': {
                'value': 'O',
            },
        },
    },
}

def traverse_morse_tree(code):
    node = morse_tree
    for char in code:
        if char in node:
            node = node[char]
        else:
            return None
    return node['value']

'''
# Test: alphabets and gibberish
print(traverse_morse_tree('.-'))
print(traverse_morse_tree('-...'))
print(traverse_morse_tree('-.-.'))
print(traverse_morse_tree('-..'))
print(traverse_morse_tree('.'))
print(traverse_morse_tree('..-.'))
print(traverse_morse_tree('--.'))
print(traverse_morse_tree('....'))
print(traverse_morse_tree('..'))
print(traverse_morse_tree('.---'))
print(traverse_morse_tree('-.-'))
print(traverse_morse_tree('.-..'))
print(traverse_morse_tree('--'))
print(traverse_morse_tree('-.'))
print(traverse_morse_tree('---'))
print(traverse_morse_tree('.--.'))
print(traverse_morse_tree('--.-'))
print(traverse_morse_tree('.-.'))
print(traverse_morse_tree('...'))
print(traverse_morse_tree('-'))
print(traverse_morse_tree('..-'))
print(traverse_morse_tree('...-'))
print(traverse_morse_tree('.--'))
print(traverse_morse_tree('-..-'))
print(traverse_morse_tree('-.--'))
print(traverse_morse_tree('--..'))

print(traverse_morse_tree('--...'))
print(traverse_morse_tree('.-s.-'))
print(traverse_morse_tree('..--'))
print(traverse_morse_tree('--d-.'))
print(traverse_morse_tree('----a'))
'''