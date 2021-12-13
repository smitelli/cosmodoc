import os
from collections import defaultdict

import datalib.defs


def register_parser(parent):
    parser = parent.add_parser(
        'map', help='generate the map header database')
    parser.add_argument(
        '-d', dest='dirname', required=True, metavar='DIR',
        help='path containing all expected map data .MNI files')
    parser.set_defaults(command_func=run)


def run(args):
    db = parse_map_data(args.dirname)

    print(datalib.defs.json_minidumps(db.to_dict()))


###############################################################################


class MapDB:
    def __init__(self):
        self.table = []
        self.index_actor = defaultdict(list)
        self.index_backdrop = defaultdict(list)
        self.index_music = defaultdict(list)
        self.index_palette_animation = defaultdict(list)
        self.index_special_actor = defaultdict(list)

    def insert(self, map_name, header, actors, tiles):
        self.table.append({
            'map_name': map_name,
            'backdrop_id': header.backdrop_id,
            'backdrop_hscroll_flag': header.backdrop_hscroll_flag,
            'backdrop_vscroll_flag': header.backdrop_vscroll_flag,
            'width_tiles': header.width_tiles,
            'height_tiles': header.height_tiles,
            'music_id': header.music_id,
            'palette_animation_id': header.palette_animation_id,
            'rain_flag': header.rain_flag,
            'actor_count': len(actors),
            'fountain_count': sum(1 for act in actors if act.is_fountain),
            'light_count': sum(1 for act in actors if act.is_light),
            'platform_count': sum(1 for act in actors if act.is_platform),
            'player_count': sum(1 for act in actors if act.is_player),
            'tile_size_bytes': len(tiles),
        })

        for act in actors:
            try:
                if map_name not in self.index_actor[act.real_type]:
                    self.index_actor[act.real_type].append(map_name)
            except ValueError:
                if map_name not in self.index_special_actor[act.type]:
                    self.index_special_actor[act.type].append(map_name)

        if map_name not in self.index_backdrop[header.backdrop_id]:
            self.index_backdrop[header.backdrop_id].append(map_name)

        if map_name not in self.index_music[header.music_id]:
            self.index_music[header.music_id].append(map_name)

        if map_name not in self.index_palette_animation[header.palette_animation_id]:
            self.index_palette_animation[header.palette_animation_id].append(map_name)

    def to_dict(self):
        return {
            'table': self.table,
            'index': {
                'actor': self.index_actor,
                'backdrop': self.index_backdrop,
                'music': self.index_music,
                'palette_animation': self.index_palette_animation,
                'special_actor': self.index_special_actor
            },
            'sort': {
                'actor': sorted(self.index_actor.keys()),
                'backdrop': sorted(self.index_backdrop.keys()),
                'music': sorted(self.index_music.keys()),
                'palette_animation': sorted(self.index_palette_animation.keys()),
                'special_actor': sorted(self.index_special_actor.keys())
            }
        }


def parse_map_data(dirname):
    map_db = MapDB()

    for filename in datalib.defs.map_file_iterator(dirname):
        map_name = datalib.defs.normalize_groupent_name(os.path.basename(filename))

        with open(filename, 'rb') as f:
            header = datalib.defs.MapHeaderStruct()
            f.readinto(header)

            actors = []
            for _ in range(header.num_actors):
                act = datalib.defs.ActorStruct()
                f.readinto(act)
                actors.append(act)

            tiles = f.read()

        map_db.insert(map_name, header, actors, tiles)

    return map_db
