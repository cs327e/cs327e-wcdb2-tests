

# -------
# imports
# -------

import StringIO
import unittest


from WCDB2 import *

# --------
# TestWCDB
# --------

class TestWCDB (unittest.TestCase) :

    def test_insertSQL_1 (self) :
        table = "Name"
        catagoryDict ={'Name': [{'organizationKindIdent': "'AUN'", 'Name': "'Agency of the United Nations'"}]} 
        cat = "OrganizationKind"
        returnValue = insertSQL(table,catagoryDict,cat)
        self.assert_(returnValue == "drop table if exists orgKName;\nCREATE TABLE orgKName(organizationKindIdent text,Name text);\ninsert into orgKName (organizationKindIdent, Name) values ('AUN', 'Agency of the United Nations');\n")

    def test_insertSQL_2 (self) :
        table = "Name"
        catagoryDict ={'Name': [{'personKindIdent': "'PR'", 'Name': "'obama'"}]} 
        cat = "PersonKind"
        returnValue = insertSQL(table,catagoryDict,cat)
        self.assert_(returnValue == "drop table if exists perKName;\nCREATE TABLE perKName(Name text,personKindIdent text);\ninsert into perKName (Name, personKindIdent) values ('obama', 'PR');\n")

    def test_insertSQL_3 (self) :
        table = "Name"
        catagoryDict ={'Name': [{'crisisIdent': "'GJD12'", 'Name': "'Bombing'"}]} 
        cat = "Crisis"
        returnValue = insertSQL(table,catagoryDict,cat)
        self.assert_(returnValue == "drop table if exists criName;\nCREATE TABLE criName(crisisIdent text,Name text);\ninsert into criName (crisisIdent, Name) values ('GJD12', 'Bombing');\n")



    def test_main_1 (self) :
        r = StringIO.StringIO("<first>\n<second>\n</second>\n</first>")
        w = StringIO.StringIO()
        main(r, w)
        self.assert_(w.getvalue() == "<first>\n<second>\n</second>\n</first>")

    def test_main_2 (self) :
        r = StringIO.StringIO("<first>\n<s>\n</s>\n</first>")
        w = StringIO.StringIO()
        main(r, w)
        self.assert_(w.getvalue() == "<first>\n<s>\n</s>\n</first>")

    def test_main_3 (self) :
        r = StringIO.StringIO("<first><second></second></first>")
        w = StringIO.StringIO()
        main(r, w)
        self.assert_(w.getvalue() == "<first><second /></first>")



    def test_login_1 (self) :
        c = login(
            "z",
            "tracy",
            "mfTTR8Puk5",
            "cs327e_tracy")
        assert str(type(c)) == "<type '_mysql.connection'>"

    def test_login_2 (self) :
        c = login(
            "z",
            "amtul",
            "bhoe8w2M2b",
            "cs327e_amtul")
        assert str(type(c)) == "<type '_mysql.connection'>"


    def test_login_3 (self) :
        c = login()
        assert str(type(c)) == "<type '_mysql.connection'>"




print "TestWCDB2.py"
unittest.main()
print "Done."