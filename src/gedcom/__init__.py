"""
This is the __init__.py file for the gedcom package.
"""

import datetime
import enum

# Import necessary modules or packages here
from .fact import GedcomTag, TagValue, Fact
from .family import Family
from .person import Person, Sex
from .tree import FamilyTree

# from .module_name import ClassName, function_name

__version__ = "0.1.0"
__author__ = "Nicholas Wade"
