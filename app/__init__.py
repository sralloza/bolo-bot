from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
from .main import create_app
from .utils import setup_logging

setup_logging()
app = create_app()
