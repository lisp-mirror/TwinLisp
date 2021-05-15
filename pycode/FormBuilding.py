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

import types, copy
from ElemSearchFuncs import *


class LevelInfo(object):
    """ """
    def __init__(self,blockName=None,implScope=False,isTopLevel=True,
                 explScopeWarn=False,nickToRealNames=None):
        self.blockName = blockName
        self.implScope = implScope
        self.explScopeWarn = explScopeWarn
        self.isTopLevel = isTopLevel
        self.__lowerLevelFuncName = None
        if nickToRealNames is None:
            self.__nickToRealNames = copy.copy(TWL_METH_NICKNAMES)
        else:
            self.__nickToRealNames = copy.copy(nickToRealNames)
        self.currImplVar = []
        self.newVars = []
        self.__lowerLevelImplVar = []

    def setLowerLevelFuncName(self,funcName):
        self.__lowerLevelFuncName = funcName

    def lowerFuncLevel(self):
        if self.__lowerLevelFuncName is None:
            raise Exception, "Programming error: function name should be set before calling LevelInfo.lowerFuncLevel"
        funcName = self.__lowerLevelFuncName
        self.__lowerLevelFuncName = None
        lowerLevel = self.lowerMacLevel()
        lowerLevel.blockName = funcName
        lowerLevel.implScope = self.implScope
        return lowerLevel

    def lowerRegLevel(self):
        lowerLevel = LevelInfo(blockName=self.blockName,
                               implScope=self.implScope,
                               isTopLevel=False,
                               explScopeWarn=self.explScopeWarn,
                               nickToRealNames=self.__nickToRealNames)
        lowerLevel.currImplVar = self.__lowerLevelImplVar + self.currImplVar
        self.__lowerLevelImplVar = []
        return lowerLevel

    def lowerMacLevel(self):
        lowerLevel = LevelInfo(blockName=self.blockName,
                               implScope=False,
                               isTopLevel=False,
                               explScopeWarn=self.explScopeWarn,
                               nickToRealNames=self.__nickToRealNames)
        lowerLevel.currImplVar = self.__lowerLevelImplVar
        self.__lowerLevelImplVar = []
        return lowerLevel

    def addSymbSynonym(self,nickName,realName):
        self.__nickToRealNames[nickName] = realName

    def getRealSymbol(self,symb):
        if self.__nickToRealNames.has_key(symb):
            return self.__nickToRealNames[symb]
        else:
            return symb

    def setImplVarForLowerLevel(self,symbList):
        self.__lowerLevelImplVar = symbList


def _formSymbAsImplVarForLowerLevel(symbList,form):
    tf = form
    if tf[0]==SHORTCUT_TYPE:
        tf = form
        while tf[0]==SHORTCUT_TYPE:
            tf = tf[2]
    if tf[0]==ATOM_TYPE:
        symbList.append(tf[1])


def _formSymbAsImplVar(level,form):
    tf = form
    if tf[0]==SHORTCUT_TYPE:
        tf = form
        while tf[0]==SHORTCUT_TYPE:
            tf = tf[2]
    if tf[0]==FORM_TYPE:
        if tf[1][0]==(ATOM_TYPE,"values"):
            for innerForm in tf[1][1:len(tf[1])]:
                _formSymbAsImplVar(level,innerForm)
        return
    if tf[0]==ATOM_TYPE:
        if level.implScope:
            if (level.currImplVar.count(tf[1])==0) and (tf[1].count(":")==0):
                level.currImplVar.append(tf[1])
                level.newVars.append(tf[1])
        else:
            if level.explScopeWarn and (level.currImplVar.count(tf[1])==0):
                raise SyntaxError, "Assignment to unknown variable '%s'. You have to use 'let'-type constructs, or declare variable global." % tf[1]


