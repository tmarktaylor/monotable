"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
"""

from codecs import open
from os import path
from setuptools import setup


def make_badge_text():
    """Generate reStructuredText for license and python.org badges."""
    badge_directives = [
        ".. |apache| image:: https://img.shields.io/pypi/l/monotable.svg",
        "   :target: http://www.apache.org/licenses/LICENSE-2.0",
        "   :alt: License: Apache 2.0",
        "",
        ".. |py_versions| image::",
        "    https://img.shields.io/pypi/pyversions/monotable.svg",
        "    :target: https://pypi.python.org/pypi/monotable",
        "    :alt: Python versions supported",
        "",
        ".. |build_status| image::",
        "    https://travis-ci.org/tmarktaylor/monotable.svg?branch=master",
        "    :target: https://travis-ci.org/tmarktaylor/monotable",
        "    :alt: Build Status",
        "",
        "",
        ".. |coverage| image::",
        "    https://codecov.io/gh/tmarktaylor/monotable/"
        "coverage.svg?branch=master",
        "    :target: https://codecov.io/gh/tmarktaylor/"
        "monotable?branch=master",
        "    :alt: Code Coverage",
        "",
        "|apache| |py_versions| |build_status| |coverage|",
        "",
        ]
    return '\n'.join(badge_directives)


def replace_doctest_directives(text):
    """Replace some sphinx.doctest directives with reST compatible ones.

    Does not replace testsetup, testcleanup.
    """
    text = text.replace('.. testcode::', '.. code:: python')
    text = text.replace('.. testoutput::', '.. code::')
    return text


def replace_line_endings(text):
    """Replace line endings in string text with Python '\n'."""
    # This code fixes a problem where the local file
    # .tox\installonly\Lib\site-packages\monotable-0.1.0.dist-info\
    # DESCRIPTION.rst
    # was truncated to 4 lines with the last 3 whitespace.
    # Observed problem when invoking tox (2.5.0) from Python 2.7.13 on windows.
    # The file DESCRIPTION.rst has Unix-LF line endings.
    # The file README.rst has DOS\Windows line endings.
    # These line endings were still in the the string long_description.
    # Not sure why.
    lines = text.splitlines()
    return '\n'.join(lines)


def make_long_description():
    """Read and process file README.rst to create the long description.

    README.rst is used for both the PYPI long description and the
    Sphinx documentation.  This was done to achieve both:
        1. Sphinx doctest tests the examples in README.rst.
        2. Syntax coloring of the examples in README.rst.

    To preview the long-description locally requires
        pip install sphinx
    which installs sphinx including the script rst2html5.py
    Then run a shell command something like this:
    python readme_preview.py <path to>Scripts/rst2html5.py readme.html
    """
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        text = f.read()
        # prepend badge directives
        # This is done to keep the badge directives out of the Sphinx docs.
        text = '\n'.join([make_badge_text(), text])
        text = replace_doctest_directives(text)
        return replace_line_endings(text)


# Uncomment the import line above, the setup_requirements line below,
# and the two commented out args to setup() (setup_requires, tests_require)
# to add support for python setup.py test.
# per similar advice from https://pypi.org/project/pytest-runner/.

setup(
    name='monotable',
    version='3.1.0',
    description=('ASCII table with per column format specs, '
                 'multi-line content, formatting directives, '
                 'column width control.'),
    long_description=make_long_description(),
    long_description_content_type='text/x-rst',
    url='https://github.com/tmarktaylor/monotable',
    author='Mark Taylor',
    author_email='mark66547ta2' '@' 'gmail' '.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    python_requires='>=3.5',
    package_data={"monotable": ["py.typed"]},
    zip_safe=False,    # per mypy 26.2  Making PEP 561 compatible packages
    packages=['monotable'],
    keywords='ascii table pretty',

    # setup_requires= Note to Contributors: Please do not add any install
    # time dependencies.  Please use extras_requires instead.

    # Advice from https://github.com/pypa/sampleproject/blob/master/setup.py
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[test,docs]

    # These dependencies mirror those in tox.ini.
    extras_require={'cover': ['coverage', 'pytest', 'codecov'],
                    'inspect': [
                        'flake8', 'pep8-naming', 'mypy', 'typing',
                        'check-manifest', 'twine'
                    ],
                    'docs': ['sphinx<=1.8.5', 'sphinx_rtd_theme<=0.5'],
                    },
)
