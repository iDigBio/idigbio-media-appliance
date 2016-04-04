import os

from setuptools import setup, find_packages

from codecs import open
import json


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r', 'utf-8') as f:
        return f.read()

with open("package.json", "r", encoding="utf-8") as jsonf:
    package_json = json.load(jsonf)

setup(
    name=package_json["name"],
    version=package_json["version"],
    description=package_json["description"],
    long_description=read('README.rst') + "\n\n",
    url=package_json["repository"],
    license='MIT',
    author=package_json["author"].split(" ")[0],
    author_email=package_json["author"].split(" ")[1][1:-1],
    packages=find_packages(exclude=['tests*']),
    entry_points={
        "console_scripts": [
            "idigbio_media_appliance=idigbio_media_appliance.__main__:main"
        ],
    },
    install_requires=[
        'Flask',
        'Flask-RESTful',
        'Flask-SQLAlchemy',
        'alembic',
        'gevent',
        'easygui',
        'appdirs  ',
        'unicodecsv',
        'idigbio'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
)
