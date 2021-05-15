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

import unittest, StringIO
from StringReading import GrowingList
from ElemSearchFuncs import getElemsInBrackets, skipElems, getRequiredElemInd


class TestElemSearchFuncs(unittest.TestCase):

    def testGetElemsInBrackets1(self):
        st = "(a)"
        gL = GrowingList(StringIO.StringIO(st))
        elems, end = getElemsInBrackets(0,gL)
        self.assertEqual(len(elems),1)
        self.assertEqual(end,2)
        self.assertEqual(elems[0].value,"a")
        elems, end = getElemsInBrackets(0,gL,True)
        self.assertEqual(len(elems),3)
        self.assertEqual(end,3)
        self.assertEqual(elems[0].type,"(")
        self.assertEqual(elems[1].value,"a")
        self.assertEqual(elems[2].type,")")

    def testGetElemsInBrackets2(self):
        st = """~((a)+b[{(s)}])"""
        gL = GrowingList(StringIO.StringIO(st))
        elems, end = getElemsInBrackets(0,gL)
        self.assertEqual(len(elems),12)
        self.assertEqual(end,13)
        self.assertEqual(elems[8].value,"s")
        elems, end = getElemsInBrackets(0,gL,True)
        self.assertEqual(len(elems),14)
        self.assertEqual(end,14)
        self.assertEqual(elems[0].type,"~(")
        self.assertEqual(elems[9].value,"s")
        self.assertEqual(elems[13].type,")")

    def testGetElemsInBrackets3(self):
        st = """~((a),
                    b[{(s)}])"""
        gL = GrowingList(StringIO.StringIO(st))
        elems, end = getElemsInBrackets(0,gL)
        self.assertEqual(len(elems),14)
        self.assertEqual(end,15)
        self.assertEqual(elems[4].type,elems[4].LINE_END_TYPE)

    def testGetElemsInBrackets4(self):
        st = """~((a,
                    b[{(s)}])"""
        gL = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getElemsInBrackets,0,gL)
        st = """~((a),
                    b[(s)}])"""
        gL = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getElemsInBrackets,0,gL)

    def testSkipElems(self):
        st = """def foo () 
                        { a , b \\ t g * ;comment
                          c}"""
        gL = GrowingList(StringIO.StringIO(st))
        elemFound, ind = skipElems([gL[0].WHITE_TYPE],1,gL)
        self.assert_(elemFound)
        self.assertEqual(gL[ind].value,"foo")
        elemFound, ind = skipElems([gL[0].WHITE_TYPE],3,gL)
        self.assert_(elemFound)
        self.assertEqual(gL[ind].type,"(")
        elemFound, ind = skipElems([gL[0].WHITE_TYPE],6,gL)
        self.assert_(not elemFound)
        elemFound, ind = skipElems([gL[0].WHITE_TYPE],6,gL,False)
        self.assert_(elemFound)
        self.assertEqual(gL[ind].type,"{")
        self.assertEqual(skipElems([gL[0].WHITE_TYPE],ind,gL)[1],ind)
        elemFound, ind = skipElems([gL[0].WHITE_TYPE,","],ind+3,gL)
        self.assert_(elemFound)
        self.assertEqual(gL[ind].value,"b")
        elemFound, ind = skipElems([gL[0].WHITE_TYPE],ind+1,gL)
        self.assert_(elemFound)
        self.assertEqual(gL[ind].value,"c")

    def testGetRequiredElemInd(self):
        st = """def foo \\
                        ()
                        {}"""
        gL = GrowingList(StringIO.StringIO(st))
        ind = getRequiredElemInd(gL[0].SYMB_TYPE,1,gL)
        self.assertEqual(gL[ind].value,"foo")
        ind = getRequiredElemInd("(",3,gL)
        self.assertEqual(gL[ind].type,"(")
        self.assertRaises(SyntaxError,getRequiredElemInd,"{",ind+2,gL)
        ind = getRequiredElemInd("{",ind+2,gL,False)
        self.assertEqual(gL[ind].type,"{")



if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestElemSearchFuncs))
    unittest.TextTestRunner(verbosity=1).run(suite)

