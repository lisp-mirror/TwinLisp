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
from StringReading import markElemsInStr, GrowingList, DummyGrowingList,\
                          REG_PHASE, STRING_PHASE, CLISP_PHASE


class TestMarkElemsInStr(unittest.TestCase):

    def testMarkElemsInStr1(self):
        # note unix end line character
        st = "  &lisp-symbol = foo(x,y)*.45  ; this is comment\n"
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        for num in (0,13):
            strElem = res[0][num]
            self.assertEqual(strElem.type,strElem.WHITE_TYPE)
            self.assertEqual(strElem.value,None)
        strElem = res[0][1]
        self.assertEqual(strElem.lineNum,0)
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"lisp-symbol")
        for num in (2,4):
            strElem = res[0][num]
            self.assertEqual(strElem.type,strElem.WHITE_TYPE)
        strElem = res[0][3]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][5]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"foo")
        strElem = res[0][6]
        self.assertEqual(strElem.type,"(")
        self.assertEqual(strElem.value,"(")
        strElem = res[0][7]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][8]
        self.assertEqual(strElem.type,",")
        self.assertEqual(strElem.value,",")
        strElem = res[0][9]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"y")
        strElem = res[0][10]
        self.assertEqual(strElem.type,")")
        self.assertEqual(strElem.value,")")
        strElem = res[0][11]
        self.assertEqual(strElem.type,"*")
        self.assertEqual(strElem.value,"*")
        strElem = res[0][12]
        self.assertEqual(strElem.type,strElem.NUM_TYPE)
        self.assertEqual(strElem.value,".45")
        strElem = res[0][14]
        self.assertEqual(strElem.type,strElem.COMM_TYPE)
        self.assertEqual(strElem.value,"; this is comment")
        strElem = res[0][15]
        self.assertEqual(strElem.type,strElem.LINE_END_TYPE)
        self.assertEqual(strElem.value,None)

    def testMarkElemsInStr2(self):
        # note mac's end line character
        st = """\t&+symbol = foo+"Some string"  ; this is comment\r"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.WHITE_TYPE)
        self.assertEqual(strElem.value,None)
        strElem = res[0][1]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"+symbol")
        for num in (2,4):
            strElem = res[0][num]
            self.assertEqual(strElem.type,strElem.WHITE_TYPE)
        strElem = res[0][3]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][5]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"foo")
        strElem = res[0][6]
        self.assertEqual(strElem.type,"+")
        self.assertEqual(strElem.value,"+")
        strElem = res[0][7]
        self.assertEqual(strElem.type,strElem.STR_START_TYPE)
        self.assertEqual(strElem.value,"\"")
        strElem = res[0][8]
        self.assertEqual(strElem.type,strElem.STR_END_TYPE)
        self.assertEqual(strElem.value,"Some string\"")
        strElem = res[0][9]
        self.assertEqual(strElem.type,strElem.WHITE_TYPE)
        strElem = res[0][10]
        self.assertEqual(strElem.type,strElem.COMM_TYPE)
        self.assertEqual(strElem.value,"; this is comment")
        strElem = res[0][11]
        self.assertEqual(strElem.type,strElem.LINE_END_TYPE)
        self.assertEqual(strElem.value,None)

    def testMarkElemsInStr3(self):
        # note win's end line character
        st = """foo=="String spreads to several lines, has \\"-quotes\r\n"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],STRING_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"foo")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"==")
        self.assertEqual(strElem.value,"==")
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.STR_START_TYPE)
        self.assertEqual(strElem.value,"\"")
        strElem = res[0][3]
        self.assertEqual(strElem.type,strElem.STR_MID_TYPE)
        self.assertEqual(strElem.value,
                         "String spreads to several lines, has \\\"-quotes\r\n")

    def testMarkElemsInStr4(self):
        # line of a multiline string
        st = """string started before, and does not end here\n"""
        res = markElemsInStr(st,0,initPhase=STRING_PHASE)
        self.assertEqual(res[1],STRING_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.STR_MID_TYPE)
        self.assertEqual(strElem.value,
                         "string started before, and does not end here\n")
        st = """\n"""
        res = markElemsInStr(st,0,initPhase=STRING_PHASE)
        self.assertEqual(res[1],STRING_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.STR_MID_TYPE)
        self.assertEqual(strElem.value,"\n")
        st = """\r\n"""
        res = markElemsInStr(st,0,initPhase=STRING_PHASE)
        self.assertEqual(res[1],STRING_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.STR_MID_TYPE)
        self.assertEqual(strElem.value,"\r\n")

    def testMarkElemsInStr5(self):
        # line of a multiline string
        st = """string started before, and ends here"  ; some comment\n"""
        res = markElemsInStr(st,0,initPhase=STRING_PHASE)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.STR_END_TYPE)
        self.assertEqual(strElem.value,
                         "string started before, and ends here\"")
        strElem = res[0][1]
        self.assertEqual(strElem.type,strElem.WHITE_TYPE)
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.COMM_TYPE)
        self.assertEqual(strElem.value,"; some comment")

    def testMarkElemsInStr6(self):
        st = """x[0]=&+$%^\\(-symbol(23.4)\n"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"[")
        self.assertEqual(strElem.value,"[")
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.NUM_TYPE)
        self.assertEqual(strElem.value,"0")
        strElem = res[0][3]
        self.assertEqual(strElem.type,"]")
        self.assertEqual(strElem.value,"]")
        strElem = res[0][4]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][5]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"+$%^\\(-symbol")
        strElem = res[0][6]
        self.assertEqual(strElem.type,"(")
        self.assertEqual(strElem.value,"(")
        strElem = res[0][7]
        self.assertEqual(strElem.type,strElem.NUM_TYPE)
        self.assertEqual(strElem.value,"23.4")
        strElem = res[0][8]
        self.assertEqual(strElem.type,")")
        self.assertEqual(strElem.value,")")

    def testMarkElemsInStr7(self):
        st = """x=&&symbol[23.4]\\(()\n"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"&symbol[23.4]\\(")
        strElem = res[0][3]
        self.assertEqual(strElem.type,"(")
        self.assertEqual(strElem.value,"(")
        strElem = res[0][4]
        self.assertEqual(strElem.type,")")
        self.assertEqual(strElem.value,")")

    def testMarkElemsInStr8(self):
        st = """\n"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.LINE_END_TYPE)

    def testMarkElemsInStr9(self):
        st = """x=&\\\n"""  # #\Newline will not be treated as part of a symbol
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][2]
        self.assertEqual(strElem.type,"&")
        self.assertEqual(strElem.value,"&")
        strElem = res[0][3]
        self.assertEqual(strElem.type,"\\")
        self.assertEqual(strElem.value,"\\")

    def testMarkElemsInStr10(self):
        st = """x=""\n"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.STR_START_TYPE)
        self.assertEqual(strElem.value,"\"")
        strElem = res[0][3]
        self.assertEqual(strElem.type,strElem.STR_END_TYPE)
        self.assertEqual(strElem.value,"\"")

    def testMarkElemsInStr11(self):
        st = """x=#b01010\n"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.SYNT_STRUCT_TYPE)
        self.assertEqual(strElem.value,"#b01010")

    def testMarkElemsInStr12(self):
        st = """x=(#\L,4)"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][2]
        self.assertEqual(strElem.type,"(")
        self.assertEqual(strElem.value,"(")
        strElem = res[0][3]
        self.assertEqual(strElem.type,strElem.SYNT_STRUCT_TYPE)
        self.assertEqual(strElem.value,"#\L")
        strElem = res[0][4]
        self.assertEqual(strElem.type,",")
        self.assertEqual(strElem.value,",")
        strElem = res[0][5]
        self.assertEqual(strElem.type,strElem.NUM_TYPE)
        self.assertEqual(strElem.value,"4")
        strElem = res[0][6]
        self.assertEqual(strElem.type,")")
        self.assertEqual(strElem.value,")")

    def testMarkElemsInStr13(self):
        st = """x=#'foo"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][2]
        self.assertEqual(strElem.type,"#'")
        self.assertEqual(strElem.value,"#'")
        strElem = res[0][3]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"foo")

    def testMarkElemsInStr14(self):
        st = """x!=#c(1.,2e-3)"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"!=")
        self.assertEqual(strElem.value,"!=")
        strElem = res[0][2]
        self.assertEqual(strElem.type,"#c")
        self.assertEqual(strElem.value,"#c")
        strElem = res[0][3]
        self.assertEqual(strElem.type,"(")
        self.assertEqual(strElem.value,"(")
        strElem = res[0][4]
        self.assertEqual(strElem.type,strElem.NUM_TYPE)
        self.assertEqual(strElem.value,"1.")
        strElem = res[0][5]
        self.assertEqual(strElem.type,",")
        self.assertEqual(strElem.value,",")
        strElem = res[0][6]
        self.assertEqual(strElem.type,strElem.NUM_TYPE)
        self.assertEqual(strElem.value,"2e-3")
        strElem = res[0][7]
        self.assertEqual(strElem.type,")")
        self.assertEqual(strElem.value,")")

    def testMarkElemsInStr15(self):
        st = """ x = # C(1,2)\n"""
        self.assertRaises(SyntaxError,markElemsInStr,st,0)
        st = """ x = #\\\n"""   # use #\Newline for newline character
        self.assertRaises(SyntaxError,markElemsInStr,st,0)
        st = """x=#\n"""
        self.assertRaises(SyntaxError,markElemsInStr,st,0)
        st = """x=#(fg)\n"""
        self.assertRaises(SyntaxError,markElemsInStr,st,0)
        st = """x=#,fg\n"""
        self.assertRaises(SyntaxError,markElemsInStr,st,0)

    def testMarkElemsInStr16(self):
        st = """x=#\L()"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.SYNT_STRUCT_TYPE)
        self.assertEqual(strElem.value,"#\L")
        strElem = res[0][3]
        self.assertEqual(strElem.type,"(")
        self.assertEqual(strElem.value,"(")
        strElem = res[0][4]
        self.assertEqual(strElem.type,")")
        self.assertEqual(strElem.value,")")

    def testMarkElemsInStr17(self):
        st = """x=3/4+3./4-.5f+7"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.NUM_TYPE)
        self.assertEqual(strElem.value,"3/4")
        strElem = res[0][3]
        self.assertEqual(strElem.type,"+")
        self.assertEqual(strElem.value,"+")
        strElem = res[0][4]
        self.assertEqual(strElem.type,strElem.NUM_TYPE)
        self.assertEqual(strElem.value,"3.")
        strElem = res[0][5]
        self.assertEqual(strElem.type,"/")
        self.assertEqual(strElem.value,"/")
        strElem = res[0][6]
        self.assertEqual(strElem.type,strElem.NUM_TYPE)
        self.assertEqual(strElem.value,"4")
        strElem = res[0][7]
        self.assertEqual(strElem.type,"-")
        self.assertEqual(strElem.value,"-")
        strElem = res[0][8]
        self.assertEqual(strElem.type,strElem.NUM_TYPE)
        self.assertEqual(strElem.value,".5f+7")

    def testMarkElemsInStr18(self):
        st = """x=&lisp-pack:&lisp-symb\n"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"x")
        strElem = res[0][1]
        self.assertEqual(strElem.type,"=")
        self.assertEqual(strElem.value,"=")
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"lisp-pack")
        strElem = res[0][3]
        self.assertEqual(strElem.type,":")
        self.assertEqual(strElem.value,":")
        strElem = res[0][4]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"lisp-symb")

    def testMarkElemsInStr19(self):
        st = """if a & b-c {\n"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"a")
        strElem = res[0][4]
        self.assertEqual(strElem.type,"&")
        self.assertEqual(strElem.value,"&")
        strElem = res[0][5]
        self.assertEqual(strElem.type,strElem.WHITE_TYPE)
        strElem = res[0][6]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"b")
        strElem = res[0][7]
        self.assertEqual(strElem.type,"-")
        self.assertEqual(strElem.value,"-")
        strElem = res[0][8]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"c")

    def testMarkElemsInStr20(self):
        st = """if a &b-c {\n"""
        res = markElemsInStr(st,0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][2]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"a")
        strElem = res[0][4]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"b-c")

    def testMarkElemsInStr21(self):
        res = markElemsInStr("\n",0)
        self.assertEqual(res[1],REG_PHASE)
        self.assertEqual(len(res[0]),1)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.LINE_END_TYPE)
        self.assertEqual(strElem.value,None)

    def testMarkElemsInStr22(self):
        res = markElemsInStr("def foo(&def ){}",0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.SPEC_SYMB_TYPE)
        self.assertEqual(strElem.value,"def")
        strElem = res[0][4]
        self.assertEqual(strElem.type,strElem.SYMB_TYPE)
        self.assertEqual(strElem.value,"def")

    def testMarkElemsInStr23(self):
        res = markElemsInStr("cl{{(+ 1 2)}} - 3 \n",0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.CLISP_START_TYPE)
        self.assert_(strElem.value is None)
        strElem = res[0][1]
        self.assertEqual(strElem.type,strElem.CLISP_END_TYPE)
        self.assertEqual(strElem.value,"(+ 1 2)\n")
        strElem = res[0][3]
        self.assertEqual(strElem.type,"-")
        self.assertEqual(strElem.value,"-")

    def testMarkElemsInStr24(self):
        res = markElemsInStr("cl{{(+ 1 2) ;comment in lisp code}}-3\n",0)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.CLISP_START_TYPE)
        self.assert_(strElem.value is None)
        strElem = res[0][1]
        self.assertEqual(strElem.type,strElem.CLISP_END_TYPE)
        self.assertEqual(strElem.value,"(+ 1 2) ;comment in lisp code\n")

    def testMarkElemsInStr25(self):
        res = markElemsInStr("cl{{(+ 1 2)\n",0)
        self.assertEqual(res[1],CLISP_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.CLISP_START_TYPE)
        self.assert_(strElem.value is None)
        self.assert_(strElem.start is 0)
        self.assert_(strElem.end is None)
        self.assertEqual(strElem.lineNum,0)
        strElem = res[0][1]
        self.assertEqual(strElem.type,strElem.CLISP_MID_TYPE)
        self.assertEqual(strElem.value,"(+ 1 2)\n")

    def testMarkElemsInStr26(self):
        res = markElemsInStr("(+ 1 2)  ;;comment\n",0,initPhase=CLISP_PHASE)
        self.assertEqual(res[1],CLISP_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.CLISP_MID_TYPE)
        self.assertEqual(strElem.value,"(+ 1 2)  ;;comment\n")

    def testMarkElemsInStr27(self):
        res = markElemsInStr("(+ 1 2)  ;;comment}}\n",0,initPhase=CLISP_PHASE)
        self.assertEqual(res[1],REG_PHASE)
        strElem = res[0][0]
        self.assertEqual(strElem.type,strElem.CLISP_END_TYPE)
        self.assertEqual(strElem.value,"(+ 1 2)  ;;comment\n")


