#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "ruamel.yaml==0.19.1",
# ]
# ///

'''
Before running, make all the C symbols public:

    find src/ -name *.c -print0 | xargs -0 sed -i 's/^static //g'

Add "PUBLIC MyProcedure" to everything in lowelevel.asm that doesn't have it.

Compile each episode as usual and save the *.MAP files. Then fix this script
because it's just terrible.
'''

import re
from ruamel.yaml import YAML


def address_to_linear(addr):
    if re.match(r'[0-9A-F:]{9}', addr):
        # ABCD:1234 format
        seg, off = addr.split(':')
        return int(f'{seg}0', 16) + int(off, 16)
    elif re.match(r'[0-9A-F]{5}H', addr):
        # ACF04H format
        return int(addr.rstrip('H'), 16)

    return None


def mapfile_to_symbols(filename):
    starts = set()
    symbols = {}

    with open(filename, 'r') as f:
        in_public_table = False
        for line in f.readlines():
            if 'Publics by Value' in line:
                in_public_table = True

            parts = list(filter(None, re.split(r'\s+', line)))

            try:
                test_address = address_to_linear(parts[0])
            except IndexError:
                continue

            if test_address is not None:
                starts.add(test_address)

                if in_public_table:
                    address, symbol_name = parts[0], parts[-1]
                    assert symbol_name not in symbols
                    symbols[symbol_name] = address

    for sym, start in symbols.items():
        linstart = address_to_linear(start)

        try:
            end = min([s for s in starts if s > linstart])
            size = end - linstart
        except ValueError:
            print(f'Unknown size for {sym}')
            size = None

        symbols[sym] = (start, size)

    return symbols


def rewrite(filename, symbols, namespace):
    yaml = YAML()
    yaml.width = 500

    with open(filename, 'r') as f:
        cref = yaml.load(f)

    for yaml_key in cref.keys():
        if yaml_key not in symbols and f'_{yaml_key}' in symbols:
            sym = f'_{yaml_key}'
        else:
            sym = yaml_key

        try:
            (start, size) = symbols[sym]
        except KeyError:
            print(f'Nothing in symbol table for {sym}')
            continue

        if 'symbol_address' not in cref[yaml_key]:
            cref[yaml_key]['symbol_address'] = {}
        cref[yaml_key]['symbol_address'][namespace] = start

        if 'size' not in cref[yaml_key]:
            cref[yaml_key]['size'] = {}
        cref[yaml_key]['size'][namespace] = size

    with open(filename, 'w') as f:
        yaml.dump(cref, f)


def main():
    for i in [1, 2, 3]:
        syms = mapfile_to_symbols(f'./COSMORE{i}.MAP')
        rewrite('../src/data/cref.yml', syms, f'E{i}')


if __name__ == '__main__':
    main()
