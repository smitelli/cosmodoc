+++
title = "B800 Text Format"
description = "An analysis of the text screens shown when the game ends."
weight = 160
+++

# `B800` Text Format

{{< table-of-contents >}}

Most shareware (and registered!) games of the era displayed a full-screen text page immediately before returning to the DOS prompt, and _Cosmo_ was no exception:

{{< image src="b800-example-2052x.png"
    alt="Sample of a full screen of B800 text."
    1x="b800-example-684x.png"
    2x="b800-example-1368x.png"
    3x="b800-example-2052x.png" >}}

These screens showed colorful line-drawn boxes, customarily in front of a background that resembled the closed curtains on a theater stage. Most contained teasers and ordering information in the case of shareware episodes, or messages thanking the player for purchasing the registered episodes.

Much less commonly, this type of text display was used to provide a more substantial-looking error message in cases where the game was unable to run on a particular system:

{{< image src="b800-low-memory-2052x.png"
    alt="Another sample of B800 text, this time for a low memory error."
    1x="b800-low-memory-684x.png"
    2x="b800-low-memory-1368x.png"
    3x="b800-low-memory-2052x.png" >}}

{{% aside class="armchair-engineer" %}}
**Red Marking Pen**

These were some of the, shall we say, "less proofread" parts of the game.
{{% /aside %}}

There were several `B800` text entries in the game's [group files]({{< relref "group-file-format" >}}):

Entry Name   | Description
-------------|------------
COSMO1.MNI   | End screen for episode 1. Contains teasers for the registered game and ordering information.
COSMO2.MNI   | End screen for episode 2. Contains advertisements for other Apogee games.
COSMO3.MNI   | End screen for episode 3. Identical to COSMO2.MNI except for the episode number in the top line of text.
NOMEMORY.MNI | Error message explaining that the system does not have enough memory.

## The `B800` Mechanism

PC-compatible graphics adapters that supported color usually booted into mode number 03h by default. This was a text mode providing 80x25 characters with 16 colors. The foreground and background color of each character on the screen could be set independently.

`B800` files are named after the segment address where the mode 03h screen buffer is located: `B800:0000`. The 4,000 bytes at this memory-mapped address contain the full screen buffer, and writing data within this address range  immediately changes the text/colors displayed on the screen. That's all the file format is -- 4,000 bytes that are loaded directly into the video memory in order to put characters on the screen.

The printable text content uses 2,000 bytes (80 &times; 25) of memory, the foreground colors use 1,000 bytes (80 &times; 25 &times; log<sub>2</sub> 16 = 8,000 bits), and the background colors use another 1,000 bytes. The colors are encoded using the standard [RGBI palette]({{< relref "full-screen-image-format#colors-and-palettes" >}}) with one key difference: on the background _only_, the intensity bit flashes the foreground text instead of brightening the background color. `B800` text files utilized this liberally.

## Encoding and Decoding

Within a `B800` text file, and the memory area it mirrors, every even-addressed byte controls the **character** displayed on the screen, and every odd-addressed byte controls the **attributes** (foreground color, background color, flashing) on the character that immediately preceded it.

Characters and attributes are stored in row-major order, starting at the top-left corner of the screen.

### Characters

Unicode 1.0 was less than a year old when the game was released, and DOS PCs were rooted firmly in the world of **code pages**. The basic idea was this: Since there were only eight bits available for each character on the screen, there could only be 256 (2<sup>8</sup>) different characters (or **code points**) to choose from. This isn't too much of a problem if all you're doing is writing using the Latin alphabet, but toss in Cyrillic, Greek, Arabic, Hebrew, Urdu... You run out of encoding space real fast. Using code pages, the system can "switch" to a different display font, where the underlying text data doesn't change but the fonts on the display do:

