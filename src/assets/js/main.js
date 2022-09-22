function InitializeTableOfContents() {
    var tocElement = document.getElementById('toc-container'),
        tocHTML = '',
        lastLevel = 1;  //we skip the H1 level

    if (tocElement === null) return;

    document
        .getElementById('main-page')
        .querySelectorAll('h2, h3, h4, h5, h6')
        .forEach(function(el) {
            var level = el.nodeName.substring(1, 2);

            // TODO This isn't technically right; nested <ul> belongs inside <li>
            for (; lastLevel < level; lastLevel++) {
                tocHTML += '<ul>';
            }

            for (; lastLevel > level; lastLevel--) {
                tocHTML += '</ul>';
            }

            tocHTML += '<li><a href="#' + el.id + '">' + el.innerHTML + '</a></li>';
        });

    for (; lastLevel > 1; lastLevel--) {  //again, we skip the H1 level
        tocHTML += '</ul>';
    }

    tocElement.innerHTML = tocHTML;
}

if (document.readyState !== 'loading') {
    InitializeTableOfContents();
} else {
    document.addEventListener('DOMContentLoaded', InitializeTableOfContents);
}

window.addEventListener('load', function() {
    // `base64 -w0 /path/to/some.png`
    var eyes = {
            '16x16': {
                open: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAwElEQVQ4y52T0Y3EMAhEH1EKmaZIkaYpdzL3k3id6HbPe0hIwc5gHtghiRXrvXuOJQXAvipuQDrHWkRZUuzfiiMKADuJKG8r4k+2hDCbJwyAbVVYZ+nP+KsK5iTHOYl9lf947F9jXELI9E3k9LgX21+nZ5qoQFL8NpXt3U27df48sT0SjgS9d89lSYqLuSo+851vwQ3stIHhbVq/9ub/JL3GeACtAueLpCpGAwHa1NAbYnu402/j63tUeyH8xyXxA4AspdtjLcmZAAAAAElFTkSuQmCC',
                shut: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAArklEQVQ4y6VTQQ7DIAxzEA/xp+gj4VP8xLs0NNuKlG6WIpFC4oBdI4kM5pyKOUkDgJIt7gA81LQa1mxxxBgGNcGGqWaLW9PtmYokxrC33BsW/In6tMCZbRhIWs0+3rHuYs9ldFYvijKWzOv7uHeSlp3TIpyxfzRcDeacimORtGMj3xfOf0EdkJoEYEUP330vniN5yXgA6KdFo3miA/vGkYspMu5yX69p/Qq/BEm8APHmqWnfboHWAAAAAElFTkSuQmCC'
            },
            '32x32': {
                open: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA9hAAAPYQGoP6dpAAAA5ElEQVRYw91XQQ6EIAxsN/sQPoWPpJ/iJ90L3dWJ3RpDItCLwaphpp2pcEqJekatVf/lU0q8X7/o4Xj3Rl7aOms+fY5ZdM/E/AxEyJnlsNaWNybmZQCR3411VOCFOmpYlwFpXe/5gIAq1u0BRGqxwUyYj4FI/1vw/rrTMGe14h+QGmPa8iw86TT0ap9/yE6RR7NiPAZs59itoedDjUvA0HgMRN1q1w1qKw3ZVwXT/w8YImTiRi8QEVFxvjeuD5iX4849przaowqG7QEmokuOZUgM+dU83kdfeJ4BOx1Hp9reMYwKPqH0gpA8/2htAAAAAElFTkSuQmCC',
                shut: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA9hAAAPYQGoP6dpAAAA2klEQVRYw+1XwQ3DMAg8qgzCUsmQ9lLexH2kVBEVxYlcGbflE8VICdzBgYmZ0dNKKfWdn5np+H7DYFt6Z54M/7ruwFCmekRifgS8zMVy3qmvCol5EbAyF65b7Xu6QHMNpxvCIPAPYPn0DzTn9KiReZXQU77tpS3oR6bhk2vFsSBWp5+GnvaTkXmaTgckcl2tnmmOk4NQPAS8apXnpriV6Xd2D4hbA9budqEWAADJ+F5cHRAt15FbSFncp8YdcTgCBKBJsSQTa+ez/Ppc68J4BOR27N1qe1uYLrgDZpiA49gEBboAAAAASUVORK5CYII='
            }
        },
        delayMs = 200,  //game timer is roughly 93ms; way too short for Chrome
        shutPrev = null;

    setInterval(function() {
        // Game actually used probability 2/40. I'm not that overt.
        var shut = (Math.random() * 100 > 99);

        if (shut === shutPrev) return;

        document.querySelectorAll('link[rel="icon"]').forEach(function(el) {
            var eye = eyes[el.sizes.value];

            el.href = shut ? eye.shut : eye.open;
        });

        shutPrev = shut;
    }, delayMs);
});

window.addEventListener('load', function() {
    var docHref = document.location.href;

    document
        .getElementById('main-menu')
        .querySelectorAll('li a')
        .forEach(function(el) {
            if (docHref.startsWith(el.href)) {
                try {
                    el.scrollIntoViewIfNeeded();
                } catch (e) {
                    el.scrollIntoView();
                }
            }
        });
});
