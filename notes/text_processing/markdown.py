import markdown  # i.e. python-markdown
import re


def render(text):
    return markdown.markdown(text, extensions=['fenced_code'])


def __text_preprocessor(text):
    regex = re.compile(r'\$\$[^$]+\$\$', re.M)
    index = 0
    blocks = []
    res = regex.finditer(text)
    for x in res:
        fr, to = x.span()
        blocks.append(text[index:fr])
        blocks.append('<div class="block-formula">')
        blocks.append(text[fr:to])
        blocks.append('</div>\n')
        index = to
    blocks.append(text[index:])
    text = ''.join(blocks)

    regex = re.compile(r'(?<!\$)\$(?!\$)[^$]+(?<!\$)\$(?!\$)')
    index = 0
    blocks = []
    res = regex.finditer(text)
    for x in res:
        fr, to = x.span()
        blocks.append(text[index:fr])
        blocks.append(text[fr:to].replace('_', r'\_'))
        index = to
    blocks.append(text[index:])
    return ''.join(blocks)
