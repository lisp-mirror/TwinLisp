"""
Copyright (C) 2006 Mikalai Birukou

This file is part of TwinLisp.

    TwinLisp is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    TwinLisp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with TwinLisp; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""


import unittest
from TestStringReading import TestMarkElemsInStr, TestGrowingList
from TestElemSearchFuncs import TestElemSearchFuncs
from TestFormBuilding import TestFormBuilding
from TestFormBuildingTwo import TestFormBuildingTwo
from TestFormBuildingThree import TestFormBuildingThree
from TestFormWritting import TestFormWritting

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMarkElemsInStr))
suite.addTest(unittest.makeSuite(TestGrowingList))
suite.addTest(unittest.makeSuite(TestElemSearchFuncs))
suite.addTest(unittest.makeSuite(TestFormBuilding))
suite.addTest(unittest.makeSuite(TestFormBuildingTwo))
suite.addTest(unittest.makeSuite(TestFormBuildingThree))
suite.addTest(unittest.makeSuite(TestFormWritting))
unittest.TextTestRunner(verbosity=1).run(suite)