class TestGrowingList(unittest.TestCase):

    def testGetItem(self):
        st = """def foo(x,y) { ; definition of function
        "foo adds x and y"
        x+y}"""
        gL = GrowingList(StringIO.StringIO(st))
        self.assertEqual(len(gL),13)
        self.assertEqual(gL[0].value,"def")
        self.assertEqual(gL[1].type,gL[1].WHITE_TYPE)
        self.assertEqual(gL[2].value,"foo")
        self.assertEqual(gL[3].value,"(")
        self.assertEqual(gL[4].value,"x")
        self.assertEqual(gL[5].value,",")
        self.assertEqual(gL[6].value,"y")
        self.assertEqual(gL[7].value,")")
        self.assertEqual(gL[8].type,gL[8].WHITE_TYPE)
        self.assertEqual(gL[9].value,"{")
        self.assertEqual(gL[10].type,gL[10].WHITE_TYPE)
        self.assertEqual(gL[11].value,"; definition of function")
        self.assertEqual(gL[12].type,gL[12].LINE_END_TYPE)
        gL.growOnIndex(13)
        self.assertEqual(len(gL),17)
        self.assertEqual(gL[13].type,gL[13].WHITE_TYPE)
        self.assertEqual(gL[14].value,"\"")
        self.assertEqual(gL[15].value,"foo adds x and y\"")
        self.assertEqual(gL[16].type,gL[16].LINE_END_TYPE)
        gL.growOnIndex(17)
        self.assertEqual(len(gL),23)
        self.assertEqual(gL[17].type,gL[17].WHITE_TYPE)
        self.assertEqual(gL[18].value,"x")
        self.assertEqual(gL[19].value,"+")
        self.assertEqual(gL[20].value,"y")
        self.assertEqual(gL[21].value,"}")
        self.assertEqual(gL[22].type,gL[22].LINE_END_TYPE)
        gL.growOnIndex(23)
        self.assertEqual(len(gL),23)
        self.assertRaises(IndexError,gL.__getitem__,23)
        self.assertEqual(len(gL[10:20]),10)
        self.assertEqual(type(gL[10:20]),type(DummyGrowingList()))
        self.assertEqual(gL[10:20][0],gL[10])
        self.assertEqual(gL[10:20][5],gL[15])
        self.assertEqual(gL[10:20][9],gL[19])


if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMarkElemsInStr))
    suite.addTest(unittest.makeSuite(TestGrowingList))
    unittest.TextTestRunner(verbosity=1).run(suite)

