import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()

setup(
    name="pytest-freeze-reqs",
    version="0.2.0",
    packages=["freeze_reqs"],
    description="Check if requirement files are frozen",
    long_description=README,
    long_description_content_type="text/markdown",
    author="drozdowsky",
    author_email="hdrozdow+github@pm.me",
    url="https://github.com/drozdowsky/pytest-freeze-reqs/",
    license="MIT",
    install_requires=["pytest>=5.4", "requirements-parser"],
    entry_points={"pytest11": ["freeze_reqs = freeze_reqs.pytest_freeze_reqs"]},
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Pytest",
    ],
)
