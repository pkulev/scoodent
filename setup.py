from setuptools import find_packages, setup


__version__ = "0.1.0"


setup(
    name="scoodent",
    version=__version__,
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    scooctl = scoodent.client.shell.__main__:main
    [gui_scripts]
    scooclient = scoodent.client.__main__:main
    """
)
