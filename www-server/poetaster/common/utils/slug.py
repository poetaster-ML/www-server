import re
import unicodedata

from sqlalchemy import func


def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count


def slugify(model, value, session, allow_unicode=False):
    """Normalize and then append an increasing number until unique.
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata \
            .normalize('NFKD', value) \
            .encode('ascii', 'ignore') \
            .decode('ascii')

    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)

    i = 0
    while get_count(session.query(model).filter_by(slug=value)) > 0:
        value += '-' + str(i) if i == 0 else str(i)
        i += 1

    return value
