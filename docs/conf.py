import recommonmark.parser

source_suffix = '.md'
source_parsers = {'.md': recommonmark.parser.CommonMarkParser}
master_doc = 'index'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.todo',
              'sphinx.ext.mathjax', 'sphinx.ext.ifconfig', 'sphinx.ext.viewcode']
