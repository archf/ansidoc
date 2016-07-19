from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

PACKAGE_NAME = 'ansidoc'
REPOSITORY_VERSION_FILE = 'VERSION'
LONG_DESCRIPTION_FILE = 'README.md'
PACKAGE_VERSION_FILE_HEADER = """\
# Do no edit, this file is generated from setuptools setup.py script.
# Edit the 'VERSION' file in the root of this repository instead.

"""


def get_long_description(file):
    """Get the long description from the README file."""
    with open(file, encoding='utf-8') as f:
        return f.read()


def get_version(file):
    """Get current release version from repository version file."""
    with open(file) as f:
        return f.readline().strip()


def update_software_version(package, header, version):
    """Generate __version__.py inside a given package."""
    with open(path.join(package, '__version__.py'), 'w') as f:
        f.write(header + "__version__ = " + "'" + version + "'")


VERSION = get_version(REPOSITORY_VERSION_FILE)
update_software_version(PACKAGE_NAME, PACKAGE_VERSION_FILE_HEADER, VERSION)


setup(
    name=PACKAGE_NAME,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=VERSION,

    description='Manage ansible role documentation and more',
    long_description=get_long_description(LONG_DESCRIPTION_FILE),

    # The project's main homepage.
    url='https://github.com/pypa/sampleproject',

    # Author details
    author='Felix Archambault',
    author_email='fel.archambault@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='ansible documentation generation',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'env']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['jinja2', 'PyYaml'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.

    package_data={
        PACKAGE_NAME: ['templates/*'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa

    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # sys.prefix == /<env>/ when using a virtual environment
    # sys.prefix = /usr on global python3.5*
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'ansidoc=ansidoc.__main__:main',
        ],
    },
)