def _macLambdaListForm(elems,level):
    form = (FORM_TYPE,[])
    symbList = []
    ind = 0
    option = "no-option"
    while ind<len(elems):
        elemFound, ind = skipElems([StrElem.WHITE_TYPE,","],ind,elems,False)
        if not elemFound: break
        if (elems[ind].type==StrElem.SYMB_TYPE) and (MAC_LAMBDA_LIST_OPTIONS.count(elems[ind].value)!=0):
            if (elems[ind].value!="&whole") and (elems[ind].value!="&environment"):
                option = elems[ind].value
            form[1].append((ATOM_TYPE,elems[ind].value))
            ind = ind+1
        elif elems[ind].type==".":
            brackInd = getRequiredElemInd("(",ind+1,elems)
            trueVal, innerLamdaListForm, ind = _procSpecificList(brackInd,elems,level,MAC_LAMBDA_LIST)
            form[1].extend(innerLamdaListForm)
        elif elems[ind].type=="*":
            if (option=="no-option") or (option=="&optional"):
                option = "&rest"
                form[1].append((ATOM_TYPE,"&rest"))
            elif option!="&rest":
                raise SyntaxError, "The '&rest' parameter on line %d, position %d, cannot follow option '%s'" % (elems[ind].lineNum,elems[ind].start,option)
            restForm, ind = getOneForm(ind+1,elems,level,False)
            form[1].append(restForm)
        elif elems[ind].type=="**":
            if (option=="no-option") or (option=="&optional"):
                option = "&rest"
                form[1].append((ATOM_TYPE,"&body"))
            elif option!="&rest":
                raise SyntaxError, "The '&body' parameter on line %d, position %d, cannot follow option '%s'" % (elems[ind].lineNum,elems[ind].start,option)
            restForm, ind = getOneForm(ind+1,elems,level,False)
            form[1].append(restForm)
        else:
            keyPresent, arrowInd = getElemIndInOperExpr("->",ind,elems)
            if keyPresent:
                keyForm, keyFormEnd = getOneForm(0,elems[ind:arrowInd],level,False)
                if keyForm is None: raise SyntaxError, "Missing a keyword before '->' on line %d, position %d" % (elems[arrowInd].lineNum,elems[arrowInd].start)
                if (option=="no-option") or (option=="&optional") or (option=="&rest"):
                    option = "&key"
                    form[1].append((ATOM_TYPE,"&key"))
                elif option!="&key":
                    raise SyntaxError, "The '&key' parameter on line %d, position %d, cannot follow option '%s'" % (elems[ind].lineNum,elems[ind].start,option)
                svarPresent, questInd = getElemIndInOperExpr("=?",arrowInd+1,elems)
            else:
                svarPresent, questInd = getElemIndInOperExpr("=?",ind,elems)
            if svarPresent:
                svarForm, svarFormEnd = getOneForm(questInd+1,elems,level,False)
                if svarForm is None: raise SyntaxError, "Missing a variable name after '=?' on line %d, position %d" % (elems[questInd].lineNum,elems[questInd].start)
                if option=="no-option":
                    option = "&optional"
                    form[1].append((ATOM_TYPE,"&optional"))
                elif option=="&rest":
                    option = "&key"
                    form[1].append((ATOM_TYPE,"&key"))
                elif (option!="&optional") and (option!="&key"):
                    raise SyntaxError, "'=?' on line %d, position %d, has no sense after option '%s'" % (elems[questInd].lineNum,elems[questInd].start,option)
            if keyPresent and svarPresent:
                varForms, varFormsEnd = getFormsSeparByElem("=",0,elems[arrowInd+1:questInd],level)
                _formSymbAsImplVarForLowerLevel(symbList,varForms[0])
                ind = svarFormEnd
                if len(varForms)==1:
                    form[1].append((FORM_TYPE,[(FORM_TYPE,[keyForm,varForms[0]]),
                                               (ATOM_TYPE,LISP_NIL),svarForm]))
                elif len(varForms)==2:
                    form[1].append((FORM_TYPE,[(FORM_TYPE,[keyForm,varForms[0]]),
                                               varForms[1],svarForm]))
            elif (not keyPresent) and svarPresent:
                varForms, varFormsEnd = getFormsSeparByElem("=",0,elems[ind:questInd],level)
                _formSymbAsImplVarForLowerLevel(symbList,varForms[0])
                ind = svarFormEnd
                if len(varForms)==1:
                    form[1].append((FORM_TYPE,[varForms[0],(ATOM_TYPE,LISP_NIL),svarForm]))
                elif len(varForms)==2:
                    form[1].append((FORM_TYPE,[varForms[0],varForms[1],svarForm]))
            elif keyPresent and (not svarPresent):
                varForms, ind = getFormsSeparByElem("=",arrowInd+1,elems,level)
                if len(varForms)==1:
                    form[1].append((FORM_TYPE,[(FORM_TYPE,[keyForm,varForms[0]])]))
                elif len(varForms)==2:
                    form[1].append((FORM_TYPE,[(FORM_TYPE,[keyForm,varForms[0]]),
                                               varForms[1]]))
            elif (not keyPresent) and (not svarPresent):
                varForms, ind = getFormsSeparByElem("=",ind,elems,level)
                _formSymbAsImplVarForLowerLevel(symbList,varForms[0])
                if len(varForms)==1:
                    form[1].append(varForms[0])
                elif len(varForms)==2:
                    if option=="no-option":
                        option = "&optional"
                        form[1].append((ATOM_TYPE,"&optional"))
                    elif option=="&rest":
                        option = "&key"
                        form[1].append((ATOM_TYPE,"&key"))
                    elif option=="&allow-other-keys":
                        option = "&aux"
                        form[1].append((ATOM_TYPE,"&aux"))
                    form[1].append((FORM_TYPE,[varForms[0],varForms[1]]))
    level.setImplVarForLowerLevel(symbList)
    return form


def _letListForm(innerElems,level):
    form = (FORM_TYPE,[])
    symbList = []
    ind = 0
    while ind<len(innerElems):
        forms, ind = getFormsSeparByElem("=",ind,innerElems,level)
        _formSymbAsImplVarForLowerLevel(symbList,forms[0])
        if len(forms)==2:
            form[1].append((FORM_TYPE,[forms[0],forms[1]]))
        elif len(forms)==1:
            form[1].append(forms[0])
        elemFound, ind = skipElems([StrElem.WHITE_TYPE,","],ind,innerElems,False)
        if not elemFound: break
    level.setImplVarForLowerLevel(symbList)
    return form


def _doVarListForm(innerElems,level):
    form = (FORM_TYPE,[])
    symbList = []
    ind = 0
    while ind<len(innerElems):
        stepForm, arrowInd, end = getFormAfterElem("->",ind,innerElems,level)
        if stepForm is None:
            forms, end = getFormsSeparByElem("=",ind,innerElems,level)
            _formSymbAsImplVarForLowerLevel(symbList,forms[0])
            if len(forms)==2:
                form[1].append((FORM_TYPE,[forms[0],forms[1]]))
            elif len(forms)==1:
                form[1].append(forms[0])
        else:
            forms, irrelevantEnd = getFormsSeparByElem("=",0,innerElems[ind:arrowInd],level)
            if len(forms)==2:
                form[1].append((FORM_TYPE,[forms[0],forms[1],stepForm]))
            elif len(forms)==1:
                form[1].append((FORM_TYPE,[forms[0],(ATOM_TYPE,LISP_NIL),stepForm]))
        elemFound, ind = skipElems([StrElem.WHITE_TYPE,","],end,innerElems,False)
        if not elemFound: break
    level.setImplVarForLowerLevel(symbList)
    return form


def _procName(start,elems,level,onSameLine):
    elemFound, ind = getRequiredElemInd2(StrElem.SYMB_TYPE,start,elems,onSameLine)
    if elemFound:
        return True, [(ATOM_TYPE,level.getRealSymbol(elems[ind].value))], ind+1
    elemFound, ind = getShortcutInd(start,elems,onSameLine)
    if elemFound:
        while elemFound:
            elemFound, ind = getShortcutInd(ind+1,elems)
        ind = getRequiredElemInd(StrElem.SYMB_TYPE,ind,elems)
        elems[ind].value = level.getRealSymbol(elems[ind].value)
        form, irrelevantEnd = getOneForm(0,elems[start:ind+1],level,False)
        return True, [form], ind+1
    elemFound, ind = getRequiredElemInd2(StrElem.STR_START_TYPE,start,elems,onSameLine)
    if elemFound:
        strAtom, end = getStringAtom(ind,elems)
        return True, [strAtom], end
    elemFound, ind = getRequiredElemInd2(":",start,elems,onSameLine)
    if elemFound:
        ind = getRequiredElemInd(StrElem.SYMB_TYPE,ind+1,elems)
        return True, [(ATOM_TYPE,":"+elems[ind].value)], ind+1
    return False, [(ATOM_TYPE,LISP_NIL)], start


def procName(start,elems,level,addLineNums):
    return _procName(start,elems,level,True)

def procName2(start,elems,level,addLineNums):
    return _procName(start,elems,level,False)

def procFunName(start,elems,level,addLineNums):
    elemFound, ind = getRequiredElemInd2(StrElem.SPEC_SYMB_TYPE,start,elems,False)
    if elemFound and (elems[ind].value==SETTER_SPEC_SYMB):
        isSetter = True
        ind = ind+1
    else:
        isSetter = False
    succ, formList, end = _procName(ind,elems,level,False)
    level.setLowerLevelFuncName(formList[0][1])
    if isSetter:
        return succ, [(FORM_TYPE,[(ATOM_TYPE,SETTER_FUNC),formList[0]])], end
    else:
        return succ, formList, end

