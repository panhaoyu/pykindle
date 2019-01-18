#!/usr/bin/env python
import configparser
from setuptools import find_packages, setup

config = configparser.ConfigParser()
with open('config.ini', mode='r', encoding='utf-8') as file:
    config.read_file(file)


def get_version():
    subconfig = config['version']
    subconfig['third'] = str(int(subconfig['third']) + 1)
    version = [subconfig['first'], subconfig['second'], subconfig['third']]
    version = '.'.join(version)
    with open('config.ini', mode='w', encoding='utf-8') as file:
        config.write(file)
    return version


def get_readme():
    with open('README.md', mode='r', encoding='utf-8') as file:
        return file.read()


setup(
    name='pykindle',
    version=get_version(),
    author='Haoyu Pan',
    description="PyKindle: Generate mobi files in a programming way",
    long_description=get_readme(),
    author_email='haoyupan@aliyun.com',
    install_requires=['jinja2', 'markdown'],
    url="https://github.com/panhaoyu/pykindle",
    packages=find_packages(),
    include_package_data=True,
    license='GPL',
    classifiers=[
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Documentation': 'https://github.com/panhaoyu/pykindle',
        'Source': 'https://github.com/panhaoyu/pykindle',
    },
)
