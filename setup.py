"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
"""

from codecs import open
from os import path
from setuptools import setup


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
    # .tox\py36\Lib\site-packages\monotable-0.1.0.dist-info\DESCRIPTION.rst
    # was truncated to 4 lines with the last 3 whitespace.
    # Observed problem when invoking tox (2.5.0) from Python 2.7.13 on win32.
    # The file README.rst has DOS\Windows line endings.
    # These line endings were still in the the string long_description.
    # Not sure why.
    # Suspect a version of BIF open() that did not support universal newline
    # was being called.
    lines = text.splitlines()
    return '\n'.join(lines)


def make_long_description():
    """Read and process file README.rst to create the long description.

    To preview the long-description locally requires
    pip install sphinx
    which installs sphinx including the script rst2html.py.
    Then run a shell command something like this:
    python setup.py --long-description |
        C:\Python27\Scripts\rst2html.py - readme.html
    """
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        text = f.read()
        text = replace_doctest_directives(text)
        return replace_line_endings(text)


# Uncomment the import line above, the setup_requirements line below,
# and the two commented out args to setup() (setup_requires, tests_require)
# to add support for python setup.py test.
# per similar advice from https://pypi.org/project/pytest-runner/.

setup(
    name='monotable',
    version='1.0.1',
    description=('ASCII table with per column format specs, '
                 'multi-line content, plug-in format functions, '
                 'column width control.'),
    long_description=make_long_description(),
    url='https://github.com/tmarktaylor/monotable',
    author='Mark Taylor',
    author_email='mark66547ta2' '@' 'gmail' '.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    packages=['monotable'],
    keywords='ascii table pretty',

    # setup_requires= Note to Contributors: Please do not add any install
    # time dependencies.  Please use extras_requires instead.

    # Advice from https://github.com/pypa/sampleproject/blob/master/setup.py
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[test,docs]
    extras_require={'test': ['tox', 'pytest'],
                    'docs': ['sphinx', 'sphinx_rtd_theme']
                    },
)