def procFunNameFromLevelInfo(start,elems,level,addLineNums):
    funcName = level.blockName
    if funcName is None:
        if start<len(elems):
             errorLineNum = elems[start].lineNum
        else:
            if len(elems)==0:
                raise SyntaxError, "Function name is underfined"
            else:
                errorLineNum = elems[-1].lineNum
        raise SyntaxError, "Function name on line %d is underfined" % errorLineNum
    else:
        return True, [(ATOM_TYPE,funcName)], start


def procDoTestResultList(start,elems,level,addLineNums):
    try:
        ind = getRequiredElemInd("(",start,elems,False)
    except SyntaxError:
        return False, [(FORM_TYPE,[(ATOM_TYPE,LISP_NIL)])], start
    innerElems, ind = getElemsInBrackets(ind,elems)
    forms = getForms(innerElems,level,addLineNums)
    if len(forms)==0:
        forms = [(ATOM_TYPE,LISP_NIL)]
    return True, [(FORM_TYPE,forms)], ind+1


def procOperExpr(start,elems,level,addLineNums):
    form, end = getOneForm(start,elems,level,False)
    if form is None:
        return False, [(FORM_TYPE,[])], start
    else:
        return True, [form], end


def _operExprInBrack(start,elems,level,addLineNums,singleExpr):
    try:
        brackInd = getRequiredElemInd("(",start,elems)
    except SyntaxError:
        return False, [(FORM_TYPE,[])], start
    innerElems, ind = getElemsInBrackets(brackInd,elems)
    forms = getForms(innerElems,level,addLineNums)
    if len(forms)==0:
        raise SyntaxError, "Missing form(s) in brackets, starting line %d, position %d" % (elems[brackInd].lineNum,elems[brackInd].start)
    elif singleExpr and (len(forms)>1):
        raise SyntaxError, "Expect one form in brackets, starting line %d, position %d, but got %d forms" % (elems[brackInd].lineNum,elems[brackInd].start,len(forms))
    return True, forms, ind+1


def procOperExprInBrack(start,elems,level,addLineNums):
    return _operExprInBrack(start,elems,level,addLineNums,True)


def procMultOperExprInBrack(start,elems,level,addLineNums):
    partFound, newForms, end = _operExprInBrack(start,elems,level,addLineNums,False)
    if len(newForms)==1:
        return partFound, newForms, end
    else:
        return partFound, [(FORM_TYPE,newForms)], end


def _procSpecificList(start,elems,level,listType):
    try:
        ind = getRequiredElemInd("(",start,elems,False)
    except SyntaxError:
        return False, [(FORM_TYPE,[])], start
    innerElems, ind = getElemsInBrackets(ind,elems)
    if (listType==LAMBDA_LIST) or (listType==MAC_LAMBDA_LIST):
        form = _macLambdaListForm(innerElems,level)
    elif listType==LET_LIST:
        form = _letListForm(innerElems,level)
    elif listType==DO_VAR_LIST:
        form = _doVarListForm(innerElems,level)
    return True, [form], ind+1


def procDoVarList(start,elems,level,addLineNums):
    return _procSpecificList(start,elems,level,DO_VAR_LIST)

def procLetList(start,elems,level,addLineNums):
    return _procSpecificList(start,elems,level,LET_LIST)

def procLambdaList(start,elems,level,addLineNums):
    return _procSpecificList(start,elems,level,LAMBDA_LIST)

def procMacLambdaList(start,elems,level,addLineNums):
    return _procSpecificList(start,elems,level,MAC_LAMBDA_LIST)


def _procBlock(start,elems,level,addLineNums):
    try:
        ind = getRequiredElemInd("{",start,elems,False)
    except SyntaxError, er:
        return False, [], start
    innerElems, ind = getElemsInBrackets(ind,elems)
    return True, getForms(innerElems,level,addLineNums), ind+1

def procBodyBlock(start,elems,level,addLineNums):
    return _procBlock(start,elems,level.lowerRegLevel(),addLineNums)

def procMacBodyBlock(start,elems,level,addLineNums):
    return _procBlock(start,elems,level.lowerMacLevel(),addLineNums)

def procFunBodyBlock(start,elems,level,addLineNums):
    return _procBlock(start,elems,level.lowerFuncLevel(),addLineNums)


def _letLikeElemsInBraces(start,elems,level):
    try:
        ind = getRequiredElemInd("{",start,elems,False)
    except SyntaxError, er:
        return False, [], start
    innerElems, end = getElemsInBrackets(ind,elems)
    return True, _letListForm(innerElems,LevelInfo())[1], end+1

def procClassOptions(start,elems,level,addLineNums):
    return _letLikeElemsInBraces(start,elems,level)

def procStructOptions(start,elems,level,addLineNums):
    return _letLikeElemsInBraces(start,elems,level)


def _funCallLikeElemsInBraces(start,elems,level,slotNameAtom):
    try:
        ind = getRequiredElemInd("{",start,elems,False)
    except SyntaxError, er:
        return False, [], start
    form, end = funcCall(ind,elems,level,slotNameAtom)
    return True, form[1], end

def procClassSlotsList(start,elems,level,addLineNums):
    form = (FORM_TYPE,[])
    try:
        brackInd = getRequiredElemInd("{",start,elems,False)
    except SyntaxError, er:
        return False, [form], start
    innerElems, end = getElemsInBrackets(brackInd,elems)
    ind = 0
    while ind<len(innerElems):
        slPresent, slName, ind = _procName(ind,innerElems,level,False)
        if slPresent:
            optPresent, optForms, ind = _funCallLikeElemsInBraces(ind,innerElems,level,slName[0])
            if optPresent:
                form[1].append((FORM_TYPE,optForms))
            else:
                form[1].append(slName[0])
        else:
            elemFound, ind = skipElems([StrElem.WHITE_TYPE,StrElem.COMM_TYPE,","],ind,innerElems,False)
            if not elemFound: break
    return True, [form], end+1

def procStructSlots(start,elems,level,addLineNums):
    strPres, form, end = procClassSlotsList(start,elems,level,addLineNums)
    return strPres, form[0][1], end


def procMethQualif(start,elems,level,addLineNums):
    elemFound, ind = getRequiredElemInd2(":",start,elems,False)
    if elemFound:
        elemFound, ind = getRequiredElemInd2(StrElem.SYMB_TYPE,ind+1,elems)
        if elemFound:
            return True, [(ATOM_TYPE,":"+elems[ind].value)], ind+1
    return False, [], start


