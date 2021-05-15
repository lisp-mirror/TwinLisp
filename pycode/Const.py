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
#
#   constants
#

CLISP_START_STRING = "cl{{"
CLISP_END_STRING = "}}"

# BRACKETS describes enclosing symbols (brackets): key is an openning 'bracket', value is a closing one
BRACKETS = {"(": ")", "[": "]", "{": "}", "~(": ")", "~[": "]"}
CLOSING_BRACKETS = BRACKETS.values()

# types of operator association
RIGHT_ASSOC = "right-association"
LEFT_ASSOC = "left-association"
MULT_ARGS_ASSOC = "multi-arguments-to-one-func-call"

UNAR_OPERS = {"+": ["_unary+_",2,RIGHT_ASSOC],
              "-": ["_unary-_",2,RIGHT_ASSOC],
              "!": ["_not_",2,RIGHT_ASSOC],
              "not": ["_not_",2,RIGHT_ASSOC]}

BIN_OPERS = {"**": ["_**_",3,RIGHT_ASSOC],
             "*": ["_*_",4,LEFT_ASSOC],
             "/": ["_/_",4,LEFT_ASSOC],
             "%": ["_%_",4,LEFT_ASSOC],
             "+": ["_+_",5,LEFT_ASSOC],
             "-": ["_-_",5,LEFT_ASSOC],
             "<": ["_<_",7,LEFT_ASSOC],
             ">": ["_>_",7,LEFT_ASSOC],
             "<=": ["_<=_",7,LEFT_ASSOC],
             ">=": ["_>=_",7,LEFT_ASSOC],
             "==": ["_==_",8,LEFT_ASSOC],
             "!=": ["_!=_",8,LEFT_ASSOC],
             "&": ["_and_",9,LEFT_ASSOC],
             "and": ["_and_",9,LEFT_ASSOC],
             "^": ["_xor_",10,LEFT_ASSOC],
             "xor": ["_xor_",10,LEFT_ASSOC],
             "|": ["_or_",11,LEFT_ASSOC],
             "or": ["_or_",11,LEFT_ASSOC],
             "<<": ["_<<_",13,LEFT_ASSOC],
             "@": ["values",14,MULT_ARGS_ASSOC],
             "=": ["setf",15,RIGHT_ASSOC],
             "+=": ["_+=_",15,RIGHT_ASSOC],
             "-=": ["_-=_",15,RIGHT_ASSOC],
             "*=": ["_*=_",15,RIGHT_ASSOC],
             "/=": ["_/=_",15,RIGHT_ASSOC]}

OPER_SYMB = ["and","or","xor","not"]    # "word" operator, not a block structure

SHORTCUT_OPERS = {"'": "'",
                  "#.": "#.",
                  "#'": "#'",
                  "`": "`",
                  "$": ",",
                  "$@": ",@"}

COMPL_NUM_OPER = ["#C","#c"]

# TwinLisp's names of funcs/methods
MAKE_SIMPLE_ARRAY_FUNC = "_make-vector_"
MAKE_LIST_FUNC = "list"
MAKE_COMPLEX_NUM_FUNC = "complex"
MAKE_DICTIONARY_FUNC = "_make-hash-table_"
GET_ITEM_FUNC = "_getitem_"
MAKE_SLICE_FUNC = "_make-slice_"
GET_OBJ_SLOT_FUNC = "slot-value"
LISP_NIL = "nil"
SETTER_FUNC = "setf"

# Nicknames to "popular" methods
TWL_METH_NICKNAMES = {"pop": "tl-pop",
                      "_pop": "pop",
                      "remove": "tl-remove",
                      "_remove": "remove",
                      "append": "tl-append",
                      "_append": "append",
                      "count": "tl-count",
                      "_count": "count"}

def _getMultiCharOper(opers):
    multOpers = {}
    for operDict in opers:
        for oper in operDict.keys():
            if (OPER_SYMB.count(oper)==0) and (len(oper)>1):
                if multOpers.has_key(oper[0]):
                    multOpers[oper[0]].append(oper)
                else:
                    multOpers[oper[0]] = [oper]
    return multOpers
def _addMultiCharOper(oldOpers,operList):
    for oper in operList:
        if len(oper)>1:
            if oldOpers.has_key(oper[0]):
                oldOpers[oper[0]].append(oper)
            else:
                oldOpers[oper[0]] = [oper]

# DOUBLE_CHAR_OPERS is used in string reading to mark elements
MULTI_CHAR_OPERS = _getMultiCharOper((UNAR_OPERS,BIN_OPERS,SHORTCUT_OPERS))
_addMultiCharOper(MULTI_CHAR_OPERS,COMPL_NUM_OPER)
_addMultiCharOper(MULTI_CHAR_OPERS,["~(","~[","->","::","=?"])


