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


def test_latex_inline_with_underline():
    text, should = __wrap(
        r'abc $ \mathop{P}_{2}=x_{4} $ abc',
        r'<p>abc $ \mathop{P}_{2}=x_{4} $ abc</p>'
    )
    output = render(text)
    assert output == should


def test_latex_with_ampersand():
    text, should = __wrap(
        r'$$ a & b & c \\ $$',
        r'$$ a & b & c \\ $$' + '\n'
    )
    output = render(text)
    assert output == should


def test_no_latex_in_code():
    text, should = __wrap(
        '```\n$ sh test.sh\n$ ls\n```',
        '<pre><code>$ sh test.sh\n$ ls\n</code></pre>\n'
    )
    output = render(text)
    assert output == should


def test_dollar_sign():
    text, should = __wrap(
        r'I have \$10 and _you_ have \$20',
        r'<p>I have $10 and <em>you</em> have $20</p>'
    )
    output = render(text)
    assert output == should


def test_no_latex_in_offset_formatted_code():
    text = ('text\n\n    $code$ 1\n    code2\n\ntext')
    expect = '<p>text</p>\n<pre><code>$code$ 1\ncode2\n</code></pre>\n<p>text</p>'
    assert render(text) == expect


def test_escaped_dollar_sign_in_code():
    text, should = __wrap(
        '```\n$ cp . arc\\$(pwd)\n$ ls\n```',
        '<pre><code>$ cp . arc\\$(pwd)\n$ ls\n</code></pre>\n'
    )
    output = render(text)
    assert output == should


@pytest.mark.skip('Bug in the markdown library')
def test_markdown_with_escpaed_dollar_sign():
    from markdown import markdown
    text = '```\n$ cp . arc\\$(pwd)\n```'
    should = '<pre><code>$ cp . arc\\$(pwd)</code></pre>\n'
    assert markdown(text) == should


def __wrap(text, output):
    raw = ''.join(['there is header here\n\n', text,
                   '\n\nand footer down here'])
    res = ''.join(['<p>there is header here</p>\n', output,
                  '\n<p>and footer down here</p>'])
    return raw, res