BLOCK_FUNCS = {FUN_NAME: procFunName,
               NAME: procName,
               NAME2: procName2,
               FUN_NAME_FROM_LEVEL: procFunNameFromLevelInfo,
               LAMBDA_LIST: procLambdaList,
               MAC_LAMBDA_LIST: procMacLambdaList,
               MAC_BODY_BLOCK: procMacBodyBlock,
               FUN_BODY_BLOCK: procFunBodyBlock,
               BODY_BLOCK: procBodyBlock,
               LET_LIST: procLetList,
               DO_VAR_LIST: procDoVarList,
               DO_TEST_RES_LIST: procDoTestResultList,
               OPER_EXPR: procOperExpr,
               OPER_EXPR_IN_BRACK: procOperExprInBrack,
               MULT_OPER_EXPR_IN_BRACK: procMultOperExprInBrack,
               STRUCT_SLOTS: procStructSlots,
               STRUCT_OPTIONS: procStructOptions,
               CLASS_SLOTS_LIST: procClassSlotsList,
               CLASS_OPTIONS: procClassOptions,
               METH_QUALIF: procMethQualif}


def _isStructPresent(part,start,elems):
    if type(part[0])!=types.StringType:
        raise Exception, "Programming error: inner forms' descriptions in TL_BLOCK should start from either AUX_SPEC_SYMB or block structure symbol; instead got: "+part.__str__()
    if AUX_SPEC_SYMB.count(part[0])==0:
        try:
            # level info object here should be dummy
            partFound, newForms, ind = BLOCK_FUNCS[part[0]](start,elems,LevelInfo(),False)
        except KeyError:
            raise NotImplementedError, "Handling of block structure '%s' is not implemented." % part
        return partFound, start, part
    else:
        try:
            ind = getRequiredElemInd(StrElem.SPEC_SYMB_TYPE,start,elems,False)
            if part[0]==elems[ind].value:
                return True, ind+1, part[1:len(part)]
            else:
                return False, start, part
        except SyntaxError:
            return False, start, part


def _readBlockStructElems(blockDescr,firstElemInd,elems,level,addLineNums):
    forms = []
    ind = firstElemInd
    for descr in blockDescr:
        isOptional = False
        multiple = False
        if (type(descr)==types.StringType) or (type(descr)==types.ListType):
            part = descr
        elif type(descr)==types.TupleType:
            part = descr[0]
            for opt in descr[1:len(descr)]:
                if opt==OPTIONAL:
                    isOptional = True
                elif opt==MULT:
                    multiple = True
        else:
            raise Exception, "Programming error: wrong element in Const.TL_BLOCK - "+descr.__str__()
        if type(part)==types.StringType:
            try:
                partFound, newForms, ind = BLOCK_FUNCS[part](ind,elems,level,addLineNums)
            except KeyError:
                raise NotImplementedError, "Handling of block structure '%s' is not implemented." % part
            if partFound:
                if multiple:
                    forms.append([newForms])
                    while partFound:
                        partFound, newForms, ind = BLOCK_FUNCS[part](ind,elems,level,addLineNums)
                        if partFound: forms[-1].append(newForms)
                else:
                    forms.append(newForms)
            else:
                if isOptional:
                    forms.append(newForms)
                else:
                    raise SyntaxError, "Required '%s' part of a block structure is missing on line %d" % (part,elems[ind].lineNum)
        elif type(part)==types.ListType:
            partFound, ind, partToRead = _isStructPresent(part,ind,elems)
            if partFound:
                newForms, ind = _readBlockStructElems(partToRead,ind,elems,level,addLineNums)
                if multiple:
                    forms.append([newForms])
                    while True:
                        partFound, ind, partToRead = _isStructPresent(part,ind,elems)
                        if partFound:
                            newForms, ind = _readBlockStructElems(partToRead,ind,elems,level,addLineNums)
                            forms[-1].append(newForms)
                        else:
                            break
                else:
                    forms.append(newForms)
            else:
                if isOptional:
                    forms.append([])
                else:
                    raise SyntaxError, "Required special symbol '%s' is missing on line %d, position %d" % (part[0],elems[ind].lineNum,elems[ind].start)
        else:
            raise Exception, "Programming error: wrong element in Const.TL_BLOCK - "+part.__str__()
    return forms, ind


def _descrProcessing(descr,blockParts):
    if type(descr)==types.StringType:
        return [(ATOM_TYPE,descr)]
    elif type(descr)==types.IntType:
        return blockParts[descr]
    elif type(descr)==types.TupleType:
        isOptional = False
        multiple = False
        partInd = descr[0]
        descrInd = 1
        while True:
            if descr[descrInd]==OPTIONAL:
                isOptional = True
                descrInd = descrInd+1
            elif descr[descrInd]==MULT:
                multiple = True
                descrInd = descrInd+1
            else:
                break
        if len(blockParts[partInd])==0:
            if isOptional:
                if len(descr)<=(descrInd+1):
                    return []
                return _descrProcessing(descr[descrInd+1],blockParts)
            else:
                raise Exception, "Programming error: not optional element is empty in _writeBlockStructForm"
        else:
            if multiple:
                res = []
                for part in blockParts[partInd]:
                    res.extend(_descrProcessing(descr[descrInd],part))
                return res
            else:
                return _descrProcessing(descr[descrInd],blockParts[partInd])
    elif type(descr)==types.ListType:
        return [_writeBlockStructForm(descr,blockParts)]
    else:
        raise Exception, "Programming error: unknown type in form description in TL_BLOCK: "+descrType.__str__()


def _writeBlockStructForm(formDescr,blockParts):
    form = (FORM_TYPE,[])
    for descr in formDescr:
        form[1].extend(_descrProcessing(descr,blockParts))
    return form


def getBlockForm(firstElemInd,elems,level,addLineNums):
    blockName = elems[firstElemInd].value
    blockParts, end = _readBlockStructElems(TL_BLOCK[blockName][0],
                                            firstElemInd+1,elems,level,addLineNums)
    return _writeBlockStructForm(TL_BLOCK[blockName][1],blockParts), end


def getBracketedForm(indOpenBr,elems,level,addLineNums):
    innerElems, indClosBr = getElemsInBrackets(indOpenBr,elems)
    return (FORM_TYPE,getForms(innerElems,level,addLineNums)), indClosBr+1


