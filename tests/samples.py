from datetime import datetime
from notes.data.article import Article

page1 = Article(
    id=1,
    title='foo',
    preview='bar',
    created_at=datetime.now(),
    updated_at=datetime.now(),
    body='foo\nbar'
)

page2 = Article(
    id=1,
    title='bar',
    preview='foo',
    created_at=datetime.now(),
    updated_at=datetime.now(),
    body='bar\nfoo'
)
