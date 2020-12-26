from setuptools import setup

import versioneer

setup(
    name="gale-telegram-bot",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
