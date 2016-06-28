from setuptools import find_packages, setup


__version__ = "0.1.0"


setup(
    name="kisqpy",
    version=__version__,
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    kisctl = kisqpy.client.shell.__main__:main
    [gui_scripts]
    kisclient = kisqpy.client.gui.__main__:main
    """
)
