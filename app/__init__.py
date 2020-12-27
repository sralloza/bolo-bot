from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
from .core.utils import setup_logging
from .main import create_app

setup_logging()
app = create_app()
