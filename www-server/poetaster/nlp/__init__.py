import pkgutil
import functools
from importlib import import_module
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


DEFAULT_BACKEND = "poetaster.nlp.backends.SpacyBackend"


def load_backend(backend_name):
    """Return an nlp backend."""

    try:
        module_bits = backend_name.split(".")
        klass = module_bits.pop()
        return getattr(import_module(".".join(module_bits)), klass)
    except ImportError as e_user:
        # The nlp backend wasn't found. Display a helpful error message
        # listing all built-in nlp backends.
        backend_dir = str(Path(__file__).parent / 'backends')
        available_backends = [
            name for _, name, ispkg in pkgutil.iter_modules([backend_dir])
            if ispkg and name not in {'base'}
        ]
        if backend_name not in [
            'poetaster.nlp.backends.%s' % b for b in available_backends
        ]:
            backend_reprs = map(repr, sorted(available_backends))
            raise ImproperlyConfigured(
                "%r isn't an available nlp backend.\n"
                "Try using 'poetaster.nlp.backends.X', where X is one of:\n"
                "    %s" % (backend_name, ", ".join(backend_reprs))
            ) from e_user
        else:
            # If there's some other error, this must be an error in Django
            raise


get_backend = functools.partial(
    load_backend, settings.NLP.get("BACKEND", DEFAULT_BACKEND))
