from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='color-contrast-calc',
    version='0.1.0',
    description='Utility that helps you choose colors with sufficient contrast, WCAG 2.0 in mind',
    long_description=long_description,
    url='https://github.com/nico-hn/color_contrast_calc_py',
    author='HASHIMOTO, Naoki',
    author_email='hashimoto.naoki@gmail.com',
    license='MIT',
    classifier=[
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='~=3.2',
    install_requires=[
        'numpy>=1.3',
    ],
    extras_requires={
        'dev': ['pytest'],
        'test': ['pylint']
    },
    packages=find_packages(exclude=['tests', 'docs', 'examples']),
    package_data={
        'color_contrast_calc': ['color_keywords.json'],
    }
)
