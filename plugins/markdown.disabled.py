from __future__ import unicode_literals

import codecs

from os import remove
from markdown2 import Markdown
from cactus.utils.filesystem import fileList

# requires markdown2 package, to install it run
# pip install markdown2

template = """
{metadata}
{{% extends "{extends}" %}}
{{% block {block} %}}
{{% verbatim %}}
{html}
{{% endverbatim %}}
{{% endblock %}}
"""

CLEANUP = []
DEFAULT_EXTENDS = 'post.html'
DEFAULT_BLOCK = 'body'

def preBuild(site):
    for path in fileList(site.paths['pages']):

        if not path.endswith('.md'):
            continue

        md = Markdown(extras=[
            'fenced-code-blocks',
            'footnotes',
            'header-ids',
            'metadata',
            'smarty-pants',
            'tables',
        ])

        with codecs.open(path, 'r', 'utf-8') as f:
            html = md.convert(f.read())

        metadata = ['{}: {}'.format(k, v)
                    for k, v in md.metadata.items()]
        out_path = path.replace('.md', '.html')

        extends = md.metadata.get('extends', DEFAULT_EXTENDS)
        block = md.metadata.get('block', DEFAULT_BLOCK)

        with codecs.open(out_path, 'w', 'utf-8') as f:
            data = template.format(
                metadata='\n'.join(metadata),
                html=html,
                extends=extends,
                block=block,
            )
            f.write(data)

        CLEANUP.append(out_path)

def postBuild(site):
    global CLEANUP
    for path in CLEANUP:
        remove(path)
    CLEANUP = []
