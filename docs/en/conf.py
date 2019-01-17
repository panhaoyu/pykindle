import recommonmark.parser

source_parsers = {
    '.md': recommonmark.parser.CommonMarkParser,
}

master_doc = 'index'
source_suffix = ['.md']
