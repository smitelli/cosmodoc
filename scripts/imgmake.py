#!/usr/bin/env python3

import pathlib
import re
import subprocess
import sys

PNGQUANT_QUALITY = 25

INKSCAPE_BIN = '/usr/local/bin/inkscape-cosmodoc'
PNGQUANT_BIN = '/usr/bin/pngquant'
OPTIPNG_BIN = '/usr/bin/optipng'
IS_CYGWIN = (sys.platform == 'cygwin')


def execute(command_list):
    p = subprocess.Popen(
        command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return_code = p.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, command_list)


def parse_manifest_entry(entry):
    file, *vers = re.split(r'\s+', entry)

    if len(vers) == 0:
        raise RuntimeError(f'No versions for entry {file}')

    return file, vers


def parse_manifest_ver(ver):
    match = re.match(r'([0-9]*)x([0-9]*)', ver)

    if match is None:
        raise RuntimeError(f'Unusable version {ver} encountered')

    try:
        width = int(match.group(1))
    except Exception:
        width = None

    try:
        height = int(match.group(2))
    except Exception:
        height = None

    return width, height


def maybe_make_image(*, source, destination, ver):
    src_str = str(source)
    dest_str = str(destination)

    dest_ver = re.sub(r'\.svg$', f'-{ver}.png', dest_str, flags=re.I)
    assert dest_ver != dest_str

    try:
        if pathlib.Path(dest_ver).stat().st_mtime >= source.stat().st_mtime:
            return
    except FileNotFoundError:
        pass

    make_image(src_str, dest_ver, ver)


def make_image(source, destination, ver):
    if IS_CYGWIN:
        source = subprocess.check_output(['cygpath', '-w', source]).strip().decode()
        destination = subprocess.check_output(['cygpath', '-w', destination]).strip().decode()

    # === INKSCAPE =============================================================

    cmd = [
        INKSCAPE_BIN,
        '--export-area-page',
        '--export-background=#ffffff',
        '--export-background-opacity=255']

    width, height = parse_manifest_ver(ver)
    if width is not None:
        cmd += [f'--export-width={width}']
    if height is not None:
        cmd += [f'--export-height={height}']

    cmd += [f'--export-filename={destination}', source]

    print(f'Executing {" ".join(cmd)}...', end='', flush=True)
    execute(cmd)
    print(f' done.\n')

    # === PNGQUANT =============================================================

    cmd = [
        PNGQUANT_BIN, '--ordered', '--quality', str(PNGQUANT_QUALITY),
        '--speed', '1', '--output', destination, '--force', destination]

    print(f'Executing {" ".join(cmd)}...', end='', flush=True)
    execute(cmd)
    print(f' done.\n')

    # === OPTIPNG ==============================================================

    cmd = [OPTIPNG_BIN, '-o7', '-zm1-9', '-strip', 'all', destination]

    print(f'Executing {" ".join(cmd)}...', end='', flush=True)
    execute(cmd)
    print(f' done.\n')


def make():
    root = pathlib.Path(__file__).resolve().parents[1]

    source = root / 'imgsrc'
    destination = root / 'src/content/topics'
    manifest = source / 'manifest.txt'

    with manifest.open() as f:
        for entry in f.read().splitlines():
            file, vers = parse_manifest_entry(entry)

            for ver in vers:
                maybe_make_image(
                    source=source / file, destination=destination / file, ver=ver)


def clean():
    root = pathlib.Path(__file__).resolve().parents[1]

    destination = root / 'src/content/topics'
    manifest = root / 'imgsrc' / 'manifest.txt'

    with manifest.open() as f:
        for entry in f.read().splitlines():
            file, vers = parse_manifest_entry(entry)

            for ver in vers:
                target = pathlib.Path(re.sub(
                    r'\.svg$', f'-{ver}.png', str(destination / file), flags=re.I))

                if target.exists():
                    print(f'Removing {target}...', end='', flush=True)
                    target.unlink()
                    print(' done.\n')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'clean':
        clean()
    else:
        make()
