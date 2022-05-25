from distutils.core import setup
from setuptools import find_packages


setup(
    name='Infermary',
    version='1.0.0',
    description='Library for type inference and casting of tabular data.',
    author='Klearly',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'decorator'
    ],
    test_suite='pytest',
    tests_require=[
        'pytest==3.5.0',
        'pylint==1.8.4'
    ]
)
