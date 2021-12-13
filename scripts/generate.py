#!/usr/bin/env python3.7

import sys
from argparse import ArgumentParser

import datalib.actor
import datalib.font
import datalib.map
import datalib.music
import datalib.sound
import datalib.sprite

parser = ArgumentParser(description='Table data generator utility')


def usage(args):
    parser.print_usage()
    sys.exit(2)


def main():
    parser.add_argument(
        '-V', '--version', action='version', version='%(prog)s 0.0.1')
    parser.set_defaults(command_func=usage)

    commands = parser.add_subparsers(metavar='COMMAND')
    datalib.actor.register_parser(commands)
    datalib.font.register_parser(commands)
    datalib.map.register_parser(commands)
    datalib.music.register_parser(commands)
    datalib.sound.register_parser(commands)
    datalib.sprite.register_parser(commands)

    args = parser.parse_args()
    args.command_func(args)


if __name__ == '__main__':
    main()
