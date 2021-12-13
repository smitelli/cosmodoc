import ctypes
import json
from pathlib import Path

MAP_FILES = [
    'A1.MNI', 'A2.MNI', 'A3.MNI', 'A4.MNI', 'A5.MNI', 'A6.MNI', 'A7.MNI',
    'A8.MNI', 'A9.MNI', 'A10.MNI', 'A11.MNI', 'BONUS1.MNI', 'BONUS2.MNI',
    'B1.MNI', 'B2.MNI', 'B3.MNI', 'B4.MNI', 'B5.MNI', 'B6.MNI', 'B7.MNI',
    'B8.MNI', 'B9.MNI', 'B10.MNI', 'BONUS3.MNI', 'BONUS4.MNI',
    'C1.MNI', 'C2.MNI', 'C3.MNI', 'C4.MNI', 'C5.MNI', 'C6.MNI', 'C7.MNI',
    'C8.MNI', 'C9.MNI', 'C10.MNI', 'BONUS5.MNI', 'BONUS6.MNI']

MUSIC_FILES = [
    'MCAVES.MNI', 'MSCARRY.MNI', 'MBOSS.MNI', 'MRUNAWAY.MNI', 'MCIRCUS.MNI',
    'MTEKWRD.MNI', 'MEASYLEV.MNI', 'MROCKIT.MNI', 'MHAPPY.MNI', 'MDEVO.MNI',
    'MDADODA.MNI', 'MBELLS.MNI', 'MDRUMS.MNI', 'MBANJO.MNI', 'MEASY2.MNI',
    'MTECK2.MNI', 'MTECK3.MNI', 'MTECK4.MNI', 'MZZTOP.MNI']

SOUND_FILES = ['SOUNDS.MNI', 'SOUNDS2.MNI', 'SOUNDS3.MNI']

ERROR_RATE_HZ = 1193181.818181 / 1192030  # Game runs slightly FASTER than ideal
MUSIC_RATE_HZ = 560 * ERROR_RATE_HZ
SOUND_RATE_HZ = 140 * ERROR_RATE_HZ


class MapHeaderStruct(ctypes.LittleEndianStructure):
    _fields_ = [
        ('backdrop_id', ctypes.c_uint16, 5),
        ('rain_flag', ctypes.c_uint16, 1),
        ('backdrop_hscroll_flag', ctypes.c_uint16, 1),
        ('backdrop_vscroll_flag', ctypes.c_uint16, 1),
        ('palette_animation_id', ctypes.c_uint16, 3),
        ('music_id', ctypes.c_uint16, 5),
        ('width_tiles', ctypes.c_uint16),
        ('actor_size_words', ctypes.c_uint16)
    ]

    @property
    def height_tiles(self):
        return int(0x8000 / self.width_tiles)

    @property
    def num_actors(self):
        return int(self.actor_size_words / 3)


class ActorStruct(ctypes.LittleEndianStructure):
    _fields_ = [
        ('type', ctypes.c_uint16),
        ('x_tiles', ctypes.c_uint16),
        ('y_tiles', ctypes.c_uint16)
    ]

    @property
    def is_player(self):
        return (self.type == 0)

    @property
    def is_platform(self):
        return (self.type == 1)

    @property
    def is_fountain(self):
        return (2 <= self.type <= 5)

    @property
    def is_light(self):
        return (6 <= self.type <= 8)

    @property
    def real_type(self):
        if self.type < 31:
            raise ValueError('not a real actor type')
        return self.type - 31


class InfoHeaderStruct(ctypes.LittleEndianStructure):
    _fields_ = [
        ('offset_words', ctypes.c_uint16)
    ]

    @property
    def offset_bytes(self):
        return self.offset_words * 2


class InfoEntryStruct(ctypes.LittleEndianStructure):
    _fields_ = [
        ('height_tiles', ctypes.c_uint16),
        ('width_tiles', ctypes.c_uint16),
        ('frame_offset_bytes', ctypes.c_uint32)
    ]

    @property
    def frame_offset_bytes_fixed(self):
        # Data files are stored in segments, each 0xFFFF bytes long. The offset
        # calculation assumes it's working against segmented data. This method
        # removes that assumption, and returns the true offset as it would be
        # found in the file on disk.
        segment_num = self.frame_offset_bytes >> 16

        return self.frame_offset_bytes - segment_num


class SoundHeaderStruct(ctypes.LittleEndianStructure):
    _fields_ = [
        ('magic', ctypes.c_char * 4),
        ('size_bytes', ctypes.c_uint16),
        ('num_sounds', ctypes.c_uint16),
        ('data1', ctypes.c_uint16),
        ('data2', ctypes.c_char * 6)
    ]


class SoundEntryStruct(ctypes.LittleEndianStructure):
    _fields_ = [
        ('offset_bytes', ctypes.c_uint16),
        ('priority', ctypes.c_uint8),
        ('rate', ctypes.c_uint8),
        ('name', ctypes.c_char * 12)
    ]


def json_minidumps(obj):
    return json.dumps(obj, separators=(',', ':'))


def map_file_iterator(dirname):
    for mf in MAP_FILES:
        yield Path(dirname) / mf


def music_file_iterator(dirname):
    for mf in MUSIC_FILES:
        yield Path(dirname) / mf


def normalize_groupent_name(name):
    return name.upper().replace('.MNI', '')


def sound_file_iterator(dirname):
    for sf in SOUND_FILES:
        yield Path(dirname) / sf
