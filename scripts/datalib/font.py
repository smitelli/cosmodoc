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
        2: '\u2191',
        3: '\u2193',
        5: '\u2190',
        6: '\u2192',
        8: 'Empty Health Bar, Bottom',
        9: 'Empty Health Bar, Top',
        10: 'Space',
        25: '\u00a3',
        95: 'Filled Health Bar, Top',
        96: 'Filled Health Bar, Bottom',
    }

    table = []

    for i in range(100):
        if i in specials:
            char = specials[i]
        elif i in (0, 1, 4, 7):
            char = 'Solid Black Tile'
        elif 10 <= i < 69:
            char = chr(i + 22)
        elif 69 <= i < 95:
            char = chr(i + 28)
        elif 97 <= i < 100:
            char = 'Solid Gray Tile'
        else:
            raise RuntimeError('huh?')

        table.append({
            'index': i,
            'offset_bytes': i * 40,
            'character': char,
            'literal': len(char) == 1
        })

    return {
        'table': table
    }
