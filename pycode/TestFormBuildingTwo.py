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


class TestFormBuildingTwo(unittest.TestCase):

    def testGetFormsBlockForm1(self):
        st = """def foo() {
                    ~()
                    ~()}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[]),(FORM_TYPE,[]),(FORM_TYPE,[])])])

    def testGetFormsBlockForm2(self):
        st = """def foo\\
                    () {
                        ~()
                        ~()}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[]),(FORM_TYPE,[]),(FORM_TYPE,[])])])

    def testGetFormsBlockForm3(self):
        st = """def foo
                    () {
                        ~()
                        ~()}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[]),(FORM_TYPE,[]),(FORM_TYPE,[])])])

    def testGetFormsBlockForm4(self):
        st = """def foo ()
                    {~()
                     ~()}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[]),(FORM_TYPE,[]),(FORM_TYPE,[])])])

    def testGetFormsBlockForm5(self):
        st = """def foo() {
                    progn{~(), ~()}
                    ~()}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),(FORM_TYPE,[]),
                         (FORM_TYPE,[(ATOM_TYPE,"progn"),
                                     (FORM_TYPE,[]),(FORM_TYPE,[])]),
                         (FORM_TYPE,[])])])

    def testGetFormsBlockForm6(self):
        st = """def foo {
                    ~()
                    ~()}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[]),(FORM_TYPE,[]),(FORM_TYPE,[])])])

    def testGetFormsBlockForm7(self):
        st = """def foo 
                   {~()
                    ~()}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[]),(FORM_TYPE,[]),(FORM_TYPE,[])])])

    def testGetFormsBlockForm8(self):
        st = """def $foo {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(SHORTCUT_TYPE,",",(ATOM_TYPE,"foo")),
                         (FORM_TYPE,[])])])

    def testGetFormsBlockForm9(self):
        st = """def `$foo {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),
                         (SHORTCUT_TYPE,"`",(SHORTCUT_TYPE,",",(ATOM_TYPE,"foo"))),
                         (FORM_TYPE,[])])])

    def testGetFormsBlockForm10(self):
        st = """def setter foo {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"foo")]),
                         (FORM_TYPE,[])])])

    def testGetFormsBlockForm11(self):
        st = """def setter $foo {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(SHORTCUT_TYPE,",",(ATOM_TYPE,"foo"))]),
                         (FORM_TYPE,[])])])

    def testGetFormsLambdaList1(self):
        st = """def foo(a) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a")])])])

    def testGetFormsLambdaList2(self):
        st = """def foo(a,) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a")])])])

    def testGetFormsLambdaList3(self):
        st = """def foo(a,b) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"b")])])])

    def testGetFormsLambdaList4(self):
        st = """def foo(a,b,) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"b")])])])

    def testGetFormsLambdaList5(self):
        st = """def foo(a,b,&&key) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"b"),
                                     (ATOM_TYPE,"&key")])])])

    def testGetFormsLambdaList6(self):
        st = """def foo(a,&&optional,b) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"&optional"),
                                     (ATOM_TYPE,"b")])])])

    def testGetFormsLambdaList7(self):
        st = """def foo(a,b=5) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"&optional"),
                                     (FORM_TYPE,[(ATOM_TYPE,"b"),(ATOM_TYPE,"5")])])])])

    def testGetFormsLambdaList8(self):
        st = """def foo(a,b=5=?bPresent) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"&optional"),
                                     (FORM_TYPE,[(ATOM_TYPE,"b"),(ATOM_TYPE,"5"),
                                                 (ATOM_TYPE,"bPresent")])])])])

    def testGetFormsLambdaList9(self):
        st = """def foo(a,b=?bPresent) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"&optional"),
                                     (FORM_TYPE,[(ATOM_TYPE,"b"),(ATOM_TYPE,"nil"),
                                                 (ATOM_TYPE,"bPresent")])])])])

    def testGetFormsLambdaList10(self):
        st = """def foo(a,bKey->b=?bPresent) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"&key"),
                                     (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"bKey"),(ATOM_TYPE,"b")]),
                                                 (ATOM_TYPE,"nil"),(ATOM_TYPE,"bPresent")])])])])

    def testGetFormsLambdaList11(self):
        st = """def foo(a,bKey->b=5=?bPresent) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"&key"),
                                     (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"bKey"),(ATOM_TYPE,"b")]),
                                                 (ATOM_TYPE,"5"),(ATOM_TYPE,"bPresent")])])])])

    def testGetFormsLambdaList12(self):
        st = """def foo(a,&&aux b=5) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"&aux"),
                                     (FORM_TYPE,[(ATOM_TYPE,"b"),(ATOM_TYPE,"5")])])])])

    def testGetFormsMacLambdaList1(self):
        st = """mac foo(a,.(**body),b=5=?bPresent) {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defmacro"),(ATOM_TYPE,"foo"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),
                                     (FORM_TYPE,[(ATOM_TYPE,"&body"),(ATOM_TYPE,"body")]),
                                     (ATOM_TYPE,"&optional"),
                                     (FORM_TYPE,[(ATOM_TYPE,"b"),(ATOM_TYPE,"5"),
                                                 (ATOM_TYPE,"bPresent")])])])])

    def testGetFormsLetList1(self):
        st = """let () {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[]),(ATOM_TYPE,"a")])])

    def testGetFormsLetList2(self):
        st = """let {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[]),(ATOM_TYPE,"a")])])

    def testGetFormsLetList3(self):
        st = """let (x,y) {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x"),(ATOM_TYPE,"y")]),
                         (ATOM_TYPE,"a")])])

    def testGetFormsLetList4(self):
        st = """let (x,y=a) {y}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x"),
                                                       (FORM_TYPE,[(ATOM_TYPE,"y"),(ATOM_TYPE,"a")])]),
                         (ATOM_TYPE,"y")])])

    def testGetFormsLetList5(self):
        st = """let (x,y=a=5) {y}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[(ATOM_TYPE,"x"),
                                                       (FORM_TYPE,[(ATOM_TYPE,"y"),
                                                                   (FORM_TYPE,[(ATOM_TYPE,"setf"),
                                                                               (ATOM_TYPE,"a"),
                                                                               (ATOM_TYPE,"5")])])]),
                         (ATOM_TYPE,"y")])])

    def testGetFormsBlockName1(self):
        st = """block {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"block"),(ATOM_TYPE,"nil"),(ATOM_TYPE,"a")])])

    def testGetFormsBlockName2(self):
        st = """block nil {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"block"),(ATOM_TYPE,"nil"),(ATOM_TYPE,"a")])])

    def testGetFormsBlockName3(self):
        st = """block foo {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"block"),(ATOM_TYPE,"foo"),(ATOM_TYPE,"a")])])

    def testGetFormsBlockName4(self):
        st = """block $foo {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"block"),
                         (SHORTCUT_TYPE,",",(ATOM_TYPE,"foo")),
                         (ATOM_TYPE,"a")])])

    def testGetFormsBlockName5(self):
        st = """block `$foo {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"block"),
                         (SHORTCUT_TYPE,"`",(SHORTCUT_TYPE,",",(ATOM_TYPE,"foo"))),
                         (ATOM_TYPE,"a")])])

    def testGetFormsDoLists1(self):
        st = """do () {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"do"),(FORM_TYPE,[]),(FORM_TYPE,[(ATOM_TYPE,LISP_NIL)]),
                         (ATOM_TYPE,"a")])])

    def testGetFormsDoLists2(self):
        st = """do () () {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"do"),(FORM_TYPE,[]),(FORM_TYPE,[(ATOM_TYPE,LISP_NIL)]),
                         (ATOM_TYPE,"a")])])

    def testGetFormsDoLists3(self):
        st = """do () (a==2) {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"do"),(FORM_TYPE,[]),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"_==_"),(ATOM_TYPE,"a"),(ATOM_TYPE,"2")])]),
                         (ATOM_TYPE,"a")])])

    def testGetFormsDoLists4(self):
        st = """do () (a==2,"Some computed form","Return result") {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"do"),(FORM_TYPE,[]),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"_==_"),(ATOM_TYPE,"a"),(ATOM_TYPE,"2")]),
                                     (ATOM_TYPE,"\"Some computed form\""),(ATOM_TYPE,"\"Return result\"")]),
                         (ATOM_TYPE,"a")])])

    def testGetFormsDoLists5(self):
        st = """do (a) (a==2,"Return result") {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"do"),(FORM_TYPE,[(ATOM_TYPE,"a")]),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"_==_"),(ATOM_TYPE,"a"),(ATOM_TYPE,"2")]),
                                     (ATOM_TYPE,"\"Return result\"")]),
                         (ATOM_TYPE,"a")])])

    def testGetFormsDoLists6(self):
        st = """do (a=0,b) (a==2,"Return result") {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"do"),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"a"), (ATOM_TYPE,"0")]),(ATOM_TYPE,"b")]),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"_==_"),(ATOM_TYPE,"a"),(ATOM_TYPE,"2")]),
                                     (ATOM_TYPE,"\"Return result\"")]),
                         (ATOM_TYPE,"a")])])

    def testGetFormsDoLists7(self):
        st = """do (a=0->a+b,b=1) {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"do"),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"a"), (ATOM_TYPE,"0"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"a"),
                                                             (ATOM_TYPE,"b")])]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"b"), (ATOM_TYPE,"1")])]),
                         (FORM_TYPE,[(ATOM_TYPE,LISP_NIL)]),
                         (ATOM_TYPE,"a")])])

    def testGetFormsDoLists8(self):
        st = """do (a->a+b,b=1) (a==2,"Return result") {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"do"),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"a"), (ATOM_TYPE,"nil"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"a"),
                                                             (ATOM_TYPE,"b")])]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"b"), (ATOM_TYPE,"1")])]),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"_==_"),(ATOM_TYPE,"a"),(ATOM_TYPE,"2")]),
                                     (ATOM_TYPE,"\"Return result\"")]),
                         (ATOM_TYPE,"a")])])

    def testGetFormsDoLists9(self):
        st = """do 
                  (a=0->a+b)
                  (a==2,"Return result") 
                  {a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"do"),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"a"), (ATOM_TYPE,"0"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"a"),
                                                             (ATOM_TYPE,"b")])])]),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"_==_"),(ATOM_TYPE,"a"),(ATOM_TYPE,"2")]),
                                     (ATOM_TYPE,"\"Return result\"")]),
                         (ATOM_TYPE,"a")])])

    def testGetFormsBreak1(self):
        st = """break
                x=3"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"nil"),(FORM_TYPE,[])]),
             (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"3")])])

    def testGetFormsBreak2(self):
        st = """break x=3"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"nil"),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"3")])])])

    def testGetFormsBreak3(self):
        st = """break from blockName x=3"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"blockName"),
                         (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"3")])])])

    def testGetFormsBreak4(self):
        st = """break from blockName
                x=3"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"blockName"),(FORM_TYPE,[])]),
             (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"3")])])

    def testGetFormsBreak5(self):
        st = """break from $blockName
                x=3"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"return-from"),
                         (SHORTCUT_TYPE,",",(ATOM_TYPE,"blockName")),
                         (FORM_TYPE,[])]),
             (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"3")])])

    def testGetFormsBreak6(self):
        st = """break from `$blockName
                x=3"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"return-from"),
                         (SHORTCUT_TYPE,"`",(SHORTCUT_TYPE,",",(ATOM_TYPE,"blockName"))),
                         (FORM_TYPE,[])]),
             (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"3")])])

    def testGetFormsReturn1(self):
        st = """def foo {return}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),(FORM_TYPE,[]),
                         (FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"foo"),(FORM_TYPE,[])])])])

    def testGetFormsReturn2(self):
        st = """def foo {return a}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),(FORM_TYPE,[]),
                         (FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"foo"),(ATOM_TYPE,"a")])])])

    def testGetFormsReturn3(self):
        st = """def foo {return a@b@c}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),(FORM_TYPE,[]),
                         (FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"foo"),
                                     (FORM_TYPE,[(ATOM_TYPE,"values"),(ATOM_TYPE,"a"),(ATOM_TYPE,"b"),
                                                 (ATOM_TYPE,"c")])])])])

    def testGetFormsReturn4(self):
        st = """def foo {do () () {return a@b@c}}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"defun"),(ATOM_TYPE,"foo"),(FORM_TYPE,[]),
                         (FORM_TYPE,[(ATOM_TYPE,"do"),(FORM_TYPE,[]),(FORM_TYPE,[(ATOM_TYPE,LISP_NIL)]),
                                     (FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"foo"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"values"),(ATOM_TYPE,"a"),
                                                             (ATOM_TYPE,"b"),(ATOM_TYPE,"c")])])])])])

    def testGetFormsIf1(self):
        st = """if (a) {x=b}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"cond"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"b")])])])])

    def testGetFormsIf2(self):
        st = """if (a) {x=b}
                elif (c) {y=0}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"cond"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"b")])]),
                         (FORM_TYPE,[(ATOM_TYPE,"c"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"y"),(ATOM_TYPE,"0")])])])])

    def testGetFormsIf3(self):
        st = """if (a) {x=b}
                elif (c) {y=0}
                elif (d) {y=1}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"cond"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"b")])]),
                         (FORM_TYPE,[(ATOM_TYPE,"c"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"y"),(ATOM_TYPE,"0")])]),
                         (FORM_TYPE,[(ATOM_TYPE,"d"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"y"),(ATOM_TYPE,"1")])])])])

    def testGetFormsIf4(self):
        st = """if (a) {x=b}
                elif (c) {y=0}
                else {foo()}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"cond"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"b")])]),
                         (FORM_TYPE,[(ATOM_TYPE,"c"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"y"),(ATOM_TYPE,"0")])]),
                         (FORM_TYPE,[(ATOM_TYPE,"t"),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo")])])])])

    def testGetFormsIf5(self):
        st = """if (a) {x=b}
                elif (b) {x=0}
                elif (c) {y=0}
                else {foo()}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"cond"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"b")])]),
                         (FORM_TYPE,[(ATOM_TYPE,"b"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"0")])]),
                         (FORM_TYPE,[(ATOM_TYPE,"c"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"y"),(ATOM_TYPE,"0")])]),
                         (FORM_TYPE,[(ATOM_TYPE,"t"),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo")])])])])

    def testGetFormsIf6(self):
        st = """if (a) {x=b}
                else {foo()}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"cond"),
                         (FORM_TYPE,[(ATOM_TYPE,"a"),
                                     (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"x"),(ATOM_TYPE,"b")])]),
                         (FORM_TYPE,[(ATOM_TYPE,"t"),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo")])])])])

    def testGetFormsFlet1(self):
        st = """flet {}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,[(FORM_TYPE,[(ATOM_TYPE,"flet"),(FORM_TYPE,[])])])

    def testGetFormsFlet2(self):
        st = """flet foo (a,b) {a+b}
                     boo (a,b) {a*b}
                     pr {}
                     {foo(1,2)-boo(3,4)}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"flet"),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"foo"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"b")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"a"),(ATOM_TYPE,"b")])]),
                                     (FORM_TYPE,[(ATOM_TYPE,"boo"),
                                                 (FORM_TYPE,[(ATOM_TYPE,"a"),(ATOM_TYPE,"b")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"_*_"),(ATOM_TYPE,"a"),
                                                             (ATOM_TYPE,"b")])]),
                                     (FORM_TYPE,[(ATOM_TYPE,"pr"),(FORM_TYPE,[])])]),
                         (FORM_TYPE,[(ATOM_TYPE,"_-_"),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"1"),(ATOM_TYPE,"2")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"boo"),(ATOM_TYPE,"3"),(ATOM_TYPE,"4")])])])])

    def testGetFormsFletAndReturn1(self):
        st = """flet foo {return}
                     boo (a) {return a}
                     pr (b) {return}
                     {foo(1,2)-boo(3,4)}"""
        forms = getForms(GrowingList(StringIO.StringIO(st)),LevelInfo())
        self.assertEqual(forms,
            [(FORM_TYPE,[(ATOM_TYPE,"flet"),
                         (FORM_TYPE,[(FORM_TYPE,[(ATOM_TYPE,"foo"),(FORM_TYPE,[]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"foo"),
                                                             (FORM_TYPE,[])])]),
                                     (FORM_TYPE,[(ATOM_TYPE,"boo"),(FORM_TYPE,[(ATOM_TYPE,"a")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"boo"),
                                                             (ATOM_TYPE,"a")])]),
                                     (FORM_TYPE,[(ATOM_TYPE,"pr"),(FORM_TYPE,[(ATOM_TYPE,"b")]),
                                                 (FORM_TYPE,[(ATOM_TYPE,"return-from"),(ATOM_TYPE,"pr"),
                                                             (FORM_TYPE,[])])])]),
                         (FORM_TYPE,[(ATOM_TYPE,"_-_"),
                                     (FORM_TYPE,[(ATOM_TYPE,"foo"),(ATOM_TYPE,"1"),(ATOM_TYPE,"2")]),
                                     (FORM_TYPE,[(ATOM_TYPE,"boo"),(ATOM_TYPE,"3"),(ATOM_TYPE,"4")])])])])



if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFormBuildingTwo))
    unittest.TextTestRunner(verbosity=1).run(suite)
