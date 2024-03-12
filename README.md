# Cosmodoc

The Doc for Cosmo.

## Requirements

This project requires the Hugo Extended build, and was most recently verified against Hugo v0.121.0.

## Build the site

This requires a working `hugo` binary.

```bash
cd src
hugo --printPathWarnings --printUnusedTemplates --templateMetrics
```

A valid absolute path (with protocol) should be provided for `--baseURL` in production environments, although this only affects the OpenGraph, `wget` footer, robots.txt, and sitemap.xml outputs.

Output files are stored in the top-level `public/` directory. This is an appropriate place to point an HTTP server's document root.

## Regenerate the syntax highlighter CSS

```bash
cd src
hugo gen chromastyles --style=monokailight > assets/scss/syntax.scss
```

## Renumber the content pages

If there are two pages with weights 10 and 20, a new page can be placed in-between by giving it a weight of 15. After a while there may be a shortage of free weight values to adequately sort new pages. If that happens, run:

```bash
scripts/renumber.py
```

This will renumber _all_ of the pages in even increments of 10.

## Build the images

The final images are already committed to the repository to ease deployment. It should not be necessary to do this procedure under normal circumstances unless an image has been changed or added. This requires working `inkscape`, `pngquant`, and `optipng` binaries.

Image source material is in the `imgsrc/` directory, which mirrors the naming convention and structure of `src/content/topics/`. The master list of all source files and the list of resized versions to build are in `imgsrc/manifest.txt`.

```bash
scripts/imgmake.py
```

The script tries not to rebuild existing files unless the source was modified more recently then the existing destination. This relies on the filesystem having sane mtimes on all the files.

To forcefully delete all buildable image versions, run:

```bash
scripts/imgmake.py clean
```

## Build the content data files

In the below examples, `$FILE` and `$DIR` are things you know how to fill in correctly.

```bash
scripts/generate.py actor -c $FILE > src/data/actor.json
scripts/generate.py font > src/data/font.json
scripts/generate.py map -d $DIR > src/data/map.json
scripts/generate.py music -d $DIR > src/data/music.json
scripts/generate.py sound -d $DIR > src/data/sound.json
scripts/generate.py sprite -f ACTRINFO.MNI > src/data/actor_sprite.json
scripts/generate.py sprite -f PLYRINFO.MNI > src/data/player_sprite.json
scripts/generate.py sprite -f CARTINFO.MNI > src/data/cartoon_sprite.json
```

## AdLib examples

```bash
scripts/make-adlib-examples.py
```

The scripts produce WAV files, but MP3/M4A is preferred for the web. Use whatever [FFmpeg](https://ffmpeg.org/) generates by default. Quality 4 is "good enough."

```bash
ffmpeg -i in.wav -q:a 4 out.mp3
ffmpeg -i in.wav -q:a 4 out.m4a
```

The M4A/AAC files sometimes sound kinda goofy. There's probably a way to better tune that with a command option.

## Diff rendered pages between Hugo versions

Here we went from Hugo v0.90.1 to v0.107.0, which was rather noisy.

```bash
cd src

hugo
find ../public -type f -exec sed -Ei 's/"Hugo [0-9\.]+"/"HUGOVERSION"/g' {} +
mv ../public ../public-orig

# <Put new hugo-extended binary into e.g. /usr/local/bin/hugo-107>
hugo-107
find ../public -type f -exec sed -Ei 's/"Hugo [0-9\.]+"/"HUGOVERSION"/g' {} +
```

Find overall differences:

```bash
diff -rq ../public-orig ../public
```

Find specific differences in one HTML-ish file:

```bash
diff <(tr -s '>' '\n' < ../public-orig/topics/FOO/index.html) <(tr -s '>' '\n' < ../public/topics/FOO/index.html)
```

## Deployment

If you're interested in how this gets deployed (and _dear god why are you_) then consider sniffing around [the Salt states.](https://github.com/smitelli/salt/blob/master/states/website/cosmodoc-org.sls)