<table class="full-width">
<tr><th>Byte</th><th>CP437</th><th>CP850</th><th>CP860</th><th>CP737</th><th>CP775</th><th>CP856</th><th>CP861</th><th>CP863</th><th>CP864</th><th>CP866</th></tr>
<tr><th>...</th><td colspan="10">...</td></tr>
<tr><th>80h</th><td>Ç</td><td>Ç</td><td>Ç</td><td>Α</td><td>Ć</td><td>א</td><td>Ç</td><td>Ç</td><td>°</td><td>А</td></tr>
<tr><th>81h</th><td>ü</td><td>ü</td><td>ü</td><td>Β</td><td>ü</td><td>ב</td><td>ü</td><td>ü</td><td>·</td><td>Б</td></tr>
<tr><th>82h</th><td>é</td><td>é</td><td>é</td><td>Γ</td><td>é</td><td>ג</td><td>é</td><td>é</td><td>∙</td><td>В</td></tr>
<tr><th>83h</th><td>â</td><td>â</td><td>â</td><td>Δ</td><td>ā</td><td>ד</td><td>â</td><td>â</td><td>√</td><td>Г</td></tr>
<tr><th>84h</th><td>ä</td><td>ä</td><td>ã</td><td>Ε</td><td>ä</td><td>ה</td><td>ä</td><td>Â</td><td>▒</td><td>Д</td></tr>
<tr><th>85h</th><td>à</td><td>à</td><td>à</td><td>Ζ</td><td>ģ</td><td>ו</td><td>à</td><td>à</td><td>─</td><td>Е</td></tr>
<tr><th>86h</th><td>å</td><td>å</td><td>Á</td><td>Η</td><td>å</td><td>ז</td><td>å</td><td>¶</td><td>│</td><td>Ж</td></tr>
<tr><th>87h</th><td>ç</td><td>ç</td><td>ç</td><td>Θ</td><td>ć</td><td>ח</td><td>ç</td><td>ç</td><td>┼</td><td>З</td></tr>
<tr><th>88h</th><td>ê</td><td>ê</td><td>ê</td><td>Ι</td><td>ł</td><td>ט</td><td>ê</td><td>ê</td><td>┤</td><td>И</td></tr>
<tr><th>89h</th><td>ë</td><td>ë</td><td>Ê</td><td>Κ</td><td>ē</td><td>י</td><td>ë</td><td>ë</td><td>┬</td><td>Й</td></tr>
<tr><th>8Ah</th><td>è</td><td>è</td><td>è</td><td>Λ</td><td>Ŗ</td><td>ך</td><td>è</td><td>è</td><td>├</td><td>К</td></tr>
<tr><th>8Bh</th><td>ï</td><td>ï</td><td>Í</td><td>Μ</td><td>ŗ</td><td>כ</td><td>Ð</td><td>ï</td><td>┴</td><td>Л</td></tr>
<tr><th>8Ch</th><td>î</td><td>î</td><td>Ô</td><td>Ν</td><td>ī</td><td>ל</td><td>ð</td><td>î</td><td>┐</td><td>М</td></tr>
<tr><th>8Dh</th><td>ì</td><td>ì</td><td>ì</td><td>Ξ</td><td>Ź</td><td>ם</td><td>Þ</td><td>‗</td><td>┌</td><td>Н</td></tr>
<tr><th>8Eh</th><td>Ä</td><td>Ä</td><td>Ã</td><td>Ο</td><td>Ä</td><td>מ</td><td>Ä</td><td>À</td><td>└</td><td>О</td></tr>
<tr><th>8Fh</th><td>Å</td><td>Å</td><td>Â</td><td>Π</td><td>Å</td><td>ן</td><td>Å</td><td>§</td><td>┘</td><td>П</td></tr>
<tr><th>90h</th><td>É</td><td>É</td><td>É</td><td>Ρ</td><td>É</td><td>נ</td><td>É</td><td>É</td><td>β</td><td>Р</td></tr>
<tr><th>91h</th><td>æ</td><td>æ</td><td>À</td><td>Σ</td><td>æ</td><td>ס</td><td>æ</td><td>È</td><td>∞</td><td>С</td></tr>
<tr><th>92h</th><td>Æ</td><td>Æ</td><td>È</td><td>Τ</td><td>Æ</td><td>ע</td><td>Æ</td><td>Ê</td><td>φ</td><td>Т</td></tr>
<tr><th>93h</th><td>ô</td><td>ô</td><td>ô</td><td>Υ</td><td>ō</td><td>ף</td><td>ô</td><td>ô</td><td>±</td><td>У</td></tr>
<tr><th>94h</th><td>ö</td><td>ö</td><td>õ</td><td>Φ</td><td>ö</td><td>פ</td><td>ö</td><td>Ë</td><td>½</td><td>Ф</td></tr>
<tr><th>95h</th><td>ò</td><td>ò</td><td>ò</td><td>Χ</td><td>Ģ</td><td>ץ</td><td>þ</td><td>Ï</td><td>¼</td><td>Х</td></tr>
<tr><th>96h</th><td>û</td><td>û</td><td>Ú</td><td>Ψ</td><td>¢</td><td>צ</td><td>û</td><td>û</td><td>≈</td><td>Ц</td></tr>
<tr><th>97h</th><td>ù</td><td>ù</td><td>ù</td><td>Ω</td><td>Ś</td><td>ק</td><td>Ý</td><td>ù</td><td>«</td><td>Ч</td></tr>
<tr><th>98h</th><td>ÿ</td><td>ÿ</td><td>Ì</td><td>α</td><td>ś</td><td>ר</td><td>ý</td><td>¤</td><td>»</td><td>Ш</td></tr>
<tr><th>99h</th><td>Ö</td><td>Ö</td><td>Õ</td><td>β</td><td>Ö</td><td>ש</td><td>Ö</td><td>Ô</td><td>ﻷ</td><td>Щ</td></tr>
<tr><th>9Ah</th><td>Ü</td><td>Ü</td><td>Ü</td><td>γ</td><td>Ü</td><td>ת</td><td>Ü</td><td>Ü</td><td>ﻸ</td><td>Ъ</td></tr>
<tr><th>9Bh</th><td>¢</td><td>ø</td><td>¢</td><td>δ</td><td>ø</td><td>(none)</td><td>ø</td><td>¢</td><td>(none)</td><td>Ы</td></tr>
<tr><th>9Ch</th><td>£</td><td>£</td><td>£</td><td>ε</td><td>£</td><td>£</td><td>£</td><td>£</td><td>(none)</td><td>Ь</td></tr>
<tr><th>9Dh</th><td>¥</td><td>Ø</td><td>Ù</td><td>ζ</td><td>Ø</td><td>(none)</td><td>Ø</td><td>Ù</td><td>ﻻ</td><td>Э</td></tr>
<tr><th>9Eh</th><td>₧</td><td>×</td><td>₧</td><td>η</td><td>×</td><td>×</td><td>₧</td><td>Û</td><td>ﻼ</td><td>Ю</td></tr>
<tr><th>9Fh</th><td>ƒ</td><td>ƒ</td><td>Ó</td><td>θ</td><td>¤</td><td>(none)</td><td>ƒ</td><td>ƒ</td><td>(none)</td><td>Я</td></tr>
<tr><th>...</th><td colspan="10">...</td></tr>
</table>

