"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
import os
import sys
from shopyo import __version__  # thanks gunicorn

here = path.abspath(path.dirname(__file__))

if sys.argv[-1] == "publish":  # requests
    os.system("python setup.py sdist")  # bdist_wheel
    os.system("twine upload dist/* --skip-existing")
    sys.exit()

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="shopyo",  # Required
    version=__version__,  # Required
    description="Flask base & POS software",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/Abdur-RahmaanJ/shopyo",  # Optional
    author="Abdur-Rahmaan Janhangeer",  # Optional
    author_email="arj.python@gmail.com",  # Optional
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # 'Topic :: Weather',
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="flask pos management shop",  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    packages=["shopyo"],
    include_package_data=True,
    python_requires=">=3.4",
    install_requires=open(path.join(here, "requirements.txt"), encoding="utf-8")
    .read()
    .split("\n"),  # Optional
    project_urls={  # Optional
        "Bug Reports": "https://github.com/Abdur-RahmaanJ/shopyo/issues",
        "Source": "https://github.com/Abdur-RahmaanJ/shopyo/",
    },
    entry_points={"console_scripts": ["shopyo=shopyo.__main__:main"]},
)