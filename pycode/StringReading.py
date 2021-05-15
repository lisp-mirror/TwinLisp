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

import re, types
from Const import *

# PHASE's are phases of string reading
REG_PHASE = "regular-code"
STRING_PHASE = "string-chars"
CLISP_PHASE = "common-lisp-code"

# precompiled regular expressions
_NON_WHITE_RE = re.compile(r"\S+")
_WHITE_RE = re.compile(r"\s+")
_ALPHA_NUM_RE = re.compile(r"\w+")
_CLISP_START_RE = re.compile(CLISP_START_STRING)
_CLISP_END_RE = re.compile(CLISP_END_STRING)
_ONE_DIGIT_RE = re.compile(r"[0-9]")
_INTEGER_RE = re.compile(r"[0-9]+\.?")
_RATIO_RE = re.compile(r"[0-9]+/[0-9]+")
_FLOAT_SIMP_RE = re.compile(r"[0-9]*\.[0-9]+")
_FLOAT_EXP_RE = re.compile(r"[0-9]+\.?[0-9]*[esfdlESFDL][+\-]?[0-9]+")
_FLOAT_DOT_EXP_RE = re.compile(r"\.[0-9]+[esfdlESFDL][+\-]?[0-9]+")


def _stripEndLineChar(originalString):
    st = originalString
    endOfLineChar = ""
    if len(st)>0:
        if st[-1]=="\n":
            # this is unix or win
            st = st[0:len(st)-1]
            endOfLineChar = "\n"
            if len(st)>0:
                if st[-1]=="\r":
                    # this is win
                    st = st[0:len(st)-1]
                    endOfLineChar = "\r\n"
        elif st[-1]=="\r":
            # this is mac
            st = st[0:len(st)-1]
            endOfLineChar = "\r"
    return st, endOfLineChar

def _startStringPhase(st,strNum,startIndex,marks):
    marks.append(StrElem(StrElem.STR_START_TYPE,"\"",strNum,
                         startIndex,startIndex+1))
    return startIndex+1, STRING_PHASE
    
def _findEndOfExprInStr(st,startIndex,termChars):
    """
    Expressions are expected to end by any symbol in termChars. If the first
    return parameter is True, then expression was terminated correctly. If
    it is False, then the end of the line was reached.
    """
    end = startIndex
    while end<len(st):
        ch = st[end]
        if ch in termChars:
            return True, end
        elif ch=="\\":
            if (end+1)<len(st):
                # whatever next char is, take it
                end = end+2
            else:
                end = end+1
        else:
            end = end+1
    return False, end

def _findEndOfExpr(st,startIndex,termChars):
    """
    Symbol is terminated by one of termChars, of the end of line.
    """
    endingInside, end = _findEndOfExprInStr(st,startIndex,termChars)
    if not endingInside:
        if len(st)>0:
            if st[-1]=="\\":
                end = end-1
    return end

def _procStringPhase(initStr,strNum,startIndex,marks,endOfLineChar):
    st = initStr
    endingInside, end = _findEndOfExprInStr(st,startIndex,("\"",))
    if endingInside:
        end = end+1  # include ending quote
        elemType = StrElem.STR_END_TYPE
        phase = REG_PHASE
    else:
        elemType = StrElem.STR_MID_TYPE
        phase = STRING_PHASE
        st = st+endOfLineChar
        end = len(st)
    marks.append(StrElem(elemType,st[startIndex:end],strNum,
                         startIndex,end))
    return st, end, phase

def _procCLispPhase(st,strNum,startIndex,marks,endOfLineChar):
    match = _CLISP_END_RE.search(st,startIndex)
    if match is None:
        end = len(st)
        codeEnd = end
        phase = CLISP_PHASE
        elemType = StrElem.CLISP_MID_TYPE
    else:
        codeEnd = match.start()
        end = codeEnd+len(CLISP_END_STRING)
        phase = REG_PHASE
        elemType = StrElem.CLISP_END_TYPE
    marks.append(StrElem(elemType,st[startIndex:codeEnd]+endOfLineChar,
                         strNum,startIndex,end))
    return end, phase

