from setuptools import setup, find_packages

setup(
    name='color-contrast-calc',
    version='0.0.1',
    description='Utility that supports you in choosing colors with sufficient contrast, WCAG 2.0 in mind',
    url='https://github.com/nico-hn/color_contrast_calc_py',
    author='HASHIMOTO, Naoki',
    author_email='hashimoto.naoki@gmail.com',
    license='MIT',
    install_requires=[
        'numpy'
    ],
    packages=find_packages(exclude=['tests*']),
    package_data={
        'color_contrast_calc': ['color_keywords.json'],
    }
)
