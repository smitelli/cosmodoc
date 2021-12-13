import os

import datalib.defs


def register_parser(parent):
    parser = parent.add_parser(
        'sound', help='generate the sound database')
    parser.add_argument(
        '-d', dest='dirname', required=True, metavar='DIR',
        help='path containing all expected sound data .MNI files')
    parser.set_defaults(command_func=run)


def run(args):
    db = parse_sound_data(args.dirname)

    print(datalib.defs.json_minidumps(db.to_dict()))


###############################################################################


class SoundDB:
    def __init__(self):
        self.table = []
        self.game_index = 0

    def insert(self, filename, index, sound_entry):
        groupent_name = datalib.defs.normalize_groupent_name(os.path.basename(filename))

        # Game reads 23 sounds, but each file has 24. Last file isn't filled up.
        if index > 22 or (groupent_name == 'SOUNDS3' and index > 18):
            show_game_index = False
        else:
            show_game_index = True
            self.game_index += 1

        size_bytes = self.find_data_size(filename, sound_entry.offset_bytes)

        if size_bytes > 4:
            # A guess. 2 bytes/interrupt, SOUND_RATE_HZ ints/sec, 1000 ms/sec.
            length_ms = ((size_bytes - 2) / (2 * datalib.defs.SOUND_RATE_HZ)) * 1000
        else:
            # In practice, tiny sounds consist only of silence
            length_ms = 0

        self.table.append({
            'groupent_name': groupent_name,
            'groupent_index': index,
            'game_index': self.game_index if show_game_index else None,
            'offset_bytes': sound_entry.offset_bytes,
            'size_bytes': size_bytes,
            'priority': sound_entry.priority,
            'name': sound_entry.name.decode(),
            'length_ms': round(length_ms)
        })

    @staticmethod
    def find_data_size(filename, offset):
        size_bytes = 0

        with open(filename, 'rb') as f:
            f.seek(offset)

            while True:
                check = f.read(2)
                len_check = len(check)
                size_bytes += len_check

                if len_check < 2 or check == b'\xFF\xFF':
                    break

        return size_bytes

    def to_dict(self):
        return {
            'table': self.table,
            'index': {},
            'sort': {}
        }


def parse_sound_data(dirname):
    sound_db = SoundDB()

    for filename in datalib.defs.sound_file_iterator(dirname):
        with open(filename, 'rb') as f:
            header = datalib.defs.SoundHeaderStruct()
            f.readinto(header)

            for i in range(header.num_sounds):
                snd = datalib.defs.SoundEntryStruct()
                f.readinto(snd)

                sound_db.insert(filename, i, snd)

    return sound_db
