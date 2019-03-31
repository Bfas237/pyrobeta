# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import shutil
from sys import argv

from setuptools import setup, find_packages, Command

from compiler.api import compiler as api_compiler
from compiler.docs import compiler as docs_compiler
from compiler.error import compiler as error_compiler


def read(file: str) -> list:
    with open(file, encoding="utf-8") as r:
        return [i.strip() for i in r]


def get_version():
    with open("pyrogram/__init__.py", encoding="utf-8") as f:
        return re.findall(r"__version__ = \"(.+)\"", f.read())[0]


def get_readme():
    # PyPI doesn't like raw html
    with open("README.rst", encoding="utf-8") as f:
        readme = re.sub(r"\.\. \|.+\| raw:: html(?:\s{4}.+)+\n\n", "", f.read())
        return re.sub(r"\|header\|", "|logo|\n\n|description|\n\n|schema| |tgcrypto|", readme)


class Clean(Command):
    DIST = ["./build", "./dist", "./Pyrogram.egg-info"]
    API = ["pyrogram/api/errors/exceptions", "pyrogram/api/functions", "pyrogram/api/types", "pyrogram/api/all.py"]
    DOCS = ["docs/source/functions", "docs/source/types", "docs/build"]
    ALL = DIST + API + DOCS

    description = "Clean generated files"

    user_options = [
        ("dist", None, "Clean distribution files"),
        ("api", None, "Clean generated API files"),
        ("docs", None, "Clean generated docs files"),
        ("all", None, "Clean all generated files"),
    ]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)

        self.dist = None
        self.api = None
        self.docs = None
        self.all = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        paths = set()

        if self.dist:
            paths.update(Clean.DIST)

        if self.api:
            paths.update(Clean.API)

        if self.docs:
            paths.update(Clean.DOCS)

        if self.all or not paths:
            paths.update(Clean.ALL)

        for path in sorted(list(paths)):
            try:
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            except OSError:
                print("skipping {}".format(path))
            else:
                print("removing {}".format(path))


class Generate(Command):
    description = "Generate Pyrogram files"

    user_options = [
        ("api", None, "Generate API files"),
        ("docs", None, "Generate docs files")
    ]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)

        self.api = None
        self.docs = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if self.api:
            error_compiler.start()
            api_compiler.start()

        if self.docs:
            docs_compiler.start()


if len(argv) > 1 and argv[1] in ["bdist_wheel", "install", "develop"]:
    error_compiler.start()
    api_compiler.start()
    docs_compiler.start()

setup(
    name="Pyrogram",
    version=get_version(),
    description="Telegram MTProto API Client Library for Python",
    long_description=get_readme(),
    url="https://github.com/pyrogram",
    download_url="https://github.com/pyrogram/pyrogram/releases/latest",
    author="Dan Tès",
    author_email="admin@pyrogram.ml",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    keywords="telegram chat messenger mtproto api client library python",
    project_urls={
        "Tracker": "https://github.com/pyrogram/pyrogram/issues",
        "Community": "https://t.me/PyrogramChat",
        "Source": "https://github.com/pyrogram/pyrogram",
        "Documentation": "https://docs.pyrogram.ml",
    },
    python_requires="~=3.4",
    packages=find_packages(exclude=["compiler*"]),
    zip_safe=False,
    install_requires=read("requirements.txt"),
    extras_require={
        "tgcrypto": ["tgcrypto==1.1.1"],  # TODO: Remove soon
        "fast": ["tgcrypto==1.1.1"],
    },
    cmdclass={
        "clean": Clean,
        "generate": Generate
    }
)
