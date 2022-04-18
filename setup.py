"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
"""

# See setup.cfg.
# Note:
# Entry points done here since setuptools minimum version
# for this section in setup.cfg is 51.0.0 per
# https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html
# Always prefer setuptools over distutils
from setuptools import setup

setup(
    package_data={"monotable": ["py.typed"]},
    zip_safe=False,  # per mypy 26.2  Making PEP 561 compatible packages
    packages=['monotable'],
)