def getSimpleArrayForm(start,elems,level):
    innerElems, indClosBr = getElemsInBrackets(start,elems)
    form = (FORM_TYPE,[(ATOM_TYPE,MAKE_SIMPLE_ARRAY_FUNC)])
    initElems = getForms(innerElems,level,False)
    if len(initElems)!=0:
        form[1].append((ATOM_TYPE,":initContent"))
        form[1].append((FORM_TYPE,[(ATOM_TYPE,"list")]+initElems))
    return form, indClosBr+1


def getListForm(start,elems,level):
    innerElems, indClosBr = getElemsInBrackets(start,elems)
    form = (FORM_TYPE,[(ATOM_TYPE,MAKE_LIST_FUNC)])
    form[1].extend(getForms(innerElems,level,False))
    return form, indClosBr+1


def getFormAfterElem(elemType,start,elems,level):
    elemFound, separInd = getElemIndInOperExpr(elemType,start,elems)
    if elemFound:
        form, end = getOneForm(separInd+1,elems,level,False)
        if form is None:
            raise SyntaxError, "Missing a form after '%s' on line %d, position %d" % (elems[separInd].type,elems[separInd].lineNum,elems[separInd].start)
        return form, separInd, end
    return None, None, separInd


def getFormsSeparByElem(elemType,start,elems,level):
    forms = []
    secondForm, separInd, end = getFormAfterElem(elemType,start,elems,level)
    if secondForm is None:
        firstForm, end = getOneForm(start,elems,level,False)
        if firstForm is not None: forms.append(firstForm)
        return forms, end
    else:
        firstForm, endFirstForm = getOneForm(0,elems[start:separInd],level,False)
        if firstForm is None:
            raise SyntaxError, "Missing a form before '%s' on line %d, position %d" % (elems[separInd].type,elems[separInd].lineNum,elems[separInd].start)
        else:
            forms.append(firstForm)
        forms.append(secondForm)
        return forms, end
    

def getDictForm(start,elems,level):
    innerElems, indClosBr = getElemsInBrackets(start,elems)
    form = (FORM_TYPE,[(ATOM_TYPE,MAKE_DICTIONARY_FUNC)])
    ind = 0
    while ind<len(innerElems):
        forms, ind = getFormsSeparByElem("->",ind,innerElems,level)
        form[1].append(forms[0])
        if len(forms)==2:
            form[1].append(forms[1])
        elif len(forms)==1:
            form[1].append((ATOM_TYPE,LISP_NIL))
        elemFound, ind = skipElems([StrElem.WHITE_TYPE,","],ind,innerElems,False)
        if not elemFound: break
    return form, indClosBr+1

def getNFormsInBrack(start,elems,level,numForms):
    innerElems, indClosBr = getElemsInBrackets(start,elems)
    forms = getForms(innerElems,level,False)
    if len(forms)==0:
        raise SyntaxError, "Empty brackets, starting line %d, position %d" % (elems[start].lineNum,elems[start].start)
    elif len(forms)!=numForms:
        raise SyntaxError, "Brackets, starting line %d, position %d, contain %d forms instead of %d" % (elems[start].lineNum,elems[start].start,len(forms),numForms)
    return forms, indClosBr+1


def getComplNumForm(start,elems,level):
    ind = getRequiredElemInd("(",start+1,elems)
    forms, end = getNFormsInBrack(ind,elems,level,2)
    return (FORM_TYPE,[(ATOM_TYPE,MAKE_COMPLEX_NUM_FUNC),forms[0],forms[1]]), end


def funcCall(start,elems,level,lastForm):
    innerElems, indClosBr = getElemsInBrackets(start,elems)
    form = (FORM_TYPE,[])
    if lastForm is not None:
        form[1].append(lastForm)
    ind = 0
    while ind<len(innerElems):
        elemFound, ind = skipElems([StrElem.WHITE_TYPE,","],ind,innerElems,False)
        if not elemFound: break
        if innerElems[ind].type==".":
            brackInd = getRequiredElemInd("(",ind+1,innerElems)
            innerListForm, ind = funcCall(brackInd,innerElems,level,None)
            form[1].append(innerListForm)
        else:
            forms, ind = getFormsSeparByElem("=",ind,innerElems,level)
            form[1].extend(forms)
    return form, indClosBr+1


def getitemFuncCall(start,elems,level,lastForm):
    form = (FORM_TYPE,[(ATOM_TYPE,GET_ITEM_FUNC),lastForm])
    innerElems, indClosBr = getElemsInBrackets(start,elems)
    arrowPres, arrowInd = getElemIndInOperExpr("->",0,innerElems)
    if arrowPres:
        indexForm = (FORM_TYPE,[(ATOM_TYPE,MAKE_SLICE_FUNC)])
        startForm, irrelevantEnd = getOneForm(0,innerElems[0:arrowInd],level,False)
        endForm, endEndForm = getOneForm(arrowInd+1,innerElems,level,False)
        elemFound, ind = skipElems([StrElem.WHITE_TYPE,","],endEndForm,innerElems,False)
        if elemFound:
            stepForm, irrelevantEnd = getOneForm(ind,innerElems,level,False)
        else:
            stepForm = None
        if startForm is not None:
            indexForm[1].append(startForm)
        else:
            indexForm[1].append((ATOM_TYPE,LISP_NIL))
        if endForm is not None:
            indexForm[1].append(endForm)
        else:
            if startForm is None:
                raise SyntaxError, "No index present in brackets on line %d, position %d" % (elems[start].lineNum,elems[start].start)
            indexForm[1].append((ATOM_TYPE,LISP_NIL))
        if stepForm is not None:
            indexForm[1].append(stepForm)
        else:
            indexForm[1].append((ATOM_TYPE,LISP_NIL))
    else:
        indexForm, irrelevantEnd = getOneForm(0,innerElems,level,False)
        if indexForm is None:
            raise SyntaxError, "Expected index is missing in brackets on line %d, position %d" % (elems[start].lineNum,elems[start].start)
    form[1].append(indexForm)
    return form, indClosBr+1


def slotOrFuncCall(start,elems,level,lastForm,addLineNums):
    nameInd = getRequiredElemInd(StrElem.SYMB_TYPE,start+1,elems)
    elemFound, ind = skipElems([StrElem.WHITE_TYPE],nameInd+1,elems)
    if elemFound:
        if elems[ind].type=="(":
            form, ind = funcCall(ind,elems,level,lastForm)
            form[1].insert(0,(ATOM_TYPE,level.getRealSymbol(elems[nameInd].value)))
            return form, ind
        elif elems[ind].type=="{":
            return extendWithBodyBlock(ind,elems,level,
                                       (FORM_TYPE,[(ATOM_TYPE,level.getRealSymbol(elems[nameInd].value)),
                                                   lastForm]),
                                       addLineNums)
    return (FORM_TYPE,[(ATOM_TYPE,GET_OBJ_SLOT_FUNC),lastForm,
                       (SHORTCUT_TYPE, "'",
                        (ATOM_TYPE,level.getRealSymbol(elems[nameInd].value)))]), nameInd+1


