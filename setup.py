from setuptools import setup, find_packages

setup(
    version="1.0",
    name="brname",
    packages=find_packages(),
    py_modules=["brname"],
    author="Bohui WU",
    install_requires=[],
    description="Rename multiple files according to user-defined criteria in command line",
    entry_points={
        'console_scripts': ['brname=brname.cli:main'],
    },
    include_package_data=True,
)
