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
#  Twin Lisp translator
#  can be used interactively and for file translation
#

from StringReading import GrowingList
from FormBuilding import getOneForm, LevelInfo
from FormWritting import writeTo, translate
import sys

class ReaderWriter(object):
    def __init__(self):
        self.stdin = sys.stdin
        self.firstLine = True
        self.stdout = sys.stdout
    def readline(self):
        if self.firstLine:
            self.stdout.write(">>> ")
            self.firstLine = False
        else:
            self.stdout.write("... ")
        return self.stdin.readline()


def interactiveTranslation():
    source = ReaderWriter()
    dest = source.stdout
    print """This is a Twin Lisp interactive translator.
You type Twin Lisp, the output will be Common Lisp.
Typing "Ctrl-D" or "exit" quits translator."""
    levelInfo = LevelInfo(implScope=True,explScopeWarn=True)
    while True:
        source.firstLine = True
        gL = GrowingList(source)
        if len(gL)==0:  # this will be caused by Ctrl-D
            dest.write("\nBye.\n")
            break
        if gL[0].type==gL[0].SYMB_TYPE: # typing exit
            if gL[0].value=="exit":
                dest.write("Bye.\n")
                break
        try:
            form, ind = getOneForm(0,gL,levelInfo,False)
            if form is not None: writeTo(form,dest)
        except SyntaxError, er:
            print "Syntax Error:"
            print er.__str__()


def fileTranslation(fNames):
    for fName in fNames:
        if fName[-4:len(fName)]==".twl":
            destFName = fName[0:-4] + ".lisp"
        else:
            destFName = fName + ".lisp"
        try:
            sourceFile = open(fName,"r")
            destFile = open(destFName,"w")
            try:
                translate(sourceFile,destFile)
            except SyntaxError, er:
                print "Syntax Error in file '%s':" % fName
                print er.__str__()
                break
        finally:
            sourceFile.close()
            destFile.close()


if __name__=='__main__':
    args = sys.argv
    if len(args)==1:
        interactiveTranslation()
    elif len(args)>1:
        fileTranslation(args[1:len(args)])