def packOrKeywName(start,elems,level,lastForm):
    if lastForm is None:
        ind = getRequiredElemInd(StrElem.SYMB_TYPE,start+1,elems)
        return (ATOM_TYPE,elems[start].type+elems[ind].value), None, ind+1
    else:
        updatedLastForm = lastForm
        packageNamePresent = False
        if updatedLastForm[0]==ATOM_TYPE:
            updatedLastForm = (ATOM_TYPE,updatedLastForm[1]+elems[start].type)
            packageNamePresent = True
        ind = getRequiredElemInd(StrElem.SYMB_TYPE,start+1,elems)
        if packageNamePresent:
            return None, (ATOM_TYPE,updatedLastForm[1]+elems[ind].value), ind+1
        else:
            return (ATOM_TYPE,elems[start].type+elems[ind].value), updatedLastForm, ind+1


def extendWithBodyBlock(start,elems,level,lastForm,addLineNums):
    trueVal, forms, end = procBodyBlock(start,elems,level,addLineNums)
    form = lastForm
    if form[0]!=FORM_TYPE:
        form = (FORM_TYPE,[form])
    form[1].extend(forms)
    return form, end


def getStringAtom(start,elems):
    atom = (ATOM_TYPE, elems[start].value)
    ind = start+1
    while ind<len(elems):
        if elems[ind].type==elems[ind].LINE_END_TYPE:
            ind = elems.growOnIndex(ind+1)
        elif elems[ind].type==elems[ind].STR_MID_TYPE:
            atom = (ATOM_TYPE,atom[1]+elems[ind].value)
            ind = ind+1
        elif elems[ind].type==elems[ind].STR_END_TYPE:
            return (ATOM_TYPE,atom[1]+elems[ind].value), ind+1
        else:
            raise Exception, "Programming error: Unexpected type of StrElem - '%s', from line %d, position %d" % (elems[ind].type,elems[ind].lineNum,elems[ind].start)
    raise SyntaxError, "Cannot find the end of the string started on line %d, position %d" % (elems[start].lineNum,elems[start].start)


def getCLispAtom(start,elems):
    atom = (ATOM_TYPE, "")
    ind = start+1
    while ind<len(elems):
        if elems[ind].type==elems[ind].LINE_END_TYPE:
            ind = elems.growOnIndex(ind+1)
        elif elems[ind].type==elems[ind].CLISP_MID_TYPE:
            atom = (ATOM_TYPE,atom[1]+elems[ind].value)
            ind = ind+1
        elif elems[ind].type==elems[ind].CLISP_END_TYPE:
            return (ATOM_TYPE,atom[1]+elems[ind].value), ind+1
        else:
            raise Exception, "Programming error: Unexpected type of StrElem - '%s', from line %d, position %d" % (elems[ind].type,elems[ind].lineNum,elems[ind].start)
    raise SyntaxError, "Cannot find the end of the common lisp code started on line %d, position %d" % (elems[start].lineNum,elems[start].start)


def twLispDirectiveProc(start,elems,level):
    if elems[start].value==TL_DIR_GLOBAL:
        ind = getRequiredElemInd(StrElem.SYMB_TYPE,start+1,elems,False)
        end = ind+1
        if level.currImplVar.count(elems[ind].value)==0:
            level.currImplVar.append(elems[ind].value)
    elif elems[start].value==TL_DIR_LEXSCOPE:
        ind = getRequiredElemInd(StrElem.SPEC_SYMB_TYPE,start+1,elems,False)
        end = ind+1
        if elems[ind].value==TL_EXPL_SCOPE:
            level.implScope = False
        elif elems[ind].value==TL_IMPL_SCOPE:
            level.implScope = True
        else:
            raise SyntaxError, "Unexpected element '%s' on line %d, position %d" % (elems[ind].value,elems[ind].lineNum,elems[ind].start)
    elif elems[start].value==TL_DIR_USE:
        packName = ""
        elemFound, ind = getRequiredElemInd2(StrElem.SYMB_TYPE,start+1,elems,False)
        if elemFound:
            packName = packName + elems[ind].value +":"
            ind = ind+1
        elemFound, ind = getRequiredElemInd2(":",ind,elems,False)
        if elemFound:
            packName = packName + ":"
            ind = ind+1
        ind = getRequiredElemInd("{",ind,elems,False)
        innerElems, ind = getElemsInBrackets(ind,elems)
        end = ind+1
        ind = 0
        while ind<len(innerElems):
            elemFound, ind = skipElems([StrElem.WHITE_TYPE,","],ind,innerElems,False)
            if not elemFound: break
            ind = getRequiredElemInd(StrElem.SYMB_TYPE,ind,innerElems,False)
            symbName = innerElems[ind].value
            if (ind+1)<len(innerElems):
                elemFound, ind = getRequiredElemInd2("=",ind+1,innerElems)
            else:
                elemFound = False
            if elemFound:
                if (ind+1)<len(innerElems):
                    ind = getRequiredElemInd(StrElem.SYMB_TYPE,ind+1,innerElems,False)
                else:
                    raise SyntaxError, "Expected element '%s', on line %d is missing" % (StrElem.SYMB_TYPE,innerElems[ind].lineNum)
                nickName = innerElems[ind].value
            else:
                nickName = symbName
            level.addSymbSynonym(nickName,packName+symbName)
            ind = ind+1
    else:
        raise NotImplementedError, "Handling of a TwinLisp directive '%s' on line %d, position %d, is not implemented, yet." % (elems[start].value,elems[start].lineNum,elems[start].start)
    return end


_COMMENT = "comment"
_OP = "operator"
_UN_OP = "unar-oper"
_UN_BIN_OP = "unar-or-bin-oper"
_BIN_OP = "bin-oper"
_EXPR = "expression"
_SHORTCUT = "shortcut"
_NONE = "none"

def _lastOpExType(operAndExpr):
    if len(operAndExpr)>0:
        return operAndExpr[-1][0]
    else:
        return _NONE

