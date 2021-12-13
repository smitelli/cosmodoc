import os
from collections import defaultdict

import datalib.defs


def register_parser(parent):
    parser = parent.add_parser(
        'music', help='generate the music info database')
    parser.add_argument(
        '-d', dest='dirname', required=True, metavar='DIR',
        help='path containing all expected music .MNI files')
    parser.set_defaults(command_func=run)


def run(args):
    db = parse_music_data(args.dirname)

    print(datalib.defs.json_minidumps(db.to_dict()))


###############################################################################


class MusicDB:
    def __init__(self):
        self.table = []

    def insert(self, music_name, cycles, writes):
        self.table.append({
            'music_name': music_name,
            'cycles': cycles,
            'writes': writes,
            'duration': self.cycles_to_duration(cycles)
        })

    @staticmethod
    def cycles_to_duration(cycles):
        seconds = cycles / datalib.defs.MUSIC_RATE_HZ

        minutes = int(seconds / 60)
        seconds = seconds % 60

        return f'{minutes}:{seconds:06.3f}'

    def to_dict(self):
        return {
            'table': self.table,
            'index': {},
            'sort': {}
        }


def parse_music_data(dirname):
    music_db = MusicDB()

    for filename in datalib.defs.music_file_iterator(dirname):
        music_name = datalib.defs.normalize_groupent_name(os.path.basename(filename))

        with open(filename, 'rb') as f:
            data = f.read()

        cycles = 0
        writes = 0
        pos = 0
        while True:
            if pos >= len(data):
                break

            # vals = int.from_bytes(data[pos + 0:pos + 1], byteorder='little')
            wait = int.from_bytes(data[pos + 2:pos + 4], byteorder='little')

            cycles += wait
            writes += 1
            pos += 4

        music_db.insert(music_name, cycles, writes)

    return music_db
