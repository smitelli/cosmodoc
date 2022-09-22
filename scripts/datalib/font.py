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
        0: 'Solid Black Tile',
        1: 'Solid Black Tile',
        2: '\u2191',
        3: '\u2193',
        4: 'Solid Black Tile',
        5: '\u2190',
        6: '\u2192',
        7: 'Solid Black Tile',
        8: 'Empty Health Bar, Bottom',
        9: 'Empty Health Bar, Top',
        25: '\u00a3',
        95: 'Filled Health Bar, Top',
        96: 'Filled Health Bar, Bottom',
        97: 'Solid Gray Tile',
        98: 'Solid Gray Tile',
        99: 'Solid Gray Tile'
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
            'literal': len(char) == 1
        })

    return {
        'table': table
    }
