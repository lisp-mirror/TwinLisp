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
from Const import *
from FormWritting import formToText, translate


class TestFormWritting(unittest.TestCase):

    def testFormToText1(self):
        form = (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),
                           (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),
                                       (FORM_TYPE,[(ATOM_TYPE,"_*_"),(ATOM_TYPE,"y"),(ATOM_TYPE,"d")])])])
        self.assertEqual(formToText(form),"(setf a (_+_ x (_*_ y d)))")

    def testFormToText2(self):
        form = (SHORTCUT_TYPE, "'",
                (FORM_TYPE,[(ATOM_TYPE,"setf"),(ATOM_TYPE,"a"),
                            (FORM_TYPE,[(ATOM_TYPE,"_+_"),(ATOM_TYPE,"x"),
                                        (FORM_TYPE,[(ATOM_TYPE,"_*_"),(ATOM_TYPE,"y"),(ATOM_TYPE,"d")])])]))
        self.assertEqual(formToText(form),"'(setf a (_+_ x (_*_ y d)))")

    def testTranslate1(self):
        source = StringIO.StringIO("""let(x,y,d) {
                                        x=s+t**j**f-k
                                        y=d=e-r}""")
        dest = StringIO.StringIO()
        translate(source,dest)
        self.assertEqual(dest.getvalue(),"""(let (x y d) (setf x (_-_ (_+_ s (_**_ t (_**_ j f))) k)) (setf y (setf d (_-_ e r))))
""")

    def testTranslate2(self):
        source = StringIO.StringIO("""s+t**j**f-k
                                      e-r""")
        dest = StringIO.StringIO()
        translate(source,dest,True)
        self.assertEqual(dest.getvalue(),"""; source line # 1
(_-_ (_+_ s (_**_ t (_**_ j f))) k)
; source line # 2
(_-_ e r)
""")

    def testTranslate3(self):
        source = StringIO.StringIO("""`($s + t**j**f - $k)
                                      '(e-r)""")
        dest = StringIO.StringIO()
        translate(source,dest)
        self.assertEqual(dest.getvalue(),"""`(_-_ (_+_ ,s (_**_ t (_**_ j f))) ,k)
'(_-_ e r)
""")


if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFormWritting))
    unittest.TextTestRunner(verbosity=1).run(suite)

