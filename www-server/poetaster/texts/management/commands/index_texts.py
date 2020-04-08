from texts.models import Text, Author
from texts.documents import TextDocument, AuthorDocument
from common.management.commands import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for doc in [TextDocument, AuthorDocument]:
            doc._index.delete()
            doc.init()

        for text in self.session.query(Text).all():
            index = TextDocument(
              title=text.title, raw=text.raw,
              slug=text.slug, author={
                "name": text.author.name,
                "slug": text.author.slug})
            index.save()
            print(index)

        for author in self.session.query(Author).all():
            index = AuthorDocument(name=author.name, slug=author.slug)
            index.save()
            print(index)
