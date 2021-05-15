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
from FormBuilding import getForms, LevelInfo
from StringReading import GrowingList


def formToText(form):
    if form[0]==ATOM_TYPE:
        return form[1]
    elif form[0]==FORM_TYPE:
        text = ""
        for subForm in form[1]:
            text = text + formToText(subForm) + " "
        if len(text)>0:
            text = text[0:len(text)-1]  # strip one space at the end
        text = "("+text+")"
        return text
    elif  form[0]==COMMENT_TYPE:
        return form[1]+"\n"
    elif form[0]==SHORTCUT_TYPE:
        return form[1]+formToText(form[2])
    else:
        raise Exception, "Programming error: unknown form type: "+form[0].__str__()


def writeTo(form,dest):
    text = formToText(form)
    if text[-1]!="\n":
        dest.write(text+"\n")
    else:
        dest.write(text)


def translate(source,dest,lineNumbering=False):
    for form in getForms(GrowingList(source),
                         LevelInfo(implScope=True,explScopeWarn=True),
                         lineNumbering):
        writeTo(form,dest)

