from setuptools import setup, find_packages
setup(
    name = "overkill-bar",
    version = "0.1",
    install_requires=["overkill", "overkill-extra-writers"],
    packages = find_packages(),
    author = "Steven Allen",
    author_email = "steven@stebalien.com",
    description = "Bar widgets for overkill",
    namespace_packages = ["overkill", "overkill.extra"],
    license = "GPL3",
    url = "http://stebalien.com"
)
