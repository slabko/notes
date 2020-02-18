"""

To run the script call

    PYTHONPATH=$(pwd) python ./notes/bin/test_data.py

"""
import os
from notes.data import dbsession
from notes.data.page import Page

markdown_content = r'''# Forms of linear equations

## Point-Slope Form

<div style="border-style: solid;">
$$ y - y' = m(x - x') $$
</div>

where $x'$ and $y'$ are values for known coordinates and me equals the slope,
i.e.

$$ m = \frac{\Delta y}{\Delta x} $$

Then

$$ y = y' + m(x - x') $$

## Slope Intercept Form

If we know $y$ for $x = 0$ then we get "Slope intercept form":

$$ y = y_0 + m(x - 0) \implies y = y_0 + mx $$

Let $c = y_0$, then

<div style="border-style: solid;">
$$ y = m x + c $$
</div>

## Standard Form

$$ Ax + Bx = C $$

Where $A$ and $B$ define the slope as ${B \over A}$ or **rise over run**.

# Some unrelated info

Some code:

```python
@blueprint.route('/pages/<created_at_int>')
def page(created_at_int):
    session = create_session()
    page = session.query(Page).\
        filter(Page.created_at_int == created_at_int).\
        first()

    content = markdown.markdown(page.body, extensions=['fenced_code'])
    return flask.render_template('pages/page.html', content=content, page=page)
```

Formulas: 

$$ \det A = \sum_{j=1}^{n}  a_{1j} (-1)^{1+j} \det A_{1j} = \\ = a_{11} \det A_{11} - a_{12} \det A_{12} + ... + a_{1n} (-1)^{1+n} \det A_{1n} $$


Integrals:

$$ \int f'(x) dx = f(x) $$

Inverse of the change-of-coordinate matrix

<div>
$$ \left({\mathop{P}_{C \leftarrow B}}\right)^{-1} = \mathop{P}_{B \leftarrow C} $$
</div>


A big thing:

<div>
$$ adj A = \begin{bmatrix}
C_{11} & C_{21} & \cdots & C_{n1} \\
C_{12} & C_{22} & \cdots & C_{n2} \\
\vdots & \vdots & \ddots & \vdots \\
C_{1n} & C_{2n} & \cdots & C_{nn}
\end{bmatrix} $$
</div>'''


def main():
    init_db()

    session = dbsession.create_session()

    page = Page()
    title, text = markdown_content.lstrip().split('\n', 1)
    page.title = title.lstrip('# ')
    page.preview = text[:100]
    page.body = markdown_content

    session.add(page)
    session.commit()


def init_db():
    current_directory = os.getcwd()
    db_path = os.path.join(current_directory, 'notes.sqlite')
    db_path = os.path.abspath(db_path)
    dbsession.global_init(db_path)


if __name__ == "__main__":
    main()
