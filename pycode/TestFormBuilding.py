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
from FormBuilding import getForms, LevelInfo
from Const import *


class TestFormBuilding(unittest.TestCase):

    def testGetFormsBracketForm1(self):
        st = """~()"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(),True)
        self.assertEqual(forms,[(COMMENT_TYPE,"; source line # 1"),(FORM_TYPE,[])])

    def testGetFormsBracketForm2(self):
        st = """~(),~()
                ~(),~(~(),~())"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(),True)
        self.assertEqual(forms,[(COMMENT_TYPE,"; source line # 1"),(FORM_TYPE,[]),
                                (COMMENT_TYPE,"; source line # 1"),(FORM_TYPE,[]),
                                (COMMENT_TYPE,"; source line # 2"),(FORM_TYPE,[]),
                                (COMMENT_TYPE,"; source line # 2"),
                                (FORM_TYPE,[(COMMENT_TYPE,"; source line # 2"),(FORM_TYPE,[]),
                                            (COMMENT_TYPE,"; source line # 2"),(FORM_TYPE,[])])])

    def testGetFormsBracketForm3(self):
        st = """  ~(),~(), \\ anything to new line will be skipped
                ~(),
                ~(~(),~())"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(),True)
        self.assertEqual(forms,[(COMMENT_TYPE,"; source line # 1"),(FORM_TYPE,[]),
                                (COMMENT_TYPE,"; source line # 1"),(FORM_TYPE,[]),
                                (COMMENT_TYPE,"; source line # 2"),(FORM_TYPE,[]),
                                (COMMENT_TYPE,"; source line # 3"),
                                (FORM_TYPE,[(COMMENT_TYPE,"; source line # 3"),(FORM_TYPE,[]),
                                            (COMMENT_TYPE,"; source line # 3"),(FORM_TYPE,[])])])

    def testGetFormsBracketForm4(self):
        st = """~() ; comment here
                ~()
                ~()"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,[(FORM_TYPE,[]),(COMMENT_TYPE,"; comment here"),
                                (FORM_TYPE,[]),(FORM_TYPE,[])])

    def testGetFormsBracketForm5(self):
        st = """~(a,b,c-d,~(foo))"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,[(FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"b"),
                                             (FORM_TYPE,[(ATOM_TYPE,"_-_"),
                                                         (ATOM_TYPE,"c"),(ATOM_TYPE,"d")]),
                                             (FORM_TYPE,[(ATOM_TYPE,"foo")])])])

    def testGetFormsOperForm1(self):
        st = """x"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,[(ATOM_TYPE,"x")])

    def testGetFormsOperForm2(self):
        st = """x,y"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,[(ATOM_TYPE,"x"),(ATOM_TYPE,"y")])

    def testGetFormsOperForm3(self):
        st = """x
                y"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,[(ATOM_TYPE,"x"),(ATOM_TYPE,"y")])

    def testGetFormsOperForm4(self):
        st = """x y"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsOperForm5(self):
        st = """x+y"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),(ATOM_TYPE,"y")])])

    def testGetFormsOperForm6(self):
        st = """x+y-z"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_-_"),
                         (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),(ATOM_TYPE,"y")]),
                         (ATOM_TYPE,"z"),])])

    def testGetFormsOperForm7(self):
        st = """x+y*d"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"_*_"),(ATOM_TYPE,"y"),(ATOM_TYPE,"d")])])])

    def testGetFormsOperForm8(self):
        st = """x+'y"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),(SHORTCUT_TYPE,"'",(ATOM_TYPE,"y"))])])

    def testGetFormsOperForm9(self):
        st = """x+'$y"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),
                         (SHORTCUT_TYPE,"'",(SHORTCUT_TYPE,",",(ATOM_TYPE,"y")))])])

    def testGetFormsOperForm10(self):
        st = """#'*"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,[(SHORTCUT_TYPE,"#'",(ATOM_TYPE,"_*_"))])

    def testGetFormsOperForm11(self):
        st = """a=x+y*d"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),
                                     (FORM_TYPE,[(ATOM_TYPE,"_*_"),(ATOM_TYPE,"y"),(ATOM_TYPE,"d")])])])])

    def testGetFormsOperForm12(self):
        st = """a=x*(y+d)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_*_"),(ATOM_TYPE,"x"),
                                     (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"y"),(ATOM_TYPE,"d")])])])])

    def testGetFormsOperForm13(self):
        st = """x+y*d/c-z"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_-_"),
                         (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),
                                     (FORM_TYPE,[(ATOM_TYPE,"_/_"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"_*_"),(ATOM_TYPE,"y"),(ATOM_TYPE,"d")]),
                                                 (ATOM_TYPE,"c")])]),
                          (ATOM_TYPE,"z")])])

    def testGetFormsOperForm14(self):
        st = """a=x+=y=z"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_+=_"),(ATOM_TYPE,"x"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"y"),(ATOM_TYPE,"z")])])])])

    def testGetFormsOperForm15(self):
        st = """a=x*(y+d,s)"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsOperForm16(self):
        st = """a=x*(y+d,)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_*_"),(ATOM_TYPE,"x"),
                                     (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"y"),(ATOM_TYPE,"d")])])])])

    def testGetFormsOperForm17(self):
        st = """a=x*(y+d
                     s)"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsOperForm18(self):
        st = """a=x+y \\
                  *d"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),
                                     (FORM_TYPE,[(ATOM_TYPE,"_*_"),(ATOM_TYPE,"y"),(ATOM_TYPE,"d")])])])])

    def testGetFormsOperForm19(self):
        st = """x+y**d**c-z"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_-_"),
                         (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),
                                     (FORM_TYPE,[(ATOM_TYPE,"_**_"),
                                                 (ATOM_TYPE,"y"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"_**_"),(ATOM_TYPE,"d"),(ATOM_TYPE,"c")])])]),
                          (ATOM_TYPE,"z")])])

    def testGetFormsOperForm20(self):
        st = """x+~(foo,a+b)-z"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_-_"),
                         (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"a"),(ATOM_TYPE,"b")])])]),
                         (ATOM_TYPE,"z"),])])

    def testGetFormsOperForm21(self):
        st = """x++y"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),(FORM_TYPE,[(ATOM_TYPE,"_unary+_"),(ATOM_TYPE,"y")])])])

    def testGetFormsOperForm22(self):
        st = """x+-y"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),(FORM_TYPE,[(ATOM_TYPE,"_unary-_"),(ATOM_TYPE,"y")])])])

    def testGetFormsOperForm23(self):
        st = """a@b@c=x@y@z"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),
                         (FORM_TYPE,[(ATOM_TYPE,"values"),(ATOM_TYPE,"a"),
                                     (ATOM_TYPE,"b"),(ATOM_TYPE,"c")]),
                         (FORM_TYPE,[(ATOM_TYPE,"values"),(ATOM_TYPE,"x"),
                                     (ATOM_TYPE,"y"),(ATOM_TYPE,"z")])])])

    def testGetFormsOperForm24(self):
        st = """x+"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsOperForm25(self):
        st = """x+'"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsOperForm26(self):
        st = """+"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsOperForm27(self):
        st = """*"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsOperForm28(self):
        st = """not x and y or z"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_or_"),
                         (FORM_TYPE,[(ATOM_TYPE,"_and_"),(FORM_TYPE,[(ATOM_TYPE,"_not_"),(ATOM_TYPE,"x")]),
                                     (ATOM_TYPE,"y")]),
                         (ATOM_TYPE,"z")])])

    def testGetFormsOperForm29(self):
        st = """!x & y | z"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_or_"),
                         (FORM_TYPE,[(ATOM_TYPE,"_and_"),(FORM_TYPE,[(ATOM_TYPE,"_not_"),(ATOM_TYPE,"x")]),
                                     (ATOM_TYPE,"y")]),
                         (ATOM_TYPE,"z")])])

    def testGetFormsComplexNum1(self):
        st = """x=#c(s-d,23/45)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"complex"),
                                     (FORM_TYPE,[(ATOM_TYPE,"_-_"),(ATOM_TYPE,"s"),(ATOM_TYPE,"d")]),
                                     (ATOM_TYPE,"23/45")])])])

    def testGetFormsComplexNum2(self):
        st = """x=#c(3.4e-10,23/45)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"complex"),(ATOM_TYPE,"3.4e-10"),
                                     (ATOM_TYPE,"23/45")])])])

    def testGetFormsComplexNum3(self):
        st = """x=#c(3.4e-10)"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsArray1(self):
        st = """x=[s-d,23/45,foo]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-vector_"),
                                     (ATOM_TYPE,":initContent"),
                                     (FORM_TYPE,[(ATOM_TYPE,"list"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"_-_"),(ATOM_TYPE,"s"),
                                                             (ATOM_TYPE,"d")]),
                                                 (ATOM_TYPE,"23/45"),
                                                 (ATOM_TYPE,"foo")])])])])

    def testGetFormsArray2(self):
        st = """x=[]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-vector_")])])])

    def testGetFormsList1(self):
        st = """x=~[s-d,23/45,foo]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"list"),
                                     (FORM_TYPE,[(ATOM_TYPE,"_-_"),(ATOM_TYPE,"s"),
                                                 (ATOM_TYPE,"d")]),
                                     (ATOM_TYPE,"23/45"),
                                     (ATOM_TYPE,"foo")])])])

    def testGetFormsList2(self):
        st = """x=~[]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"list")])])])

    def testGetFormsBodyBlock1(self):
        st = """x=foo{a,b}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"a"),(ATOM_TYPE,"b")])])])

    def testGetFormsBodyBlock2(self):
        st = """x=foo{a
                      b=45}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"a"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"b"),(ATOM_TYPE,"45")])])])])

    def testGetFormsBodyBlock3(self):
        st = """x=foo{}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo")])])])

    def testGetFormsBodyBlock4(self):
        st = """x=foo{a
                      b=45}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(),True)
        self.assertEqual(forms,
            [(COMMENT_TYPE,"; source line # 1"),
             (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),
                                     (COMMENT_TYPE,"; source line # 1"),(ATOM_TYPE,"a"),
                                     (COMMENT_TYPE,"; source line # 2"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"b"),(ATOM_TYPE,"45")])])])])

    def testGetFormsBodyBlock5(self):
        st = """x=foo{}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(),True)
        self.assertEqual(forms,
            [(COMMENT_TYPE,"; source line # 1"),
             (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo")])])])

    def testGetFormsString1(self):
        st = """ "Hello, World!" """
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,[(ATOM_TYPE,"\"Hello, World!\"")])

    def testGetFormsString2(self):
        st = """x="Hello, "+"World!" """
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"\"Hello, \""),
                                     (ATOM_TYPE,"\"World!\"")])])])

    def testGetFormsString3(self):
        st = """x="Hello,
the"+" brave,
  new
   World!" """
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"""\"Hello,
the\""""),(ATOM_TYPE,"""\" brave,
  new
   World!\"""")])])])

    def testGetFormsCLisp1(self):
        st = """x=cl{{(- 1 2)}}-3\n"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"_-_"),(ATOM_TYPE,"(- 1 2)\n"),
                                     (ATOM_TYPE,"3")])])])

    def testGetFormsCLisp2(self):
        st = """cl{{(foo) ; comment
        (boo)}}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,[(ATOM_TYPE,"""(foo) ; comment
        (boo)""")])

    def testGetFormsColumn1(self):
        st = """x=:a"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (ATOM_TYPE,":a")])])

    def testGetFormsColumn2(self):
        st = """x=::a"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (ATOM_TYPE,"::a")])])

    def testGetFormsColumn3(self):
        st = """x= foo : a"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (ATOM_TYPE,"foo:a")])])

    def testGetFormsColumn4(self):
        st = """:x=a"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,":x"),
                         (ATOM_TYPE,"a")])])

    def testGetFormsColumn5(self):
        st = """x=foo{}:a"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsColumn6(self):
        st = """x=('foo):a"""   # have expr 'foo and expr :a - two expr together is illegal
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsColumn7(self):
        st = """x='foo:a"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (SHORTCUT_TYPE,"'",(ATOM_TYPE,"foo:a"))])])

    def testGetFormsObjSlots1(self):
        st = """x.a=y.a"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),
                         (FORM_TYPE,[(ATOM_TYPE,"slot-value"),(ATOM_TYPE,"x"),
                                     (SHORTCUT_TYPE, "'", (ATOM_TYPE,"a"))]),
                         (FORM_TYPE,[(ATOM_TYPE,"slot-value"),(ATOM_TYPE,"y"),
                                     (SHORTCUT_TYPE, "'", (ATOM_TYPE,"a"))])])])

    def testGetFormsObjSlots2(self):
        st = """x.a="Hi".\\
                      a"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),
                         (FORM_TYPE,[(ATOM_TYPE,"slot-value"),(ATOM_TYPE,"x"),
                                     (SHORTCUT_TYPE, "'", (ATOM_TYPE,"a"))]),
                         (FORM_TYPE,[(ATOM_TYPE,"slot-value"),(ATOM_TYPE,"\"Hi\""),
                                     (SHORTCUT_TYPE, "'", (ATOM_TYPE,"a"))])])])

    def testGetFormsObjSlots3(self):
        st = """x.a=y.
                      a"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsObjSlots4(self):
        st = """x.a=y
                     .a"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormsObjMeth1(self):
        st = """x=y.foo{a,b}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"y"),(ATOM_TYPE,"a"),(ATOM_TYPE,"b")])])])

    def testGetFormsObjMeth2(self):
        st = """x=y.foo{}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"y")])])])

    def testGetFormsObjMeth3(self):
        st = """x=y.foo()"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"y")])])])

    def testGetFormsObjMeth4(self):
        st = """x=y.foo(a,b)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"y"),(ATOM_TYPE,"a"),(ATOM_TYPE,"b")])])])

    def testGetFormsObjMeth5(self):
        st = """x=y.foo(a,:b=67)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"y"),(ATOM_TYPE,"a"),
                                     (ATOM_TYPE,":b"),(ATOM_TYPE,"67")])])])

    def testGetFormsFunc1(self):
        st = """x=foo{a,b}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"a"),(ATOM_TYPE,"b")])])])

    def testGetFormsFunc2(self):
        st = """x=foo{}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo")])])])

    def testGetFormsFunc3(self):
        st = """x=foo()"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo")])])])

    def testGetFormsFunc4(self):
        st = """x=foo(a,b)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"a"),(ATOM_TYPE,"b")])])])

    def testGetFormsFunc5(self):
        st = """x=foo(a,:b=67)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"a"),
                                     (ATOM_TYPE,":b"),(ATOM_TYPE,"67")])])])

    def testGetFormInnerFuncCallList1(self):
        st = """foo(a,b=2, .(c=3,d) e,f)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"a"),(ATOM_TYPE,"b"),(ATOM_TYPE,"2"),
                         (FORM_TYPE,[(ATOM_TYPE,"c"),(ATOM_TYPE,"3"),(ATOM_TYPE,"d")]),
                         (ATOM_TYPE,"e"),(ATOM_TYPE,"f")])])

    def testGetFormDict1(self):
        st = """x={}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-hash-table_")])])])

    def testGetFormDict2(self):
        st = """x={a,b
                   c}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-hash-table_"),
                                     (ATOM_TYPE,"a"),(ATOM_TYPE,"nil"),
                                     (ATOM_TYPE,"b"),(ATOM_TYPE,"nil"),
                                     (ATOM_TYPE,"c"),(ATOM_TYPE,"nil")])])])

    def testGetFormDict3(self):
        st = """x={a,b->45
                   c->"Hi"}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-hash-table_"),
                                     (ATOM_TYPE,"a"),(ATOM_TYPE,"nil"),
                                     (ATOM_TYPE,"b"),(ATOM_TYPE,"45"),
                                     (ATOM_TYPE,"c"),(ATOM_TYPE,"\"Hi\"")])])])

    def testGetFormDict4(self):
        st = """x={a
                   b->45-y}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-hash-table_"),
                                     (ATOM_TYPE,"a"),(ATOM_TYPE,"nil"),
                                     (ATOM_TYPE,"b"),(FORM_TYPE,[(ATOM_TYPE,"_-_"),(ATOM_TYPE,"45"),
                                                                 (ATOM_TYPE,"y")])])])])

    def testGetFormDict5(self):
        st = """x={a,->45
                   c->"Hi"}"""  # key is missing before '->'
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormDict6(self):
        st = """x={a,b->
                   c->"Hi"}"""  # value is missing after '->'
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormGetitem1(self):
        st = """a[]"""  # missing any index
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormGetitem2(self):
        st = """a[->]"""  # missing any index
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormGetitem3(self):
        st = """a[->,2]"""  # missing any index
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo())

    def testGetFormGetitem4(self):
        st = """a[2]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_getitem_"),(ATOM_TYPE,"a"),(ATOM_TYPE,"2")])])

    def testGetFormGetitem5(self):
        st = """a[2->]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_getitem_"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-slice_"),(ATOM_TYPE,"2"),
                                     (ATOM_TYPE,"nil"),(ATOM_TYPE,"nil")])])])

    def testGetFormGetitem6(self):
        st = """a[->2]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_getitem_"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-slice_"),(ATOM_TYPE,"nil"),
                                     (ATOM_TYPE,"2"),(ATOM_TYPE,"nil")])])])

    def testGetFormGetitem7(self):
        st = """a[2->9]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_getitem_"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-slice_"),(ATOM_TYPE,"2"),
                                     (ATOM_TYPE,"9"),(ATOM_TYPE,"nil")])])])

    def testGetFormGetitem8(self):
        st = """a[2->9,2]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_getitem_"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-slice_"),(ATOM_TYPE,"2"),
                                     (ATOM_TYPE,"9"),(ATOM_TYPE,"2")])])])

    def testGetFormGetitem9(self):
        st = """a[2->,2]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_getitem_"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-slice_"),(ATOM_TYPE,"2"),
                                     (ATOM_TYPE,"nil"),(ATOM_TYPE,"2")])])])

    def testGetFormGetitem10(self):
        st = """a[->9,2]"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"_getitem_"),(ATOM_TYPE,"a"),
                         (FORM_TYPE,[(ATOM_TYPE,"_make-slice_"),(ATOM_TYPE,"nil"),
                                     (ATOM_TYPE,"9"),(ATOM_TYPE,"2")])])])



if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFormBuilding))
    unittest.TextTestRunner(verbosity=1).run(suite)

