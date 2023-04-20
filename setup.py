from os import path
from io import open
from setuptools import setup, find_namespace_packages


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="mic_serv_uf_chile",  # Required
    version="1.0.0",  # Required
    description="Micro service",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    author="Leonardo Gonzalez",  # Optional
    author_email="gonzalezrujano@gmail.com",  # Optional
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords="sample setuptools development",  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_namespace_packages(),  # Required
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. If you
    # do not support Python 2, you can simplify this to '>=3.5' or similar, see
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=2.7",
    install_requires=['aniso8601==9.0.1', "astroid==2.13.5; python_full_version >= '3.7.2'", 'asttokens==2.2.1', "async-timeout==4.0.2; python_version <= '3.11.2'", "attrs==23.1.0; python_version >= '3.7'", "certifi==2022.12.7; python_version >= '3.6'", "charset-normalizer==3.1.0; python_full_version >= '3.7.0'", 'click==8.1.3', "colorama==0.4.6; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6'", 'dependency-injector[yaml]==4.39.1', "dill==0.3.6; python_version >= '3.7'", "exceptiongroup==1.1.1; python_version >= '3.7'", 'executing==1.2.0', 'flask==2.1.2', 'flask-restx==1.0.3', "future==0.18.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2'", 'icecream==2.1.3', "idna==3.4; python_version >= '3.5'", "importlib-metadata==6.5.0; python_version >= '3.7'", "iniconfig==2.0.0; python_version >= '3.7'", "isort==5.12.0; python_full_version >= '3.8.0'", "itsdangerous==2.1.2; python_version >= '3.7'", "jinja2==3.1.2; python_version >= '3.7'", "jsonschema==4.17.3; python_version >= '3.7'", "lazy-object-proxy==1.9.0; python_version >= '3.7'", "markupsafe==2.1.2; python_version >= '3.7'", "mccabe==0.7.0; python_version >= '3.6'", "packaging==23.1; python_version >= '3.7'", "platformdirs==3.2.0; python_version >= '3.7'", "pluggy==1.0.0; python_version >= '3.6'", 'pycodestyle==2.9.1', 'pydantic==1.10.2', 'pydocstyle==6.1.1', "pygments==2.15.1; python_version >= '3.7'", 'pylint==2.15.5', 'pymongo==4.2.0', "pyrsistent==0.19.3; python_version >= '3.7'", 'pytest==7.3.1', 'pytz==2023.3', "pyyaml==6.0; python_version >= '3.6'", 'redis==4.5.4', 'requests==2.28.2', "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'", 'snowballstemmer==2.2.0', 'textfsm==1.1.3', "tomli==2.0.1; python_version >= '3.7'", "tomlkit==0.11.7; python_version >= '3.7'", 'typing==3.7.4.3', "typing-extensions==4.5.0; python_version >= '3.7'", "urllib3==1.26.15; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'", 'vistir==0.6.1', 'werkzeug==2.1.2', "wrapt==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", "zipp==3.15.0; python_version >= '3.7'"],  # Optional
    extras_require={"dev": ["icecream==2.1.1", "pipenv-setup==3.1.1"]},  # Optional
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # Sometimes you’ll want to use packages that are properly arranged with
    # setuptools, but are not published to PyPI. In those cases, you can specify
    # a list of one or more dependency_links URLs where the package can
    # be downloaded, along with some additional hints, and setuptools
    # will find and install the package correctly.
    # see https://python-packaging.readthedocs.io/en/latest/dependencies.html#packages-not-on-pypi
    #
    dependency_links=[],
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    # package_data={"sample": ["package_data.dat"]},  # Optional
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[("my_data", ["data/data_file"])],  # Optional
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={"console_scripts": ["sample=sample:main"]},  # Optional
    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        "Bug Reports": "https://github.com/pypa/sampleproject/issues",
        "Funding": "https://donate.pypi.org",
        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/pypa/sampleproject/",
    },
    entry_points={"console_scripts": ["mic_serv_uf_chile=mic_serv_uf_chile:cli"]},
)