def getOperAndExpr(startInd,elems,level,addLineNums):
    operAndExpr = []
    ind = startInd
    while ind<len(elems):
        elemFound, ind = skipElems([StrElem.WHITE_TYPE],ind,elems) # Does not go to the next line
        if not elemFound: break
        el = elems[ind]
        if (el.type==",") or (el.type==StrElem.LINE_END_TYPE):
            break
        elif el.type==el.COMM_TYPE:
            if len(operAndExpr)==0:
                operAndExpr.append((_COMMENT,(COMMENT_TYPE,el.value)))
                ind = ind+1
            break
        elif el.type==el.SYMB_TYPE:
            operAndExpr.append((_EXPR,(ATOM_TYPE,level.getRealSymbol(el.value))))
            ind = ind+1
        elif (el.type==el.NUM_TYPE) or (el.type==el.SYNT_STRUCT_TYPE):
            operAndExpr.append((_EXPR,(ATOM_TYPE,el.value)))
            ind = ind+1
        elif el.type==el.STR_START_TYPE:
            atom, ind = getStringAtom(ind,elems)
            operAndExpr.append((_EXPR,atom))
        elif el.type==el.CLISP_START_TYPE:
            atom, ind = getCLispAtom(ind,elems)
            operAndExpr.append((_EXPR,atom))
        elif (el.type==":") or (el.type=="::"):
            if _lastOpExType(operAndExpr)==_EXPR:
                lastForm = operAndExpr[-1][1]
            else:
                lastForm = None
            form, lastForm, ind = packOrKeywName(ind,elems,level,lastForm)
            if lastForm is not None: operAndExpr[-1] = (_EXPR,lastForm)
            if form is not None: operAndExpr.append((_EXPR,form))
        elif el.type==el.SPEC_SYMB_TYPE:
            if TL_BLOCK.has_key(el.value):
                form, ind = getBlockForm(ind,elems,level,addLineNums)
                operAndExpr.append((_EXPR,form))
            elif TL_DIRECT_SPEC_SYMB.count(el.value)!=0:
                ind = twLispDirectiveProc(ind,elems,level)
            else:
                raise SyntaxError, "Unexpected element '%s' on line %d, position %d" % (el.value,el.lineNum,el.start)
        elif el.type=="~(":
            form, ind = getBracketedForm(ind,elems,level,addLineNums)
            operAndExpr.append((_EXPR,form))
        elif el.type=="~[":
            form, ind = getListForm(ind,elems,level)
            operAndExpr.append((_EXPR,form))
        elif el.type=="(":
            if _lastOpExType(operAndExpr)==_EXPR:
                form, ind = funcCall(ind,elems,level,operAndExpr[-1][1])
                operAndExpr[-1] = (_EXPR,form)
            else:
                forms, ind = getNFormsInBrack(ind,elems,level,1)
                operAndExpr.append((_EXPR,forms[0]))
        elif el.type=="[":
            if _lastOpExType(operAndExpr)==_EXPR:
                form, ind = getitemFuncCall(ind,elems,level,operAndExpr[-1][1])
                operAndExpr[-1] = (_EXPR,form)
            else:
                form, ind = getSimpleArrayForm(ind,elems,level)
                operAndExpr.append((_EXPR,form))
        elif el.type=="{":
            if _lastOpExType(operAndExpr)==_EXPR:
                form, ind = extendWithBodyBlock(ind,elems,level,operAndExpr[-1][1],addLineNums)
                operAndExpr[-1] = (_EXPR,form)
            else:
                form, ind = getDictForm(ind,elems,level)
                operAndExpr.append((_EXPR,form))
        elif (el.type==".") and (_lastOpExType(operAndExpr)==_EXPR):
            form, ind = slotOrFuncCall(ind,elems,level,operAndExpr[-1][1],addLineNums)
            operAndExpr[-1] = (_EXPR,form)
        elif SHORTCUT_OPERS.has_key(el.type):
            operAndExpr.append((_SHORTCUT,el))
            ind = ind+1
        elif COMPL_NUM_OPER.count(el.type)!=0:
            form, ind = getComplNumForm(ind,elems,level)
            operAndExpr.append((_EXPR,form))
        elif UNAR_OPERS.has_key(el.type):
            if BIN_OPERS.has_key(el.type):
                operAndExpr.append((_UN_BIN_OP,el))
            else:
                operAndExpr.append((_UN_OP,el))
            ind = ind+1
        elif BIN_OPERS.has_key(el.type):
            operAndExpr.append((_BIN_OP,el))
            ind = ind+1
        else:
            raise SyntaxError, "Unexpected element of type '%s' on line %d in position %d" % (el.type,el.lineNum,el.start)
    return operAndExpr, ind


def _reduceBinaryOper(operStack,exprStack,nextOper):
    nextOpPrec = BIN_OPERS[nextOper.type][1]
    while len(operStack)>0:
        lastOpType = operStack[-1][1].type
        lastOpPrec = BIN_OPERS[lastOpType][1]
        if (lastOpPrec<nextOpPrec) or ((lastOpPrec==nextOpPrec) and \
                ((BIN_OPERS[lastOpType][2]==LEFT_ASSOC) or (BIN_OPERS[lastOpType][2]==MULT_ARGS_ASSOC))):
            reducedExpr = None
            if (BIN_OPERS[lastOpType][2]==MULT_ARGS_ASSOC) and (exprStack[-2][0]==FORM_TYPE):
                if exprStack[-2][1][0]==(ATOM_TYPE,BIN_OPERS[lastOpType][0]):
                    reducedExpr = (exprStack[-2][0],exprStack[-2][1]+[exprStack[-1]])
            if reducedExpr is None:
                reducedExpr = (FORM_TYPE,[(ATOM_TYPE,BIN_OPERS[lastOpType][0]),exprStack[-2],exprStack[-1]])
            exprStack.pop()
            exprStack[-1] = reducedExpr
            operStack.pop()
        else:
            break


def _reduceUnaryOper(operStack,exprStack,expr):
    reducedExpr = expr
    while len(operStack)>0:
        if operStack[-1][0]==_UN_OP:
            funcName = UNAR_OPERS[operStack[-1][1].type][0]
            reducedExpr = (FORM_TYPE,[(ATOM_TYPE,funcName),reducedExpr])
            operStack.pop()
        else:
            break
    exprStack.append(reducedExpr)


def _reduceShorcut(operStack,exprStack,opex):
    if opex[0]==_EXPR:
        reducedExpr = opex[1]
    elif (opex[0]==_BIN_OP) or (opex[0]==_UN_BIN_OP):
        reducedExpr = (ATOM_TYPE,BIN_OPERS[opex[1].type][0])
    elif opex[0]==_UN_OP:
        reducedExpr = (ATOM_TYPE,UNAR_OPERS[opex[1].type][0])
    while len(operStack)>0:
        if operStack[-1][0]==_SHORTCUT:
            reducedExpr = (SHORTCUT_TYPE,SHORTCUT_OPERS[operStack[-1][1].type],reducedExpr)
            operStack.pop()
        else:
            break
    _reduceUnaryOper(operStack,exprStack,reducedExpr)


