from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}
master_doc = 'index.md'
source_suffix = ['.md']
