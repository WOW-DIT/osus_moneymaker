from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in moneymaker/__init__.py
from moneymaker import __version__ as version

setup(
	name="moneymaker",
	version=version,
	description="moneymaker",
	author="omar",
	author_email="info@wowit.sa",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
