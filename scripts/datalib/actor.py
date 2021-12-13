import re

import datalib.defs

MAX_ACTOR_TYPE = 300
ARGS_COUNT = 13
EXTRACTOR = re.compile(
    r'CreateActor\((.+?), (.+?), (.+?), (.+?), (.+?), (.+?), (.+?), (.+?), '
    r'(.+?), (.+?), (.+?), (.+?), (.+?)\);',
    flags=re.M | re.DOTALL)


def register_parser(parent):
    parser = parent.add_parser(
        'actor', help='generate the actor database')
    parser.add_argument(
        '-c', dest='cfile', required=True, metavar='FILE',
        help='path to a .C file containing some version of CreateActorAtIndex')
    parser.set_defaults(command_func=run)


def run(args):
    db = parse_actor_data(args.cfile)

    print(datalib.defs.json_minidumps(db.to_dict()))


###############################################################################


class ActorDB:
    def __init__(self):
        self.table = []

    def insert(self, actor_type, args):
        self.table.append({
            'actor_type': actor_type,
            'sprite_type': int(args[0]),
            'xshift_tiles': int(self.prettify_xypos(args[1], absolute=True)),
            'yshift_tiles': int(self.prettify_xypos(args[2], absolute=True)),
            'always_active_flag': int(args[3]),
            'remains_active_flag': int(args[4]),
            'has_gravity_flag': int(args[5]),
            'ledge_eager_flag': int(args[6]),
            'tick_function': args[7],
            'data1': self.prettify_data(args[8], actor_type),
            'data2': self.prettify_data(args[9], actor_type),
            'data3': self.prettify_data(args[10], actor_type),
            'data4': self.prettify_data(args[11], actor_type),
            'data5': self.prettify_data(args[12], actor_type)
        })

    @staticmethod
    def prettify_xypos(source, absolute=False):
        dest = source.lower()

        # HACK: This is such an oddly specific one-time case
        if 'gamerand' in dest:
            return 'random: 50-145, steps of 5'

        if absolute:
            dest = dest.replace('xpos', '')
            dest = dest.replace('ypos', '')
        else:
            dest = dest.replace('xpos', 'x')
            dest = dest.replace('ypos', 'y')

        dest = dest.replace(' ', '')

        if not dest:
            dest = '0'

        return dest

    @staticmethod
    def prettify_data(source, actor_type):
        if source.lower() == 'type':
            return actor_type
        else:
            return __class__.prettify_xypos(source)

    def to_dict(self):
        return {
            'table': self.table,
            'index': {},
            'sort': {}
        }


def parse_actor_data(cfile):
    with open(cfile, 'r') as f:
        lines = f.readlines()

    def _hunt_for_call(start_line):
        i = start_line
        while True:
            line = lines[i]
            if 'break;' in line:
                break
            match = EXTRACTOR.search(line)
            if match is not None:
                return match
            i += 1
        return False

    actor_db = ActorDB()

    for actor_type in range(MAX_ACTOR_TYPE):
        for line_num, line in enumerate(lines):
            if f'case {actor_type}:' in line:
                match = _hunt_for_call(line_num)
                if match:
                    actor_db.insert(
                        actor_type=actor_type,
                        args=[match.group(i + 1) for i in range(ARGS_COUNT)])
                    break

    return actor_db