def _getFinalForm(operStack,exprStack,level):
    """This works with the assumption that only binary operators could have been left"""
    if len(exprStack)==0:
        if len(operStack)==0:
            return None
        else:
            raise SyntaxError, "Missing expression(s) to apply operator '%s' on line %d, position %d" % (operStack[-1][1].type,operStack[-1][1].lineNum,operStack[-1][1].start)
    while len(operStack)>0:
        lastOpType = operStack[-1][1].type
        reducedExpr = None
        if (BIN_OPERS[lastOpType][2]==MULT_ARGS_ASSOC) and (exprStack[-2][0]==FORM_TYPE):
            if exprStack[-2][1][0]==(ATOM_TYPE,BIN_OPERS[lastOpType][0]):
                reducedExpr = (exprStack[-2][0],exprStack[-2][1]+[exprStack[-1]])
        if reducedExpr is None:
            if lastOpType=="=": _formSymbAsImplVar(level,exprStack[-2])
            reducedExpr = (FORM_TYPE,[(ATOM_TYPE,BIN_OPERS[lastOpType][0]),exprStack[-2],exprStack[-1]])
        exprStack.pop()
        exprStack[-1] = reducedExpr
        operStack.pop()
    return exprStack[-1]


def getOperForm(operAndExpr,level):
    """Takes mixture of expr's and oper's and puts 'em into expr, whos form is returned.
    _SHORTCUT has precedence 0, and RIGHT_ASSOC. Note: _SHORTCUT changes the following oper to expr.
    Looking at UNAR_OPERS we note that all unary operators are RIGHT_ASSOC. Since there are no LEFT_ASSOC unary operators, their precedence does not matter. So, here we'll assume that *all unary* operators are RIGHT_ASSOC, and we won't bother with looking ahead, etc.
    Two consequent expr's is an error. Later, check for this should be moved to getOperAndExpr, were info about line positions is available, and more informative error message can be generated."""
    operStack = []
    exprStack = []
    lastElemType = _NONE
    ind = 0
    while ind<len(operAndExpr):
        opex = operAndExpr[ind]
        curr = opex[0]
        if lastElemType==_EXPR:
            if (curr==_EXPR) or (curr==_UN_OP) or (curr==_SHORTCUT):
                raise SyntaxError, "It is illegal to have two consequent expressions in an operator form"
            elif (curr==_BIN_OP) or (curr==_UN_BIN_OP):
                _reduceBinaryOper(operStack,exprStack,opex[1])
                operStack.append((_BIN_OP,opex[1]))
                lastElemType = _OP
            elif curr==_COMMENT:
                raise Exception, "Programming error: getOperAndExpr should separate operator expressions and comments"
            else:
                raise Exception, "Programming error: type of element in operAndExpr has invalid value '%s'" % curr
        elif lastElemType==_OP:
            if curr==_BIN_OP:
                raise SyntaxError, "Unexpected operator '%s' on line %d, position %d" % (opex[1].type,opex[1].lineNum,opex[1].start)
            elif (curr==_UN_OP) or (curr==_UN_BIN_OP):
                operStack.append((_UN_OP,opex[1]))
            elif curr==_SHORTCUT:
                operStack.append(opex)
                lastElemType = _SHORTCUT
            elif curr==_EXPR:
                _reduceUnaryOper(operStack,exprStack,opex[1])
                lastElemType = _EXPR
            elif curr==_COMMENT:
                raise SyntaxError, "Comment prematurely ends operator form on line %d, after position %d" % (operStack[-1][1].lineNum,operStack[-1][1].end)
            else:
                raise Exception, "Programming error: type of element in operAndExpr has invalid value '%s'" % curr
        elif lastElemType==_NONE:
            if curr==_BIN_OP:
                raise SyntaxError,"Operator '%s' on line %d, position %d, is not preceded by any expression" % (opex[1].type,opex[1].lineNum,opex[1].start)
            elif (curr==_UN_OP) or (curr==_UN_BIN_OP):
                operStack.append((_UN_OP,opex[1]))
                lastElemType = _OP
            elif curr==_SHORTCUT:
                operStack.append(opex)
                lastElemType = _SHORTCUT
            elif curr==_EXPR:
                exprStack.append(opex[1])
                lastElemType = _EXPR
            elif curr==_COMMENT:
                return opex[1]
            else:
                raise Exception, "Programming error: type of element in operAndExpr has invalid value '%s'" % curr
        elif lastElemType==_SHORTCUT:
            if curr==_SHORTCUT:
                operStack.append(opex)
            elif curr==_COMMENT:
                raise SyntaxError, "Comment prematurely ends operator form on line %d, after position %d" % (operStack[-1][1].lineNum,operStack[-1][1].end)
            else:
                _reduceShorcut(operStack,exprStack,opex)
                lastElemType = _EXPR
        else:
            raise Exception, "Programming error: lastElemType has invalid value '%s'" % curr
        ind = ind+1
    if (lastElemType==_OP) or (lastElemType==_SHORTCUT):
        raise SyntaxError, "Premature end of operator expression"
    return _getFinalForm(operStack,exprStack,level)


def getOneForm(startInd,elems,level,addLineNums):
    # returns only one first form or atom
    operAndExpr, end = getOperAndExpr(startInd,elems,level,addLineNums)
    form = getOperForm(operAndExpr,level)
    return form, end


def getForms(elems,level,addLineNums=False):
    formsAndVars = []
    ind = 0
    while ind<len(elems):
        elemFound, ind = skipElems([StrElem.WHITE_TYPE,","],ind,elems,False)
        if not elemFound: break
        if addLineNums:
            formsAndVars.append(([],(COMMENT_TYPE,"; source line # %d" % elems[ind].lineNum)))
        form, ind = getOneForm(ind,elems,level,addLineNums)
        if form is not None:
            formsAndVars.append((level.newVars,form))
            level.newVars = []
    forms = []
    if level.isTopLevel:
        for varAndForm in formsAndVars:
            forms.append(varAndForm[1])
    else:
        innerForms = forms
        for varAndForm in formsAndVars:
            if len(varAndForm[0])!=0:
                form = (FORM_TYPE,[(ATOM_TYPE,"let"),(FORM_TYPE,[])])
                for symbName in varAndForm[0]:
                    form[1][1][1].append((ATOM_TYPE,symbName))
                innerForms.append(form)
                innerForms = form[1]
            innerForms.append(varAndForm[1])
    return forms

