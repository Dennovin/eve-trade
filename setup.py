import os
from setuptools import setup, find_packages

setup(
    name="eve-trade",
    description="EVE Online market trade monitoring tools",
    url="https://github.com/Dennovin/eve-trade",
    version="0.01",
    author="Corey Cossentino",
    author_email="corey@cossentino.com",
    license="MIT",
    packages=find_packages(),
    package_data={
        "evetrade": ["static/*", "templates/*", "db/*"],
        },
    install_requires=[
        "tornado >= 4.0.2",
        ],
    scripts=[
        "scripts/eve_trade_web.py",
        "scripts/update_transactions.py",
        ],
    )
