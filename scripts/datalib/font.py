import datalib.defs


def register_parser(parent):
    parser = parent.add_parser('font', help='generate the font table')
    parser.set_defaults(command_func=run)


def run(args):
    fonts = generate_font_table()

    print(datalib.defs.json_minidumps(fonts))


###############################################################################


def generate_font_table():
    specials = {
        0: 'Solid Black',
        1: 'Solid Black',
        2: '\u2191',
        3: '\u2193',
        4: 'Solid Black',
        5: '\u2190',
        6: '\u2192',
        7: 'Solid Black',
        8: 'Empty Health Bar, Lower',
        9: 'Empty Health Bar, Upper',
        25: '\u00a3',
        95: 'Filled Health Bar, Upper',
        96: 'Filled Health Bar, Lower',
        97: 'Solid Gray',
        98: 'Solid Gray',
        99: 'Solid Gray'
    }

    table = []

    for i in range(100):
        ascii_code = None

        if i in specials:
            char = specials[i]
        elif 10 <= i < 69:
            ascii_code = i + 22
            char = chr(ascii_code)
        elif 69 <= i < 95:
            ascii_code = i + 28
            char = chr(ascii_code)
        else:
            raise RuntimeError('huh?')

        if i == 2:
            ascii_code = 24  # CP437 up arrow
        elif i == 3:
            ascii_code = 25  # CP437 down arrow
        elif i == 5:
            ascii_code = 27  # CP437 left arrow
        elif i == 6:
            ascii_code = 26  # CP437 right arrow
        elif i == 25:
            ascii_code = 156  # CP437 pound sterling

        table.append({
            'index': i,
            'offset_bytes': i * 40,
            'ascii_code': ascii_code,
            'character': char,
            'c_character': find_char(i),
            'literal': len(char) == 1
        })

    return {
        'table': table
    }


def char2tile(ch):
    # Lazily yanked out of Cosmore's DrawTextLine()
    if ch >= ord('a'):
        offset = 0x0ac8 + ((ch - ord('a')) * 40)
    else:
        offset = 0x0050 + ((ch - 0x18) * 40)
    return offset / 40


def find_char(tile):
    for c in range(255, -1, -1):
        if char2tile(c) == tile:
            res = f"{repr(chr(c))}"
            if res == '"\'"':
                res = "'\\''"
            return res
    return None
