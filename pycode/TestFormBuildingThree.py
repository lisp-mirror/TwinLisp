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


class TestFormBuildingThree(unittest.TestCase):

    def testGetFormsStruct1(self):
        st = """struct foo {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defstruct"),(FORM_TYPE,[(ATOM_TYPE,"foo")])])])

    def testGetFormsStruct2(self):
        st = """struct foo {a b
                            c}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defstruct"),(FORM_TYPE,[(ATOM_TYPE,"foo")]),
                         (ATOM_TYPE,"a"),(ATOM_TYPE,"b"),(ATOM_TYPE,"c")])])

    def testGetFormsStruct3(self):
        st = """struct foo {a{0} b{1}
                            c}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defstruct"),(FORM_TYPE,[(ATOM_TYPE,"foo")]),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"0")]),
                         (FORM_TYPE,[(ATOM_TYPE,"b"),(ATOM_TYPE,"1")]),
                         (ATOM_TYPE,"c")])])

    def testGetFormsStruct4(self):
        st = """struct foo { a {0,:type=integer}
                             b {1,:&read-only }
                             c}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defstruct"),(FORM_TYPE,[(ATOM_TYPE,"foo")]),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"0"),
                                     (ATOM_TYPE,":type"),(ATOM_TYPE,"integer")]),
                         (FORM_TYPE,[(ATOM_TYPE,"b"),(ATOM_TYPE,"1"),(ATOM_TYPE,":read-only")]),
                         (ATOM_TYPE,"c")])])

    def testGetFormsStruct5(self):
        st = """struct foo { a {0,:type=integer}
                             b {1,:&read-only }}
                   options {:include=boo,:named}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defstruct"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),
                                     (FORM_TYPE,[(ATOM_TYPE,":include"),(ATOM_TYPE,"boo")]),
                                     (ATOM_TYPE,":named")]),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"0"),
                                     (ATOM_TYPE,":type"),(ATOM_TYPE,"integer")]),
                         (FORM_TYPE,[(ATOM_TYPE,"b"),(ATOM_TYPE,"1"),(ATOM_TYPE,":read-only")])])])

    def testGetFormsClass1(self):
        st = """class foo {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defclass"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[]),(FORM_TYPE,[])])])

    def testGetFormsClass2(self):
        st = """class foo {a b
                           c}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defclass"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[]),(FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"b"),(ATOM_TYPE,"c")])])])

    def testGetFormsClass3(self):
        st = """class foo {
                    a {:type=integer}
                    c}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defclass"),(ATOM_TYPE,"foo"),(FORM_TYPE,[]),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,":type"),
                                                 (ATOM_TYPE,"integer")]),
                                     (ATOM_TYPE,"c")])])])

    def testGetFormsClass4(self):
        st = """class foo {
                    a {:type=integer}
                    c}
                  options {:documentation="doc-string"
                           :metaclass=boo}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defclass"),(ATOM_TYPE,"foo"),(FORM_TYPE,[]),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,":type"),
                                                 (ATOM_TYPE,"integer")]),
                                     (ATOM_TYPE,"c")]),
                         (FORM_TYPE,[(ATOM_TYPE,":documentation"),(ATOM_TYPE,"\"doc-string\"")]),
                         (FORM_TYPE,[(ATOM_TYPE,":metaclass"),(ATOM_TYPE,"boo")])])])

    def testGetFormsClass5(self):
        st = """class foo (super1,super2) {
                     a {:type=integer}
                     ; this comment will be dropped outentirely
                     c}
                  options {:documentation="doc-string"
                           :metaclass=boo}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defclass"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"super1"),(ATOM_TYPE,"super2")]),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,":type"),
                                                 (ATOM_TYPE,"integer")]),
                                     (ATOM_TYPE,"c")]),
                         (FORM_TYPE,[(ATOM_TYPE,":documentation"),(ATOM_TYPE,"\"doc-string\"")]),
                         (FORM_TYPE,[(ATOM_TYPE,":metaclass"),(ATOM_TYPE,"boo")])])])

    def testGetFormsMeth1(self):
        st = """meth foo (a){}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defmethod"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a")])])])

    def testGetFormsMeth2(self):
        st = """meth foo :after (a){}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defmethod"),(ATOM_TYPE,"foo"),(ATOM_TYPE,":after"),
                         (FORM_TYPE,[(ATOM_TYPE,"a")])])])

    def testGetFormsMeth3(self):
        st = """meth setter foo (a){}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defmethod"),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"foo")]),
                         (FORM_TYPE,[(ATOM_TYPE,"a")])])])

    def testGetFormsUse1(self):
        st = """use foo {x,y,z}
                x(a)
                y(b)
                z(c)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"foo:x"),(ATOM_TYPE,"a")]),
             (FORM_TYPE,[(ATOM_TYPE,"foo:y"),(ATOM_TYPE,"b")]),
             (FORM_TYPE,[(ATOM_TYPE,"foo:z"),(ATOM_TYPE,"c")])])

    def testGetFormsUse2(self):
        st = """use foo {x=e,y=f,z}
                e(a)
                x(a)
                f(b)
                y(b)
                z(c)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"foo:x"),(ATOM_TYPE,"a")]),
             (FORM_TYPE,[(ATOM_TYPE,"x"),(ATOM_TYPE,"a")]),
             (FORM_TYPE,[(ATOM_TYPE,"foo:y"),(ATOM_TYPE,"b")]),
             (FORM_TYPE,[(ATOM_TYPE,"y"),(ATOM_TYPE,"b")]),
             (FORM_TYPE,[(ATOM_TYPE,"foo:z"),(ATOM_TYPE,"c")])])

    def testGetFormsUse3(self):
        st = """use foo: {x,y,z}
                x(a)
                y(b)
                z(c)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"foo::x"),(ATOM_TYPE,"a")]),
             (FORM_TYPE,[(ATOM_TYPE,"foo::y"),(ATOM_TYPE,"b")]),
             (FORM_TYPE,[(ATOM_TYPE,"foo::z"),(ATOM_TYPE,"c")])])

    def testGetFormsUse4(self):
        st = """use foo {x}
                func(x)
                func(:x)
                func(cl:x)
                func(cl::x)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"func"),(ATOM_TYPE,"foo:x")]),
             (FORM_TYPE,[(ATOM_TYPE,"func"),(ATOM_TYPE,":x")]),
             (FORM_TYPE,[(ATOM_TYPE,"func"),(ATOM_TYPE,"cl:x")]),
             (FORM_TYPE,[(ATOM_TYPE,"func"),(ATOM_TYPE,"cl::x")])])

    def testGetFormsUse5(self):
        st = """use {x=a,y=b}
                a(1)
                b(2)"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"x"),(ATOM_TYPE,"1")]),
             (FORM_TYPE,[(ATOM_TYPE,"y"),(ATOM_TYPE,"2")])])

    def testGetFormsImplicitLexscope1(self):
        st = """progn{
                    foo(x)
                    x=1
                    foo(x)}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"progn"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")]),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),
                                                 (ATOM_TYPE,"x"),(ATOM_TYPE,"1")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")])])])])

    def testGetFormsImplicitLexscope2(self):
        st = """progn{
                    foo(x)
                    x=y=1
                    foo(x)}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"progn"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")]),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"y"),(ATOM_TYPE,"x")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"y"),
                                                             (ATOM_TYPE,"1")])]),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")])])])])

    def testGetFormsImplicitLexscope3(self):
        st = """progn{
                    foo(x)
                    x=0
                    y=1
                    foo(x)}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"progn"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")]),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"0")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"y")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"setf"),
                                                             (ATOM_TYPE,"y"),(ATOM_TYPE,"1")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")])])])])])

    def testGetFormsImplicitLexscope4(self):
        st = """progn{
                    foo(x)
                    x=1
                    global y
                    y=0
                    foo(x)}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"progn"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")]),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"1")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"y"),(ATOM_TYPE,"0")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")])])])])

    def testGetFormsImplicitLexscope5(self):
        st = """progn{
                    foo(x)
                    x=1
                    x=0
                    foo(x)}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"progn"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")]),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"1")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"0")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")])])])])

    def testGetFormsImplicitLexscope6(self):
        st = """progn{
                    foo(x)
                    x=1
                    lexscope explicit
                    y=0
                    foo(x)}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"progn"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")]),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"1")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"y"),(ATOM_TYPE,"0")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")])])])])

    def testGetFormsImplicitLexscope7(self):
        st = """progn{
                    foo(x)
                    x=0
                    lexscope explicit
                    z=1
                    lexscope implicit
                    y=2
                    foo(x)}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"progn"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")]),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"0")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"z"),(ATOM_TYPE,"1")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"y")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"setf"),
                                                             (ATOM_TYPE,"y"),(ATOM_TYPE,"2")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")])])])])])

    def testGetFormsImplicitLexscope8(self):
        st = """progn{
                    foo(x)
                    x=0
                    lexscope explicit
                    z=1
                    lexscope implicit
                    y=2
                    foo(x)}"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo(implScope=True,explScopeWarn=True))

    def testGetFormsImplicitLexscope9(self):
        st = """progn{
                    foo(x)
                    x=0
                    lexscope explicit
                    global z
                    z=1
                    lexscope implicit
                    y=2
                    foo(x)}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True,explScopeWarn=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"progn"),
                         (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")]),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"0")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"z"),(ATOM_TYPE,"1")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"y")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"setf"),
                                                             (ATOM_TYPE,"y"),(ATOM_TYPE,"2")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"x")])])])])])

    def testGetFormsImplicitLexscope10(self):
        st = """def foo (a) {
                    a = 1
                    b = 2}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True,explScopeWarn=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),(FORM_TYPE,[(ATOM_TYPE,"a")]),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),(ATOM_TYPE,"1")]),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"b")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"b"),(ATOM_TYPE,"2")])])])])

    def testGetFormsImplicitLexscope11(self):
        st = """mac foo (a) {
                    a = 1
                    b = 2}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defmacro"),(ATOM_TYPE,"foo"),(FORM_TYPE,[(ATOM_TYPE,"a")]),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),(ATOM_TYPE,"1")]),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"b"),(ATOM_TYPE,"2")])])])

    def testGetFormsImplicitLexscope12(self):
        st = """a = 1
                b = 2
                mac foo (a) {
                    a = 1
                    b = 2}"""
        allElems = GrowingList(StringIO.StringIO(st))
        self.assertRaises(SyntaxError,getForms,allElems,LevelInfo(implScope=True,explScopeWarn=True))

    def testGetFormsImplicitLexscope13(self):
        st = """a = 1
                b = 2
                mac foo (a) {
                    a = 1
                    global b
                    b = 2}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True,explScopeWarn=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),(ATOM_TYPE,"1")]),
             (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"b"),(ATOM_TYPE,"2")]),
             (FORM_TYPE,[(ATOM_TYPE,"defmacro"),(ATOM_TYPE,"foo"),(FORM_TYPE,[(ATOM_TYPE,"a")]),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),(ATOM_TYPE,"1")]),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"b"),(ATOM_TYPE,"2")])])])

    def testGetFormsImplicitLexscope14(self):
        st = """a = 1
                b = 2
                def foo (a) {
                    a = 1
                    b = 2}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True,explScopeWarn=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),(ATOM_TYPE,"1")]),
             (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"b"),(ATOM_TYPE,"2")]),
             (FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),(FORM_TYPE,[(ATOM_TYPE,"a")]),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),(ATOM_TYPE,"1")]),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"b")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"b"),(ATOM_TYPE,"2")])])])])

    def testGetFormsImplicitLexscope15(self):
        st = """def foo (a,b=lambda{a=1}) { a=9 }"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True,explScopeWarn=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"&optional"),
                                     (FORM_TYPE,[(ATOM_TYPE,"b"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"lambda"),(FORM_TYPE,[]),
                                                    (FORM_TYPE,[(ATOM_TYPE,"let"),
                                                                 (FORM_TYPE,[(ATOM_TYPE,"a")]),
                                                                 (FORM_TYPE,[(ATOM_TYPE,"setf"),
                                                                             (ATOM_TYPE,"a"),
                                                                             (ATOM_TYPE,"1")])])])])]),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),(ATOM_TYPE,"9")])])])

    def testGetFormsImplicitLexscope16(self):
        st = """progn{
                    x @ y = foo()
                    x+y}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo(implScope=True))
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"progn"),
                         (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x"),(ATOM_TYPE,"y")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"values"),(ATOM_TYPE,"x"),
                                                             (ATOM_TYPE,"y")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"foo")])]),
                                     (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),(ATOM_TYPE,"y")])])])])




if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFormBuildingThree))
    unittest.TextTestRunner(verbosity=1).run(suite)