class StrElem(object):
    """
    String is broken into these, not tokens. Tokens carry less info.
    """
    SYMB_TYPE = "symbol"
    SPEC_SYMB_TYPE = "special-symbol"
    NUM_TYPE = "number"
    SYNT_STRUCT_TYPE = "syntactic-structure"
    STR_START_TYPE = "string-start"
    STR_MID_TYPE = "string-middle"
    STR_END_TYPE = "string-end"
    CLISP_START_TYPE = "common-lisp-code-start"
    CLISP_MID_TYPE = "common-lisp-code-middle"
    CLISP_END_TYPE = "common-lisp-code-end"
    WHITE_TYPE = "white-space"
    COMM_TYPE = "comment"
    LINE_END_TYPE = "end-of-line"
    def __init__(self,elemType,value,strNum,start,end):
        self.type = elemType
        self.value = value
        self.lineNum = strNum
        self.start = start
        self.end = end

# AUX_SPEC_SYMB is a list of special words that might be used inside of TL_BLOCK's or TL's directives
AUX_SPEC_SYMB = ["elif", "else","from","is","options","finally","at","cond"]
SETTER_SPEC_SYMB = "setter"
AUX_SPEC_SYMB.append(SETTER_SPEC_SYMB)

# TL_DIRECT_SPEC_SYMB is a list of special words that start TL's directives
TL_DIR_GLOBAL = "global"
TL_DIR_LEXSCOPE = "lexscope"
TL_EXPL_SCOPE = "explicit"
TL_IMPL_SCOPE = "implicit"
TL_DIR_USE = "use"
TL_DIRECT_SPEC_SYMB = [TL_DIR_GLOBAL, TL_DIR_LEXSCOPE, TL_EXPL_SCOPE, TL_IMPL_SCOPE, TL_DIR_USE]

# TYPE's are types of nodes ready for writting 'em directly into lisp code
COMMENT_TYPE = "comment"
SHORTCUT_TYPE = "shortcut"
ATOM_TYPE = "atom"
FORM_TYPE = "form"

