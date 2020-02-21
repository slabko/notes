import markdown  # i.e. python-markdown
import re
from typing import Tuple, Dict


def render(text):
    latex_blocks_regex = re.compile(r'\$\$[^$]+\$\$', re.M)
    latex_inline_regex = re.compile(r'(?<!\$)\$[^$]+\$(?!\$)', re.M)
    block_marker = '<div id="latex-{}"></div>'
    inline_marker = '<span id="latex-{}"></span>'

    # text = latex_blocks_regex.sub('<div id="latex-12"></div>', text)
    # text = latex_inline_regex.sub('<span id="latex-10"></span>', text)

    block_replace = replace_and_mark(latex_blocks_regex, block_marker, text)
    text, block_markers = block_replace

    inline_replace = replace_and_mark(latex_inline_regex, inline_marker, text)
    text, inline_markers = inline_replace

    text = markdown.markdown(text, extensions=['fenced_code'])

    for k, v in block_markers.items():
        text = text.replace(k, v)

    for k, v in inline_markers.items():
        text = text.replace(k, v)

    return text


def replace_and_mark(regex, marker, text) -> Tuple[str, Dict[str, str]]:
    index = 0
    matches = {}
    blocks = []
    for i, x in enumerate(regex.finditer(text)):
        m = marker.format(i)
        fr, to = x.span()
        blocks.append(text[index:fr])
        blocks.append(m)
        matches[m] = x.group()
        index = to
    blocks.append(text[index:])
    text = ''.join(blocks)
    return text, matches
