import pytest
from notes.text_processing.markdown import render


def test_headers():
    text = '# header'
    output = render(text)
    assert output == '<h1>header</h1>'


def test_emphasis():
    text, should = __wrap('text _with_ emphasis',
                          '<p>text <em>with</em> emphasis</p>')
    output = render(text)
    assert output == should


def test_code():
    text, should = __wrap(
        '```\nimport pandas\n```',
        '<pre><code>import pandas\n</code></pre>\n'
    )
    output = render(text)
    assert output == should


@pytest.mark.skip('This is the problem I need to solve with markdown')
def test_latex_inline_with_underline():
    text, should = __wrap(
        r'abc $ \mathop{P}_{2}=x_{4} $ abc',
        r'<p>inline $ \mathop{P}_{2}=x_{4} $</p>'
    )
    output = render(text)
    assert output == should


@pytest.mark.skip('This is the problem I need to solve with markdown')
def test_latex_with_ampersand():
    text, should = __wrap(
        r'$$ a & b & c \\ $$',
        r'$$ a & b & c \\ $$'
    )
    output = render(text)
    assert output == should


def __wrap(text, output):
    raw = ''.join(['there is header here\n\n', text,
                   '\n\nand footer down here'])
    res = ''.join(['<p>there is header here</p>\n', output,
                  '\n<p>and footer down here</p>'])
    return raw, res