# constants for use in TL_BLOCK descriptions and/or in functions that work with elements from TL_BLOCK's
OPTIONAL = "optional element"
MULT = "one or more times"
LAMBDA_LIST_OPTIONS = ["&optional","&rest","&key","&allow-other-keys","&aux"]
MAC_LAMBDA_LIST_OPTIONS = LAMBDA_LIST_OPTIONS + ["&body","&whole","&environment"]
FUN_NAME = "function name"    # one form
NAME = "name on the current line"   # one form
NAME2 = "name on the current or the following line"   # one form
FUN_NAME_FROM_LEVEL = "func name from level info, not from code" # one form
LAMBDA_LIST = "lambda list" # one form
MAC_LAMBDA_LIST = "macro's lambda list" # one form
LET_LIST = "let list"   # one form
DO_VAR_LIST = "do vars list"    # one form
DO_TEST_RES_LIST = "do test result list"    # one form
BODY_BLOCK = "body block"   # many forms
MAC_BODY_BLOCK = "mac body block"   # many forms
FUN_BODY_BLOCK = "function body block"   # many forms
OPER_EXPR = "operator expression"   # one form
OPER_EXPR_IN_BRACK = "operator expression in round brackets"   # one form
MULT_OPER_EXPR_IN_BRACK = "multiple operator expressions in round brackets"   # one form
STRUCT_SLOTS = "structure slots definitions"
STRUCT_OPTIONS = "structure's options"
CLASS_SLOTS_LIST = "list with class slots definitions"
CLASS_OPTIONS = "class' options"
METH_QUALIF = "method qualifier - :after, :before or :around"
# TL_BLOCK gives descriptions of each special TwinLisp language constract;
#  - keys are special words that start their respective TL_BLOCK's
TL_BLOCK = {"def": ([FUN_NAME, (LAMBDA_LIST, OPTIONAL), FUN_BODY_BLOCK],
                    ["defun",0,1,2]),
            "lambda": ([(LAMBDA_LIST, OPTIONAL), BODY_BLOCK],
                       ["lambda",0,1]),
            "mac": ([NAME2, (MAC_LAMBDA_LIST, OPTIONAL), MAC_BODY_BLOCK],
                    ["defmacro",0,1,2]),
            "block": ([(NAME2, OPTIONAL), BODY_BLOCK],
                      ["block",0,1]),
            "catch": ([NAME2, BODY_BLOCK],
                      ["catch",0,1]),
            "throw": ([NAME, (OPER_EXPR, OPTIONAL)],
                      ["throw",0,1]),
            "let": ([(LET_LIST, OPTIONAL), BODY_BLOCK],
                    ["let",0,1]),
            "lets": ([(LET_LIST, OPTIONAL), BODY_BLOCK],
                     ["let*",0,1]),
            "prog": ([(LET_LIST, OPTIONAL), BODY_BLOCK],
                     ["prog",0,1]),
            "progs": ([(LET_LIST, OPTIONAL), BODY_BLOCK],
                      ["prog*",0,1]),
            "do": ([DO_VAR_LIST, (DO_TEST_RES_LIST, OPTIONAL), BODY_BLOCK],
                   ["do",0,1,2]),
            "dos": ([DO_VAR_LIST, (DO_TEST_RES_LIST, OPTIONAL), BODY_BLOCK],
                    ["do*",0,1,2]),
            "for": ([DO_VAR_LIST, (DO_TEST_RES_LIST, OPTIONAL), BODY_BLOCK],
                    ["tl-for",0,1,2]),
            "flet": ([([FUN_NAME, (LAMBDA_LIST, OPTIONAL), FUN_BODY_BLOCK], OPTIONAL, MULT), BODY_BLOCK],
                     ["flet",[(0,OPTIONAL,MULT,[0,1,2])],1]),
            "labels": ([([FUN_NAME, (LAMBDA_LIST, OPTIONAL), FUN_BODY_BLOCK], OPTIONAL, MULT), BODY_BLOCK],
                       ["labels",[(0,OPTIONAL,MULT,[0,1,2])],1]),
            "maclet": ([([NAME2, (MAC_LAMBDA_LIST, OPTIONAL), MAC_BODY_BLOCK], OPTIONAL, MULT),
                          MAC_BODY_BLOCK],
                       ["macrolet",[(0,OPTIONAL,MULT,[0,1,2])],1]),
            "if": ([OPER_EXPR_IN_BRACK, BODY_BLOCK,
                    (["elif", OPER_EXPR_IN_BRACK, BODY_BLOCK], OPTIONAL, MULT),
                    (["else", BODY_BLOCK], OPTIONAL)],
                   ["cond",[0,1],(2,MULT,OPTIONAL,[0,1]),(3,OPTIONAL,["t",0])]),
            "case": ([OPER_EXPR_IN_BRACK,
                      (["is", MULT_OPER_EXPR_IN_BRACK, BODY_BLOCK], OPTIONAL, MULT),
                      (["else", BODY_BLOCK], OPTIONAL)],
                     ["tl-case",0,(2,OPTIONAL,[0],"nil"),(1,MULT,OPTIONAL,[0,1])]),
            "comcase": ([OPER_EXPR_IN_BRACK,
                      (["is", MULT_OPER_EXPR_IN_BRACK, BODY_BLOCK], OPTIONAL, MULT)],
                     ["case",0,(1,MULT,OPTIONAL,[0,1])]),
            "typecase": ([OPER_EXPR_IN_BRACK,
                          (["is", OPER_EXPR_IN_BRACK, BODY_BLOCK], OPTIONAL, MULT)],
                         ["typecase",0,(1,MULT,OPTIONAL,[0,1])]),
            "return": ([FUN_NAME_FROM_LEVEL, (["from", NAME], OPTIONAL), (OPER_EXPR, OPTIONAL)],
                       ["return-from",(1,OPTIONAL,0,0),2]),
            "break": ([(["from", NAME], OPTIONAL), (OPER_EXPR, OPTIONAL)],
                      ["return-from",(0,OPTIONAL,0,"nil"),1]),
            "struct": ([NAME2, STRUCT_SLOTS, (["options", STRUCT_OPTIONS], OPTIONAL)],
                       ["defstruct",[0,(2,OPTIONAL,0)],1]),
            "class": ([NAME2, (LET_LIST, OPTIONAL), CLASS_SLOTS_LIST,
                       (["options", CLASS_OPTIONS], OPTIONAL)],
                      ["defclass",0,1,2,(3,OPTIONAL,0)]),
            "cond": ([NAME2, (LET_LIST, OPTIONAL), CLASS_SLOTS_LIST,
                      (["options", CLASS_OPTIONS], OPTIONAL)],
                     ["define-condition",0,1,2,(3,OPTIONAL,0)]),
            "meth": ([FUN_NAME, (METH_QUALIF, OPTIONAL), (LAMBDA_LIST, OPTIONAL), FUN_BODY_BLOCK],
                     ["defmethod",0,1,2,3]),
            "package": ([NAME2, (STRUCT_SLOTS, OPTIONAL)],
                        ["defpackage",0,1]),
            "inside": ([NAME2],
                       ["in-package",0]),
            "try": ([BODY_BLOCK, ["finally", BODY_BLOCK]],
                    ["unwind-protect",["progn",0],(1,0)]),
            "restart": ([BODY_BLOCK, (["at", (NAME2, OPTIONAL), (LAMBDA_LIST, OPTIONAL), BODY_BLOCK],
                                      OPTIONAL, MULT)],
                        ["restart-case",["progn",0],(1,MULT,OPTIONAL,[0,1,2])]),
            "handle": ([BODY_BLOCK, (["cond", NAME2, (LET_LIST, OPTIONAL), BODY_BLOCK], OPTIONAL, MULT)],
                       ["handler-case",["progn",0],(1,MULT,OPTIONAL,[0,1,2])])}


# SPEC_SYMB is used in string reading to mark elements
SPEC_SYMB = []
for symbList in (OPER_SYMB,TL_BLOCK.keys(),AUX_SPEC_SYMB,TL_DIRECT_SPEC_SYMB):
    SPEC_SYMB.extend(symbList)
