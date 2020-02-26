import markdown  # i.e. python-markdown
import re
from typing import Tuple, Dict


def render(text):
    latex_blocks_regex = re.compile(r'\$\$[^$]+\$\$', re.M)
    latex_inline_regex = re.compile(r'(?<!\\)\\\(.*?(?<!\\)\\\)')
    code_quote_regex = re.compile(r'(```|`)[^`]+(```|`)', re.M)
    code_block_regex = re.compile(r'\n\n(^ {4}.*)+', re.M | re.DOTALL)

    block_marker = '<div id="latex-block-marker-{}"></div>'
    inline_marker = '<span id="latex-inline-marker-{}"></span>'
    code_quote_marker = '<div id="code-quote-marker-{}"></div>'
    code_block_marker = '<div id="code-block-marker-{}"></div>'

    # Remove all code blocks
    code_quote_replace = replace_and_mark(code_quote_regex,
                                          code_quote_marker,
                                          text)
    text, code_quote_markers = code_quote_replace

    code_block_replace = replace_and_mark(code_block_regex,
                                          code_block_marker,
                                          text)
    text, code_block_markers = code_block_replace

    block_replace = replace_and_mark(latex_blocks_regex, block_marker, text)
    text, block_markers = block_replace

    inline_replace = replace_and_mark(latex_inline_regex, inline_marker, text)
    text, inline_markers = inline_replace

    # Unescape dollar signs
    text = text.replace(r'\$', '$')

    # Put code blocks back
    for k, v in code_quote_markers.items():
        text = text.replace(k, v)

    for k, v in code_block_markers.items():
        text = text.replace(k, v)

    text = markdown.markdown(text, extensions=['fenced_code'])

    for k, v in inline_markers.items():
        text = text.replace(k, v)

    for k, v in block_markers.items():
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
