# Third Party
from hypothesis.strategies import characters, text

postgres_text = text(alphabet=characters(blacklist_categories=("Cc", "Cs")))
