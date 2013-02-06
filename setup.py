#    SyPy: A Python framework for evaluating graph-based Sybil detection
#    algorithms in social and information networks.
#
#    Copyright (C) 2013  Yazan Boshmaf
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(
    name="sypy",
    version="0.1.0",
    author="Yazan Boshmaf",
    author_email="boshmaf@ece.ubc.ca",
    packages=["sypy", "sypy.tests"],
    url="http://boshmaf.github.com/sypy",
    license='LICENSE.txt',
    description="Graph-based Sybil detection.",
    long_description=open('README.md').read(),
    install_requires=[
        "scipy >= 0.10.1",
        "networkx >= 1.7",
        "numpy >= 1.6.2"
    ],
)