Note that in the preceding table, _the raw bytes never change._ All that changes from one code page to another is what the visual representation of a code point is.

The lower half of most code pages was the same, mirroring the 7-bit character assignments originally defined by the American Standard Code for Information Interchange (**ASCII**) in the 1960s. This allowed for compatible rendering of the letters A-Z, digits, and common printable punctuation characters across all configurations. The upper half above 80h, however, was a free-for-all.

The prevailing theory of the day was that files would tend to only be opened on computers that were geographically near one another, and all of those computers would be configured to use the same code page for display. If a file was written with the expectation that it would be displayed in one code page, and was instead opened on a computer with a different code page loaded, it may display as abject gibberish. The IBM PC (and most compatibles sold in the Western world) booted into code page 437 (**CP437**) by default.

CP437 defined a few international characters -- mostly currency symbols, accented vowels to properly write out certain names and loanwords from other languages, and enough Greek letters and mathematical symbols to write physics equations. Most of the rest of the characters were for block and box drawing, allowing solid filled areas and continuous single- or double-lines to be drawn in all four directions with corners and intersections. These box drawing characters were integral to some of the first text-based UIs in DOS software. They were also used extensively in `B800` text screens.

The full CP437 character set is as follows:

<table class="full-width">
<tr><th>00h</th><td>(blank)</td><th>20h</th><td>(space)</td><th>40h</th><td>@</td><th>60h</th><td>`</td><th>80h</th><td>Ç</td><th>A0h</th><td>á</td><th>C0h</th><td>└</td><th>E0h</th><td>α</td></tr>
<tr><th>01h</th><td>☺</td>      <th>21h</th><td>!</td>      <th>41h</th><td>A</td><th>61h</th><td>a</td><th>81h</th><td>ü</td><th>A1h</th><td>í</td><th>C1h</th><td>┴</td><th>E1h</th><td>ß</td></tr>
<tr><th>02h</th><td>☻</td>      <th>22h</th><td>"</td>      <th>42h</th><td>B</td><th>62h</th><td>b</td><th>82h</th><td>é</td><th>A2h</th><td>ó</td><th>C2h</th><td>┬</td><th>E2h</th><td>Γ</td></tr>
<tr><th>03h</th><td>♥</td>      <th>23h</th><td>#</td>      <th>43h</th><td>C</td><th>63h</th><td>c</td><th>83h</th><td>â</td><th>A3h</th><td>ú</td><th>C3h</th><td>├</td><th>E3h</th><td>π</td></tr>
<tr><th>04h</th><td>♦</td>      <th>24h</th><td>$</td>      <th>44h</th><td>D</td><th>64h</th><td>d</td><th>84h</th><td>ä</td><th>A4h</th><td>ñ</td><th>C4h</th><td>─</td><th>E4h</th><td>Σ</td></tr>
<tr><th>05h</th><td>♣</td>      <th>25h</th><td>%</td>      <th>45h</th><td>E</td><th>65h</th><td>e</td><th>85h</th><td>à</td><th>A5h</th><td>Ñ</td><th>C5h</th><td>┼</td><th>E5h</th><td>σ</td></tr>
<tr><th>06h</th><td>♠</td>      <th>26h</th><td>&amp;</td>  <th>46h</th><td>F</td><th>66h</th><td>f</td><th>86h</th><td>å</td><th>A6h</th><td>ª</td><th>C6h</th><td>╞</td><th>E6h</th><td>µ</td></tr>
<tr><th>07h</th><td>•</td>      <th>27h</th><td>'</td>      <th>47h</th><td>G</td><th>67h</th><td>g</td><th>87h</th><td>ç</td><th>A7h</th><td>º</td><th>C7h</th><td>╟</td><th>E7h</th><td>τ</td></tr>
<tr><th>08h</th><td>◘</td>      <th>28h</th><td>(</td>      <th>48h</th><td>H</td><th>68h</th><td>h</td><th>88h</th><td>ê</td><th>A8h</th><td>¿</td><th>C8h</th><td>╚</td><th>E8h</th><td>Φ</td></tr>
<tr><th>09h</th><td>○</td>      <th>29h</th><td>)</td>      <th>49h</th><td>I</td><th>69h</th><td>i</td><th>89h</th><td>ë</td><th>A9h</th><td>⌐</td><th>C9h</th><td>╔</td><th>E9h</th><td>Θ</td></tr>
<tr><th>0Ah</th><td>◙</td>      <th>2Ah</th><td>*</td>      <th>4Ah</th><td>J</td><th>6Ah</th><td>j</td><th>8Ah</th><td>è</td><th>AAh</th><td>¬</td><th>CAh</th><td>╩</td><th>EAh</th><td>Ω</td></tr>
<tr><th>0Bh</th><td>♂</td>      <th>2Bh</th><td>+</td>      <th>4Bh</th><td>K</td><th>6Bh</th><td>k</td><th>8Bh</th><td>ï</td><th>ABh</th><td>½</td><th>CBh</th><td>╦</td><th>EBh</th><td>δ</td></tr>
<tr><th>0Ch</th><td>♀</td>      <th>2Ch</th><td>,</td>      <th>4Ch</th><td>L</td><th>6Ch</th><td>l</td><th>8Ch</th><td>î</td><th>ACh</th><td>¼</td><th>CCh</th><td>╠</td><th>ECh</th><td>∞</td></tr>
<tr><th>0Dh</th><td>♪</td>      <th>2Dh</th><td>-</td>      <th>4Dh</th><td>M</td><th>6Dh</th><td>m</td><th>8Dh</th><td>ì</td><th>ADh</th><td>¡</td><th>CDh</th><td>═</td><th>EDh</th><td>φ</td></tr>
<tr><th>0Eh</th><td>♫</td>      <th>2Eh</th><td>.</td>      <th>4Eh</th><td>N</td><th>6Eh</th><td>n</td><th>8Eh</th><td>Ä</td><th>AEh</th><td>«</td><th>CEh</th><td>╬</td><th>EEh</th><td>ε</td></tr>
<tr><th>0Fh</th><td>☼</td>      <th>2Fh</th><td>/</td>      <th>4Fh</th><td>O</td><th>6Fh</th><td>o</td><th>8Fh</th><td>Å</td><th>AFh</th><td>»</td><th>CFh</th><td>╧</td><th>EFh</th><td>∩</td></tr>
<tr><th>10h</th><td>►</td>      <th>30h</th><td>0</td>      <th>50h</th><td>P</td><th>70h</th><td>p</td><th>90h</th><td>É</td><th>B0h</th><td>░</td><th>D0h</th><td>╨</td><th>F0h</th><td>≡</td></tr>
<tr><th>11h</th><td>◄</td>      <th>31h</th><td>1</td>      <th>51h</th><td>Q</td><th>71h</th><td>q</td><th>91h</th><td>æ</td><th>B1h</th><td>▒</td><th>D1h</th><td>╤</td><th>F1h</th><td>±</td></tr>
<tr><th>12h</th><td>↕</td>      <th>32h</th><td>2</td>      <th>52h</th><td>R</td><th>72h</th><td>r</td><th>92h</th><td>Æ</td><th>B2h</th><td>▓</td><th>D2h</th><td>╥</td><th>F2h</th><td>≥</td></tr>
<tr><th>13h</th><td>‼</td>      <th>33h</th><td>3</td>      <th>53h</th><td>S</td><th>73h</th><td>s</td><th>93h</th><td>ô</td><th>B3h</th><td>│</td><th>D3h</th><td>╙</td><th>F3h</th><td>≤</td></tr>
<tr><th>14h</th><td>¶</td>      <th>34h</th><td>4</td>      <th>54h</th><td>T</td><th>74h</th><td>t</td><th>94h</th><td>ö</td><th>B4h</th><td>┤</td><th>D4h</th><td>╘</td><th>F4h</th><td>⌠</td></tr>
<tr><th>15h</th><td>§</td>      <th>35h</th><td>5</td>      <th>55h</th><td>U</td><th>75h</th><td>u</td><th>95h</th><td>ò</td><th>B5h</th><td>╡</td><th>D5h</th><td>╒</td><th>F5h</th><td>⌡</td></tr>
<tr><th>16h</th><td>▬</td>      <th>36h</th><td>6</td>      <th>56h</th><td>V</td><th>76h</th><td>v</td><th>96h</th><td>û</td><th>B6h</th><td>╢</td><th>D6h</th><td>╓</td><th>F6h</th><td>÷</td></tr>
<tr><th>17h</th><td>↨</td>      <th>37h</th><td>7</td>      <th>57h</th><td>W</td><th>77h</th><td>w</td><th>97h</th><td>ù</td><th>B7h</th><td>╖</td><th>D7h</th><td>╫</td><th>F7h</th><td>≈</td></tr>
<tr><th>18h</th><td>↑</td>      <th>38h</th><td>8</td>      <th>58h</th><td>X</td><th>78h</th><td>x</td><th>98h</th><td>ÿ</td><th>B8h</th><td>╕</td><th>D8h</th><td>╪</td><th>F8h</th><td>°</td></tr>
<tr><th>19h</th><td>↓</td>      <th>39h</th><td>9</td>      <th>59h</th><td>Y</td><th>79h</th><td>y</td><th>99h</th><td>Ö</td><th>B9h</th><td>╣</td><th>D9h</th><td>┘</td><th>F9h</th><td>∙</td></tr>
<tr><th>1Ah</th><td>→</td>      <th>3Ah</th><td>:</td>      <th>5Ah</th><td>Z</td><th>7Ah</th><td>z</td><th>9Ah</th><td>Ü</td><th>BAh</th><td>║</td><th>DAh</th><td>┌</td><th>FAh</th><td>·</td></tr>
<tr><th>1Bh</th><td>←</td>      <th>3Bh</th><td>;</td>      <th>5Bh</th><td>[</td><th>7Bh</th><td>{</td><th>9Bh</th><td>¢</td><th>BBh</th><td>╗</td><th>DBh</th><td>█</td><th>FBh</th><td>√</td></tr>
<tr><th>1Ch</th><td>∟</td>      <th>3Ch</th><td>&lt;</td>   <th>5Ch</th><td>\</td><th>7Ch</th><td>|</td><th>9Ch</th><td>£</td><th>BCh</th><td>╝</td><th>DCh</th><td>▄</td><th>FCh</th><td>ⁿ</td></tr>
<tr><th>1Dh</th><td>↔</td>      <th>3Dh</th><td>=</td>      <th>5Dh</th><td>]</td><th>7Dh</th><td>}</td><th>9Dh</th><td>¥</td><th>BDh</th><td>╜</td><th>DDh</th><td>▌</td><th>FDh</th><td>²</td></tr>
<tr><th>1Eh</th><td>▲</td>      <th>3Eh</th><td>&gt;</td>   <th>5Eh</th><td>^</td><th>7Eh</th><td>~</td><th>9Eh</th><td>₧</td><th>BEh</th><td>╛</td><th>DEh</th><td>▐</td><th>FEh</th><td>■</td></tr>
<tr><th>1Fh</th><td>▼</td>      <th>3Fh</th><td>?</td>      <th>5Fh</th><td>_</td><th>7Fh</th><td>⌂</td><th>9Fh</th><td>ƒ</td><th>BFh</th><td>┐</td><th>DFh</th><td>▀</td><th>FFh</th><td>(blank<a href="/404.html" style="display:none;">🐰🥚</a>)</td></tr>
</table>

{{% aside class="fun-fact" %}}
**Everything old is new again.**

There are some precursors to emoji in the CP437 table -- especially the faces, arrows, and playing card suits. Some computers may even display some of the above characters _as_ emoji.
{{% /aside %}}

In files and console output, the control characters (00h-1Fh) represent newlines, tabs, audible beeps, and other commands to move the cursor around. In the video memory, however, these characters have absolutely no special behavior and display a single character just like any other.

### Attributes

Each attribute byte has four bits that control foreground color, three bits that control background color, and one bit that controls flashing of the foreground text:

Bit Position              | Description
--------------------------|------------
0 (least significant bit) | Foreground blue palette bit.
1                         | Foreground green palette bit.
2                         | Foreground red palette bit.
3                         | Foreground intensity palette bit.
4                         | Background blue palette bit.
5                         | Background green palette bit.
6                         | Background red palette bit.
7 (most significant bit)  | `0` = foreground text displays normally, `1` = foreground text flashes.

The default system color was 07h, or low-intensity white on a black background.

The attribute byte affects the character byte that immediately precedes it:

Offset (Bytes) | Description
---------------|------------
0              | Character at (0, 0).
1              | Attributes for character at (0, 0).
2              | Character at (1, 0).
3              | Attributes for character at (1, 0).
...            | ...
3,996          | Character at (78, 24).
3,997          | Attributes for character at (78, 24).
3,998          | Character at (79, 24).
3,999          | Attributes for character at (79, 24).

## Programming Considerations

DOS is unaware of characters drawn directly to video memory, and the cursor position is not updated in any way to reflect the updated contents of the screen. When the program exits, DOS thinks the screen is blank and the most appropriate place for the prompt should be at the current cursor position, which is near the top of the screen. With `B800` text already occupying space on the screen, this naive assumption results in the DOS prompt appearing on top of the text, with new and old characters and attributes jumbling together in an unreadable mess.

Typically, any program that displayed `B800` text would also emit -- usually via {{< lookup/cref printf >}} -- a series of newline characters to move the cursor down far enough to clear the bottom of the displayed text.
