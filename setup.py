"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject


python setup.py publish to publish

"""

# Always prefer setuptools over distutils
from setuptools import setup
import setuptools
from setuptools import find_packages

# from setuptools import find_packages

import os
import sys
import glob

here = os.path.abspath(os.path.dirname(__file__))


if sys.argv[-1] == "publish":  # requests
    os.system("python setup.py sdist")  # bdist_wheel
    os.system("twine upload dist/* --skip-existing")
    sys.exit()

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="shopcube",  # Required
    version="4.1.0",  # Required
    description="E-commerce solution",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/shopyo/shopcube",  # Optional
    author="Abdur-Rahmaan Janhangeer & contributors",  # Optional
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="flask pos management shop ecommerce cms erp",  # Optional
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
    python_requires=">=3.4",
    include_package_data=True,
    install_requires=open(os.path.join(here, "reqs", "app.txt"), encoding="utf-8")
    .read()
    .split("\n"),  # Optional
    extras_require={
        'dev': open(os.path.join(here, "reqs", "dev.txt"), encoding="utf-8")
            .read()
            .split("\n"),
    },
    project_urls={  # Optional
        "Bug Reports": "https://github.com/shopyo/shopcube/issues",
        "Source": "https://github.com/shopyo/shopcube/",
    },
    packages=find_packages(),
    entry_points={"console_scripts": ["shopcube=shopcube.__main__:main"]},
)
