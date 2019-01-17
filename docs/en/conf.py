from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}
master_doc = 'index'
source_suffix = ['.md']
