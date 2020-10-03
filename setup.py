import os

from setuptools import Command, find_packages, setup


def clean_requirements_list(input_list):
    reqs = [v.split("#")[0].strip() for v in input_list]
    return [v for v in reqs if len(v) > 0 and not v.startswith("-")]


class Cleaner(Command):
    def run(self):
        os.system("rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info")


with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requirements = f.readlines()

requirements = clean_requirements_list(requirements)

setup(
    name="twitter_sna",
    version="0.0.1",
    description="twitter social network analysis",
    long_description=readme,
    author="joshuAnalytics",
    author_email="",
    url="https://github.com/joshuAnalytics",
    packages=find_packages(include=["twitter_sna"], exclude=["docs", "test", "examples"]),
    python_requires=">=3.7",
    install_requires=requirements,
    classifiers=[
        "Intended Audience :: Developers/Researchers",
        "Language :: English",
        "Programming Language :: Python :: 3",
    ],
)
