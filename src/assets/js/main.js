/* jshint esversion: 6 */

(() => {
    function Install(fn) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            fn();
        }
    }

    function HLevel(el) {
        if (!el || !/^h[\d]$/i.test(el.nodeName)) return 0;

        return parseInt(el.nodeName.substring(1, 2), 10);
    }

    Install(() => {
        const toc = document.getElementById('toc-container');
        const headings = document.getElementById('main-page').querySelectorAll('h2,h3,h4,h5,h6');
        let i = 0;

        if (toc === null) return;

        if (headings.length === 0) {
            toc.style.display = 'none';

            return;
        }

        toc.innerHTML = (function buildTocLevel() {
            const level = HLevel(headings[i]);
            let out = '<ul>';

            while (HLevel(headings[i]) === level) {
                out += `<li><a href="#${headings[i].id}">${headings[i].innerHTML}</a>`;

                i++;

                // Recursive nonsense because nested <ul> belongs inside <li>.
                if (HLevel(headings[i]) > level) out += buildTocLevel();

                out += '</li>';
            }

            out += '</ul>';

            return out;
        })();
    });

    Install(() => {
        // `base64 -w0 /path/to/some.png`
        const eyes = {
            '16x16': {
                open: 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAwElEQVQ4y52T0Y3EMAhEH1EKmaZIkaYpdzL3k3id6HbPe0hIwc5gHtghiRXrvXuOJQXAvipuQDrHWkRZUuzfiiMKADuJKG8r4k+2hDCbJwyAbVVYZ+nP+KsK5iTHOYl9lf947F9jXELI9E3k9LgX21+nZ5qoQFL8NpXt3U27df48sT0SjgS9d89lSYqLuSo+851vwQ3stIHhbVq/9ub/JL3GeACtAueLpCpGAwHa1NAbYnu402/j63tUeyH8xyXxA4AspdtjLcmZAAAAAElFTkSuQmCC',
                shut: 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAArklEQVQ4y6VTQQ7DIAxzEA/xp+gj4VP8xLs0NNuKlG6WIpFC4oBdI4kM5pyKOUkDgJIt7gA81LQa1mxxxBgGNcGGqWaLW9PtmYokxrC33BsW/In6tMCZbRhIWs0+3rHuYs9ldFYvijKWzOv7uHeSlp3TIpyxfzRcDeacimORtGMj3xfOf0EdkJoEYEUP330vniN5yXgA6KdFo3miA/vGkYspMu5yX69p/Qq/BEm8APHmqWnfboHWAAAAAElFTkSuQmCC'
            },
            '32x32': {
                open: 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA9hAAAPYQGoP6dpAAAA5ElEQVRYw91XQQ6EIAxsN/sQPoWPpJ/iJ90L3dWJ3RpDItCLwaphpp2pcEqJekatVf/lU0q8X7/o4Xj3Rl7aOms+fY5ZdM/E/AxEyJnlsNaWNybmZQCR3411VOCFOmpYlwFpXe/5gIAq1u0BRGqxwUyYj4FI/1vw/rrTMGe14h+QGmPa8iw86TT0ap9/yE6RR7NiPAZs59itoedDjUvA0HgMRN1q1w1qKw3ZVwXT/w8YImTiRi8QEVFxvjeuD5iX4849przaowqG7QEmokuOZUgM+dU83kdfeJ4BOx1Hp9reMYwKPqH0gpA8/2htAAAAAElFTkSuQmCC',
                shut: 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA9hAAAPYQGoP6dpAAAA2klEQVRYw+1XwQ3DMAg8qgzCUsmQ9lLexH2kVBEVxYlcGbflE8VICdzBgYmZ0dNKKfWdn5np+H7DYFt6Z54M/7ruwFCmekRifgS8zMVy3qmvCol5EbAyF65b7Xu6QHMNpxvCIPAPYPn0DzTn9KiReZXQU77tpS3oR6bhk2vFsSBWp5+GnvaTkXmaTgckcl2tnmmOk4NQPAS8apXnpriV6Xd2D4hbA9budqEWAADJ+F5cHRAt15FbSFncp8YdcTgCBKBJsSQTa+ez/Ppc68J4BOR27N1qe1uYLrgDZpiA49gEBboAAAAASUVORK5CYII='
            }
        };
        // Game runs at ~93ms. FF barely does 120, Chrome is the slow one.
        const delayMs = 205;
        let shutPrev = false;

        setInterval(() => {
            // Game actually used probability 2/40. I'm not that overt.
            const shut = (1 > Math.random() * 100);

            if (shut === shutPrev) return;

            document.querySelectorAll('link[rel="icon"]').forEach(el => {
                const eye = eyes[el.sizes.value];

                el.href = `data:image/png;base64,${shut ? eye.shut : eye.open}`;
            });

            shutPrev = shut;
        }, delayMs);

        // Chrome gives higher priority to "shortcut icon" than "icon"
        document.querySelectorAll('link[rel^="shortcut"]').forEach(el => el.outerHTML = '');
    });

    Install(() => {
        const control = document.getElementById('main-menu-control');
        const page = document.getElementById('main-page');

        page.addEventListener('click', (ev) => {
            if (!control.checked) return;

            ev.preventDefault();
            control.checked = false;
        });
    });
})();

window.addEventListener('load', () => {
    const activeElement = document.querySelector('#main-menu li.active');

    if (activeElement !== null) {
        activeElement.scrollIntoView({block: 'center'});
    }
});
