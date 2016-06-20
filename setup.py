from setuptools import find_packages, setup


__version__ = "0.1.0"


setup(
    name="kisqpy",
    version=__version__,
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    kisctl = kisqpy.createdb:main
    """
)
