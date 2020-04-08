from sqlalchemy import (
    Column, String
)
from .utils.slug import slugify


class SlugColumn(Column):
    def __init__(self, *args, source="title", **kwargs):
        kwargs["default"] = lambda ctx: slugify(
            ctx.get_current_parameters()[source]
        )

        if (
            len(args) < 2 or
            not hasattr(args[1], "_sqla_type")
        ):
            kwargs["type_"] = String

        super().__init__(*args, **kwargs)