def _procAmpName(st,strNum,startIndex,marks):
    # how long is a symbol?
    end = _findEndOfExpr(st,startIndex+1,(" ", "\t", "(", ")", ",", ":"))
    if end==startIndex+1:
        # it is a lone operator &
        marks.append(StrElem("&","&",strNum,startIndex,startIndex+1))
        end = startIndex+1
    else:
        marks.append(StrElem(StrElem.SYMB_TYPE,st[startIndex+1:end],strNum,
                             startIndex+1,end))
    return end

def _OperLen(st,startIndex):
    spChar = st[startIndex]
    highestLenOper = None
    if MULTI_CHAR_OPERS.has_key(spChar):
        for oper in MULTI_CHAR_OPERS[spChar]:
            if st[startIndex:startIndex+len(oper)]==oper:
                if highestLenOper is None:
                    highestLenOper = oper
                else:
                    if len(highestLenOper)<len(oper):
                        highestLenOper = oper
    if highestLenOper is None:
        return 1
    else:
        return len(highestLenOper)

def _procSpecialChars(st,strNum,startIndex,marks):
    end = startIndex + _OperLen(st,startIndex)
    marks.append(StrElem(st[startIndex:end],st[startIndex:end],strNum,
                         startIndex,end))
    return end

def _procSpecSynt(st,strNum,startIndex,nonWhiteEnd,marks):
    operLen = _OperLen(st,startIndex)
    if operLen>1:
        end = startIndex + operLen
        elemType = st[startIndex:end]
    elif (startIndex+1)<len(st):
        end = _findEndOfExpr(st,startIndex+1,(" ", "\t", "(", ")", ","))
        if end==(startIndex+1):
            raise SyntaxError, "Empty #-y structure"
        elemType = StrElem.SYNT_STRUCT_TYPE
    else:
        raise SyntaxError, "Empty #-y structure"
    marks.append(StrElem(elemType,st[startIndex:end],strNum,startIndex,end))
    return end

def _procDotOrNum(st,strNum,startIndex,marks):
    match = _FLOAT_SIMP_RE.match(st,startIndex)
    if match is None:
        # this a dot operator
        end = startIndex+1
        elemType = "."
    else:
        # this is a float number, like .34, or .34e-4, but which one?
        simpleFloatEnd = match.end()
        match = _FLOAT_DOT_EXP_RE.match(st,startIndex)
        if match is None:
            # this is a simple style float, like .34
            end = simpleFloatEnd
        else:
            # this is exp style float, like .34e-4
            end = match.end()
        elemType = StrElem.NUM_TYPE
    marks.append(StrElem(elemType,st[startIndex:end],strNum,startIndex,end))
    return end

def _procNum(st,strNum,startIndex,marks):
    # 1 check if it is a float in exp form
    match = _FLOAT_EXP_RE.match(st,startIndex)
    if match is not None:
        end = match.end()
    else:
        # 2 check if it is a float in simple form
        match = _FLOAT_SIMP_RE.match(st,startIndex)
        if match is not None:
            end = match.end()
        else:
            # 3 check if it is a ratio
            match = _RATIO_RE.match(st,startIndex)
            if match is not None:
                end = match.end()
            else:
                # 4 cut out an integer
                end = _INTEGER_RE.match(st,startIndex).end()
    marks.append(StrElem(StrElem.NUM_TYPE,st[startIndex:end],strNum,
                         startIndex,end))
    return end

