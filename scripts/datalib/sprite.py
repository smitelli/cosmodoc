import os
from collections import defaultdict

import datalib.defs

# PAY ATTENTION: ACTRINFO.MNI is written using 16-bit segmented offset values,
# which DO NOT match the offsets in ACTORS.MNI as stored on disk. This module
# takes the (opinionated) stance that the reported offsets should reflect what's
# actually in the disk file, and not in some arcane memory image.


def register_parser(parent):
    parser = parent.add_parser(
        'sprite', help='generate the sprite database')
    parser.add_argument(
        '-f', dest='file', required=True, metavar='FILE',
        help='path to the *INFO.MNI file')
    parser.set_defaults(command_func=run)


def run(args):
    db = parse_sprite_data(args.file)

    print(datalib.defs.json_minidumps(db.to_dict()))


###############################################################################


class SpriteDB:
    def __init__(self):
        self.table = defaultdict(list)

    def insert(self, type_, frame, info_entry):
        self.table[type_].append({
            'sprite_type': type_,
            'sprite_frame': frame,
            'width_tiles': info_entry.width_tiles,
            'height_tiles': info_entry.height_tiles,
            'frame_offset_bytes': info_entry.frame_offset_bytes_fixed  # 16-bit begone
        })

    def to_dict(self):
        return {
            'table': [self.table[k] for k in sorted(self.table.keys())],
            'index': {},
            'sort': {}
        }


def parse_sprite_data(file):
    sprite_db = SpriteDB()

    with open(file, 'rb') as f:
        offset_bytes_index = []

        while True:
            if f.tell() in offset_bytes_index:
                break

            header = datalib.defs.InfoHeaderStruct()
            f.readinto(header)

            offset_bytes_index.append(header.offset_bytes)

        for type_, offset_bytes in enumerate(offset_bytes_index):
            try:
                stop = min([o for o in offset_bytes_index if o > offset_bytes])
            except ValueError:
                # Special case for last block of entries in the file
                stop = os.fstat(f.fileno()).st_size

            f.seek(offset_bytes)

            frame = 0
            while f.tell() < stop:
                entry = datalib.defs.InfoEntryStruct()
                f.readinto(entry)

                sprite_db.insert(type_=type_, frame=frame, info_entry=entry)

                frame += 1

    return sprite_db
