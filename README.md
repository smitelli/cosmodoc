# Cosmodoc

The Doc for Cosmo.

## Requirements

This project requires the Hugo Extended build, either version v0.90.0 or v0.90.1. Older versions do not support downloading via `resources.Get`, and newer verions change this call to `GetRemote` and break 302 redirects.

## Build the site

This requires a working `hugo` binary.

    cd src
    hugo --path-warnings --templateMetrics

A valid absolute path (with protocol) should be provided for `--baseURL` in production environments, although this only affects the OpenGraph, `wget` footer, robots.txt, and sitemap.xml outputs.

Output files are stored in the top-level `public/` directory. This is an appropriate place to point an HTTP server's document root.

## Renumber the content pages

If there are two pages with weights 10 and 20, a new page can be placed in-between by giving it a weight of 15. After a while there may be a shortage of free weight values to adequately sort new pages. If that happens, run:

    scripts/renumber.py

This will renumber _all_ of the pages in even increments of 10.

## Build the images

The final images are already committed to the repo to ease deployment. It should not be necessary to do this procedure under normal circumstances unless an image has been changed or added. This requires working `inkscape`, `pngquant`, and `optipng` binaries.

Image source material is in the `imgsrc/` directory, which mirrors the naming convention and structure of `src/content/topics/`. The master list of all source files and the list of resized versions to build are in `imgsrc/manifest.txt`.

    scripts/imgmake.py

The script tries not to rebuild existing files unless the source was modified more recently then the existing destination. This relies on the filesystem having sane mtimes on all the files.

To forcefully delete all builable image versions, run:

    scripts/imgmake.py clean

## Build the content data files

In the below examples, `$FILE` and `$DIR` are things you know how to fill in correctly.

    scripts/generate.py actor -c $FILE > src/data/actor.json
    scripts/generate.py font > src/data/font.json
    scripts/generate.py map -d $DIR > src/data/map.json
    scripts/generate.py music -d $DIR > src/data/music.json
    scripts/generate.py sound -d $DIR > src/data/sound.json
    scripts/generate.py sprite -f ACTRINFO.MNI > src/data/actor_sprite.json
    scripts/generate.py sprite -f PLYRINFO.MNI > src/data/player_sprite.json
    scripts/generate.py sprite -f CARTINFO.MNI > src/data/cartoon_sprite.json

## Audio conversion

Just use whatever FFmpeg generates by default. Quality 4 is "good enough."

    ffmpeg -i in.wav -q:a 4 out.mp3
    ffmpeg -i in.wav -q:a 4 out.m4a

The M4A/AAC files sometimes sound kinda goofy. There's probably a way to correct that with a command option.

## What's the current word count?

It's never going to be exact with this type of writing -- too many symbols and embedded shortcodes. Still, this feels pretty close.

    find src/content \( -iname '*.md' -o -iname '*.yml' \) -exec cat {} + | \
        sed "s/[^0-9A-Za-z',]/ /g" | wc -w

or...

    cd src
    hugo -e disable-nav
    # Using the python "html2text" package...
    find ../public/ -iname '*.html' -exec html2text --ignore-links \
        --ignore-tables --ignore-emphasis --ignore-images {} \; | wc -w

Round it down to the nearest 1,000.