def markElemsInStr(originalString,strNum,initPhase=REG_PHASE):
    marks = []
    phase = initPhase
    st, endOfLineChar = _stripEndLineChar(originalString)
    # work with st, which now has no new line character(s) at the end
    startIndex = 0
    while startIndex<len(st):
        if phase==STRING_PHASE:
            st, startIndex, phase = _procStringPhase(st,strNum,startIndex,marks,
                                                     endOfLineChar)
        elif phase==CLISP_PHASE:
            startIndex, phase = _procCLispPhase(st,strNum,startIndex,marks,
                                                endOfLineChar)
        elif phase==REG_PHASE:
            match = _WHITE_RE.match(st,startIndex)
            if match is not None:
                marks.append(StrElem(StrElem.WHITE_TYPE,None,strNum,
                                     startIndex,match.end()))
                startIndex = match.end()
                continue
            match = _NON_WHITE_RE.match(st,startIndex)
            nonWhiteEnd = match.end()
            match = _ALPHA_NUM_RE.match(st,startIndex,nonWhiteEnd)
            if match is None:
                # have some special charachter (non alpha-num) in the beginning
                spChar = st[startIndex]
                if spChar=="&":
                    startIndex = _procAmpName(st,strNum,startIndex,marks)
                elif spChar=="#":
                    startIndex = _procSpecSynt(st,strNum,startIndex,
                                               nonWhiteEnd,marks)
                elif spChar==".":
                    startIndex = _procDotOrNum(st,strNum,startIndex,marks)
                elif spChar=="\"":
                    startIndex, phase =_startStringPhase(st,strNum,
                                                         startIndex,marks)
                elif spChar==";":
                    # semicolomn starts comment, which extends till the end
                    marks.append(StrElem(StrElem.COMM_TYPE,
                                         st[startIndex:len(st)],strNum,
                                         startIndex,len(st)))
                    startIndex = len(st)
                else:
                    startIndex = _procSpecialChars(st,strNum,startIndex,marks)
            else:
                # have an alpha-num symbol or a number
                alphaNumEnd = match.end()
                match = _ONE_DIGIT_RE.match(st,startIndex)
                if match is None:
                    match = _CLISP_START_RE.match(st,startIndex)
                    if match is None:
                        # have alpha-numeric symbol
                        symb = st[startIndex:alphaNumEnd]
                        if SPEC_SYMB.count(symb)==0:
                            elType = StrElem.SYMB_TYPE
                        else:
                            if OPER_SYMB.count(symb)==0:
                                elType = StrElem.SPEC_SYMB_TYPE
                            else:
                                elType = symb
                        marks.append(StrElem(elType,symb,strNum,
                                             startIndex,alphaNumEnd))
                        startIndex = alphaNumEnd
                    else:
                        marks.append(StrElem(StrElem.CLISP_START_TYPE,None,strNum,startIndex,None))
                        phase = CLISP_PHASE
                        startIndex = match.end()
                else:
                    # have a number
                    startIndex = _procNum(st,strNum,startIndex,marks)
    if (len(st)==0) and (phase==STRING_PHASE):
        marks.append(StrElem(StrElem.STR_MID_TYPE,endOfLineChar,strNum,0,len(endOfLineChar)))
    marks.append(StrElem(StrElem.LINE_END_TYPE,None,strNum,None,None))
    return marks, phase


class DummyGrowingList(object):
    def __init__(self,elems=[]):
        self.__lineElems = elems
    def __len__(self):
        return len(self.__lineElems)
    def __getitem__(self,index):
        if type(index)==types.SliceType:
            return DummyGrowingList(self.__lineElems[index])
        return self.__lineElems[index]
    def growOnIndex(self,index):
        return index

class GrowingList(object):
    def __init__(self,fObj):
        self.__f = fObj
        self.__lineNum = 0
        self.__stringPhase = REG_PHASE
        self.__lineElems = []
        # read the first line
        self.__readLine()
    def __readLine(self):
        line = self.__f.readline()
        if len(line)!=0:    # end of file is ""
            self.__lineNum = self.__lineNum+1
            newElems, self.__stringPhase = markElemsInStr(line,self.__lineNum,self.__stringPhase)
            self.__lineElems.extend(newElems)
    def __len__(self):
        return len(self.__lineElems)
    def __getitem__(self,index):
        if type(index)==types.SliceType:
            return DummyGrowingList(self.__lineElems[index])
        return self.__lineElems[index]
    def growOnIndex(self,index):
        if index==len(self):
            self.__readLine()
        return index

