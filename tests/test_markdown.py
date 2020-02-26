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
        r'abc \( \mathop{P}_{2}=x_{4} \) abc',
        r'<p>abc \( \mathop{P}_{2}=x_{4} \) abc</p>'
    )
    output = render(text)
    assert output == should


def test_escape_latex_markers():
    text, should = __wrap(
        r'abc \\( some _not_ latex text \) abc',
        r'<p>abc \( some <em>not</em> latex text ) abc</p>'
    )
    output = render(text)
    assert output == should


def test_escape_in_code_remains_unchanged():
    text, should = __wrap(
        r'abc `\\( some _not_ latex text \)` abc',
        r'<p>abc <code>\\( some _not_ latex text \)</code> abc</p>'
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
        '\n'.join([
            r'```',
            r' $$ sh test.sh',
            r' $$ ls',
            r'```']),
        '\n'.join([
            r'<pre><code> $$ sh test.sh',
            r' $$ ls',
            r'</code></pre>',
            r''])
    )
    output = render(text)
    assert output == should


def test_no_latex_in_offset_formatted_code():
    text = '\n'.join([
        r'text',
        r'',
        r'    \(code\) 1',
        r'    code2',
        r'',
        r'text'
    ])
    expect = '\n'.join([
        r'<p>text</p>',
        r'<pre><code>\(code\) 1',
        r'code2',
        r'</code></pre>',
        r'<p>text</p>'
    ])
    assert render(text) == expect


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
