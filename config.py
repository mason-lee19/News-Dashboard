##### Source List ######
NEWS_SOURCE_LIST = [
    'bloomberg',
    'buisness-insider',
    'msnbc',
    'the-wall-street-journal'
]

TICKERS = [
    'AAPL',
    'BA',
    'GOOGL',
    'TSLA',
    'WDC',
    'COST',
    'SPR',
]

IGNORABLE_KEYWORDS = [
    "the",
    "to",
    "of",
    "in",
    "for",
    "stock",
    "market",
    "a",
    "as",
    "and",
    "is",
    "after",
    "are",
    "it",
    "on",
    "its",
    "says",
    "the",
    "at",
    "about",
    "us",
    "has",
    "what",
    "could",
    "but",
    "from",
    "you"
]
IGNORABLE_KEYWORDS = set(IGNORABLE_KEYWORDS)