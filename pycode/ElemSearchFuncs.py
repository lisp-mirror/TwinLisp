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

from Const import *


def getElemsInBrackets(indOpenBr,elems,retWithBrackets=False):
    expClosBr = [BRACKETS[elems[indOpenBr].type]]
    numOpenBr = 0
    ind = elems.growOnIndex(indOpenBr+1)
    while ind<len(elems):
        el = elems[ind]
        if BRACKETS.has_key(el.type):
            # it is an openning bracket
            numOpenBr = numOpenBr+1
            expClosBr.append(BRACKETS[el.type])
        else:
            if CLOSING_BRACKETS.count(el.type)!=0:
                # it is a closing bracket, but is it a correct one?
                if el.type==expClosBr[-1]:
                    numOpenBr = numOpenBr-1
                    expClosBr.pop()
                    if numOpenBr<0:
                        indClosBr = ind
                        break
                else:
                    raise SyntaxError, "Expect closing bracket '%s' on line %d, position %d, but got '%s' instead" % (expClosBr[-1],el.lineNum,el.start,el.type)
        ind = elems.growOnIndex(ind+1)
    else:
        raise SyntaxError, "Expected closing bracket to match '%s' on line %d, position %d, is missing" % (elems[indOpenBr].type,elems[indOpenBr].lineNum,elems[indOpenBr].start)
    if retWithBrackets:
        return elems[indOpenBr:indClosBr+1], indClosBr+1
    else:
        return elems[indOpenBr+1:indClosBr], indClosBr


def _getLineEndElemInd(startInd,elems):
    """Return the first line end element, or None"""
    for ind in xrange(startInd,len(elems)):
        if elems[ind].type==StrElem.LINE_END_TYPE:
            return True, ind
    return False, ind


def skipElems(elemTypes,startInd,elems,onSameLine=True):
    """Seeks index of the first element other then the ones that have to be skipped. If found, returns True and index, else False and len(elems)-1."""
    ind = startInd
    while ind<len(elems):
        elType = elems[ind].type
        if (elType==StrElem.LINE_END_TYPE):
            if onSameLine: break
        elif elType=="\\":
            lineEndFound, ind = _getLineEndElemInd(ind,elems)
            if not lineEndFound: return False, len(elems)
        elif elemTypes.count(elType)==0:
            return True, ind
        ind = elems.growOnIndex(ind+1)
    return False, ind


def getRequiredElemInd(elemType,startInd,elems,onSameLine=True):
    """Required element shall always be on the same line (or continued line)"""
    elemFound, ind = skipElems([StrElem.WHITE_TYPE],startInd,elems,onSameLine)
    if not elemFound:
        if onSameLine:
            raise SyntaxError, "Expect element '%s' on line %d, but line ends" % (elemType,elems[startInd].lineNum)
        else:
            if startInd<len(elems):
                raise SyntaxError, "Expected element '%s' is missing on/after line %d" % (elemType,elems[startInd].lineNum)
            else:
                raise SyntaxError, "Expected element '%s' is missing" % elemType
    if elems[ind].type==elemType:
        return ind
    else:
        raise SyntaxError, "Expected element '%s', but got instead element '%s' on line %d" % (elemType,elems[ind].type,elems[ind].lineNum)


def getRequiredElemInd2(elemType,startInd,elems,onSameLine=True):
    try:
        return True, getRequiredElemInd(elemType,startInd,elems,onSameLine)
    except SyntaxError:
        return False, startInd


def getShortcutInd(startInd,elems,onSameLine=True):
    for elemType in SHORTCUT_OPERS.keys():
        elemFound, ind = getRequiredElemInd2(elemType,startInd,elems,onSameLine)
        if elemFound: return True, ind
    return False, startInd


def getElemIndInOperExpr(elemType,startInd,elems):
    ind = startInd
    while ind<len(elems):
        elemFound, ind = skipElems([StrElem.WHITE_TYPE],ind,elems)
        if not elemFound: break
        if elems[ind].type==elemType:
            return True, ind
        elif BRACKETS.has_key(elems[ind].type):
            elemsInBrack, ind = getElemsInBrackets(ind,elems,True)
        elif (elems[ind].type==elems[ind].LINE_END_TYPE) or (elems[ind].type==","):
            break
        else:
            ind = ind+1
    return False, None


