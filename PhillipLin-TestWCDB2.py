#!/usr/bin/env python

# ---------------------------
# cs327e-wcdb1/TestWCDB2.py
# Copyright (C) 2013
# Team: Byte Me
# --------------------------

# -------
# imports
# -------

import StringIO
import unittest
import xml.etree.ElementTree as et
import lxml.etree as let
import MySQLdb

from WCDB2 import *

# -----------
# TestWCDB1
# -----------

class TestWCDB2 (unittest.TestCase) :
    # --------
    # xml_read
    # --------

    def test_read_1 (self) :
         r = StringIO.StringIO("<WorldCrisisDatabase><Crisis></Crisis></WorldCrisisDatabase>");
         xml_string = xml_read(r);
         self.assert_(xml_string == "<WorldCrisisDatabase><Crisis></Crisis></WorldCrisisDatabase>");

    def test_read_2 (self) :
         r = StringIO.StringIO("<WorldCrisisDatabase>\n<Crisis>\n</Crisis>\n</WorldCrisisDatabase>");
         xml_string = xml_read(r);
         self.assert_(xml_string == "<WorldCrisisDatabase>\n<Crisis>\n</Crisis>\n</WorldCrisisDatabase>");

    def test_read_3 (self) :
         r = StringIO.StringIO("<WorldCrisisDatabase>\t\t\t\n\t<Crisis>\t\t\n</Crisis>\n\t</WorldCrisisDatabase>");
         xml_string = xml_read(r);
         self.assert_(xml_string == "<WorldCrisisDatabase>\t\t\t\n\t<Crisis>\t\t\n</Crisis>\n\t</WorldCrisisDatabase>");

    # ----
    # xml_import
    # ----

    def test_import_1 (self) :
         r = "<WorldCrisisDatabase><Crisis></Crisis></WorldCrisisDatabase>"
         e_tree = xml_import(et, r)
         a = et.Element('WorldCrisisDatabase')
         b = et.SubElement(a, 'Crisis')
         self.assert_(et.tostring(e_tree, encoding="us-ascii", method="xml") == et.tostring(a, encoding="us-ascii", method="xml"))

    def test_import_2 (self) :
         r = "<a><b></b><c><d></d><e></e></c></a>"
         e_tree = xml_import(et, r)
         a = et.Element('a')
         b = et.SubElement(a, 'b')
         c = et.SubElement(a, 'c')
         d = et.SubElement(c, 'd')
         e = et.SubElement(c, 'e')
         self.assert_(et.tostring(e_tree, encoding="us-ascii", method="xml") == et.tostring(a, encoding="us-ascii", method="xml"))

    def test_import_3 (self) :
         r = "<a><b></b><c><d/><e/></c></a>"
         e_tree = xml_import(et, r)
         a = et.Element('a')
         b = et.SubElement(a, 'b')
         c = et.SubElement(a, 'c')
         d = et.SubElement(c, 'd')
         e = et.SubElement(c, 'e')
         self.assert_(et.tostring(e_tree, encoding="us-ascii", method="xml") == et.tostring(a, encoding="us-ascii", method="xml"))

    # -----
    # xml_export
    # -----

    def test_export_1 (self) :
        w = StringIO.StringIO()
        a = et.Element('WorldCrisisDatabase')
        b = et.SubElement(a, 'Crisis')
        xml_export(w, et, let, a)
        self.assert_(w.getvalue() == "<WorldCrisisDatabase>\n  <Crisis/>\n</WorldCrisisDatabase>\n")

    def test_export_2 (self) :
        w = StringIO.StringIO()
        a = et.Element('a')
        b = et.SubElement(a, 'b')
        c = et.SubElement(a, 'c')
        d = et.SubElement(c, 'd')
        e = et.SubElement(c, 'e')
        xml_export(w, et, let, a)
        self.assert_(w.getvalue() == "<a>\n  <b/>\n  <c>\n    <d/>\n    <e/>\n  </c>\n</a>\n")

    def test_export_3 (self) :
        w = StringIO.StringIO()
        a = et.Element('a')
        b = et.SubElement(a, 'b')
        c = et.SubElement(b, 'c')
        d = et.SubElement(c, 'd')
        e = et.SubElement(d, 'e')
        xml_export(w, et, let, a)
        self.assert_(w.getvalue() == "<a>\n  <b>\n    <c>\n      <d>\n        <e/>\n      </d>\n    </c>\n  </b>\n</a>\n")

    # -----
    # login
    # -----

    def test_login_1 (self) :
        h = "localhost"
        u = "admin"
        p = "admin"
        db = "WCDB"
        c = login(h, u, p, db)
        self.assert_(c)

    def test_login_2 (self) :
        h = "localhost"
        u = "admin"
        p = "badpass"
        db = "WCDB"
        error = False;
        try:
            c = login(h, u, p, db)
        except:   
            error = True
        self.assert_(error)

    def test_login_3 (self) :
        h = "localhost"
        u = "baduser"
        p = "admin"
        db = "WCDB"
        error = False;
        try:
            c = login(h, u, p, db)
        except:   
            error = True
        self.assert_(error)

    # -----
    # import_WCDB
    # -----

    def test_import_WCDB_1 (self) :
        h = "localhost"
        u = "admin"
        p = "admin"
        db = "WCDB"
        c = login(h, u, p, db)
        r = open("WCDB2.xml")
        e_tree = xml_import(et, xml_read(r))
        result = import_WCDB(c, e_tree)
        self.assert_(result is None)
        

    def test_import_WCDB_2 (self) :
        h = "localhost"
        u = "admin"
        p = "admin"
        db = "WCDB"
        c = login(h, u, p, db)
        create_WCDB(c)
        r = open("Acceptance Tests/RunWCDB2_5.in.xml")
        e_tree = xml_import(et, xml_read(r))
        result = import_WCDB(c, e_tree)
        self.assert_(result is None)
        curs=c.cursor()
        curs.execute('SELECT * from Person')
        self.assert_(curs.fetchone() == None)
        curs.execute('SELECT * from Crisis')
        self.assert_(curs.fetchone() == None)
        curs.execute('SELECT * from Organization')
        self.assert_(curs.fetchone() == None)

    def test_import_WCDB_3 (self) :
        h = "localhost"
        u = "admin"
        p = "admin"
        db = "WCDB"
        c = login(h, u, p, db)
        r = open("Acceptance Tests/RunWCDB2_1.in.xml")
        e_tree = xml_import(et, xml_read(r))
        result = import_WCDB(c, e_tree)
        self.assert_(result is None)
        curs=c.cursor()
        curs.execute('SELECT * from Person')
        self.assert_(curs.fetchone() != None)
        curs.execute('SELECT * from Crisis')
        self.assert_(curs.fetchone() != None)
        curs.execute('SELECT * from Organization')
        self.assert_(curs.fetchone() != None)
    # -----
    # export_WCDB
    # -----

    def test_export_WCDB_1 (self) :
        h = "localhost"
        u = "admin"
        p = "admin"
        db = "WCDB"
        c = login(h, u, p, db)
        create_WCDB(c)
        r = open("WCDB2.xml")
        e_tree = xml_import(et, xml_read(r))
        import_WCDB(c, e_tree)
        w = StringIO.StringIO()
        xml_export(w, et, let, export_WCDB(c, et))
        assert(w.getvalue() != None)

    def test_export_WCDB_2 (self) :
        h = "localhost"
        u = "admin"
        p = "admin"
        db = "WCDB"
        c = login(h, u, p, db)
        create_WCDB(c)
        r = open("Acceptance Tests/RunWCDB2_5.in.xml")
        e_tree = xml_import(et, xml_read(r))
        import_WCDB(c, e_tree)
        w = StringIO.StringIO()
        xml_export(w, et, let, export_WCDB(c, et))
        assert(w.getvalue() == "<WorldCrises/>\n")

    def test_export_WCDB_3 (self) :
        h = "localhost"
        u = "admin"
        p = "admin"
        db = "WCDB"
        c = login(h, u, p, db)
        create_WCDB(c)
        r = open("Acceptance Tests/RunWCDB2_8.in.xml")
        e_tree = xml_import(et, xml_read(r))
        import_WCDB(c, e_tree)
        w = StringIO.StringIO()
        xml_export(w, et, let, export_WCDB(c, et))
        assert(w.getvalue() =="<WorldCrises>\n  <Crisis crisisIdent=\"C01\">\n    <Name>The Great Chicago Fire</Name>\n    <Kind crisisKindIdent=\"ND\"/>\n    <Location>\n      <Locality>Chicago</Locality>\n      <Region>Illinois</Region>\n      <Country>United States</Country>\n    </Location>\n    <StartDateTime>\n      <Date>1871-10-08</Date>\n    </StartDateTime>\n    <HumanImpact>\n      <Type>None</Type>\n      <Number>None</Number>\n    </HumanImpact>\n    <EconomicImpact>222 Million USD</EconomicImpact>\n    <ResourceNeeded>None</ResourceNeeded>\n    <WaysToHelp>Donation</WaysToHelp>\n  </Crisis>\n  <Organization organizationIdent=\"O01\">\n    <Name>American Red Cross</Name>\n    <Kind organizationKindIdent=\"HA\"/>\n    <Location>\n      <Locality>Washington</Locality>\n      <Region>D.C.</Region>\n      <Country>united States</Country>\n    </Location>\n    <History>Founded in 1881. Dedicated to assisting in great national disasters.</History>\n    <ContactInfo>\n      <Telephone>18007332767</Telephone>\n      <Fax>18007332767</Fax>\n      <Email>redcross@help.help</Email>\n      <PostalAddress>\n        <StreetAddress>2218 Pershing Dr</StreetAddress>\n        <Locality>Austin</Locality>\n        <Region>Texas</Region>\n        <PostalCode>78723</PostalCode>\n        <Country>United States</Country>\n      </PostalAddress>\n    </ContactInfo>\n  </Organization>\n  <Person personIdent=\"P01\">\n    <Name>\n      <FirstName>Clara</FirstName>\n      <LastName>Barton</LastName>\n    </Name>\n    <Kind organizationKindIdent=\"F\"/>\n    <Location>\n      <Locality>Washington</Locality>\n      <Region>D.C.</Region>\n      <Country>United States</Country>\n    </Location>\n  </Person>\n  <CrisisKind crisisKindIdent=\"ND\">\n    <Name>Natural Disaster</Name>\n    <Description>A natural event causes the crisis (e.g. flood, tornado, hurricane, earthquake, volcano, etc.)</Description>\n  </CrisisKind>\n  <OrganizationKind organizationKindIdent=\"HA\">\n    <Name>Humanitarian Aid</Name>\n    <Description>Concerned with or seeking to promote human welfare: \"groups sending humanitarian aid\".</Description>\n  </OrganizationKind>\n  <OrganizationKind organizationKindIdent=\"DIS\">\n    <Name>Disaster Relief Agency</Name>\n    <Description>Provides aid in the aftermath of a disaster.</Description>\n  </OrganizationKind>\n  <OrganizationKind organizationKindIdent=\"APA\">\n    <Name>Animal Protection Agency</Name>\n    <Description>An APA is an organization dedicated to the welfare of animals, especially in times of crisis.</Description>\n  </OrganizationKind>\n  <OrganizationKind organizationKindIdent=\"NP\">\n    <Name>Non-Profit</Name>\n    <Description>A Non-Profit organization uses surplus revenues to achieve its goals (usually humanitarian) rather than distributing them as profit or dividends.</Description>\n  </OrganizationKind>\n  <OrganizationKind organizationKindIdent=\"CO\">\n    <Name>Charitable Organization</Name>\n    <Description>A Charitable Organization provides a service to the needed in the community. THe organization relies on the charity of the community (e.g. donations) to operate.</Description>\n  </OrganizationKind>\n  <PersonKind personKindIdent=\"F\">\n    <Name>Founder</Name>\n    <Description>Person who established an institution</Description>\n  </PersonKind>\n  <PersonKind personKindIdent=\"PCEO\">\n    <Name>Prseident and CEO</Name>\n    <Description>President and Chief executive officer of an institution. Typically the highest ranking executive of a company.</Description>\n  </PersonKind>\n  <PersonKind personKindIdent=\"GOV\">\n    <Name>Governor</Name>\n    <Description>Elected head of a state in the US.</Description>\n  </PersonKind>\n  <PersonKind personKindIdent=\"VP\">\n    <Name>Vice President</Name>\n    <Description>An official or executive ranking below and deputizing for a president.</Description>\n  </PersonKind>\n  <PersonKind personKindIdent=\"CM\">\n    <Name>Chairman</Name>\n    <Description>The permanent or long-term president of a committee, company, or other organization.</Description>\n  </PersonKind>\n  <PersonKind personKindIdent=\"AMB\">\n    <Name>United States Ambassador</Name>\n    <Description>An accredited diplomat sent by a country as its official representative to a foreign country.</Description>\n  </PersonKind>\n  <PersonKind personKindIdent=\"SW\">\n    <Name>Social Worker</Name>\n    <Description>Someone employed to provide social services (especially to the disadvantaged).</Description>\n  </PersonKind>\n  <PersonKind personKindIdent=\"H\">\n    <Name>Humanitarian</Name>\n    <Description>A person who seeks to promote human welfare; a philanthropist.</Description>\n  </PersonKind>\n</WorldCrises>\n")

    # -----
    # create_WCDB
    # -----

    def test_create_WCDB_1 (self) :
        h = "localhost"
        u = "admin"
        p = "admin"
        db = "WCDB"
        c = login(h, u, p, db)
        result = create_WCDB(c)
        curs=c.cursor()
        curs.execute('SELECT * from Person')
     
        self.assert_(curs.fetchone() == None)
        curs.execute('SELECT * from Crisis')
        self.assert_(curs.fetchone() == None)
        curs.execute('SELECT * from Organization')
        self.assert_(curs.fetchone() == None)

    # Can't really test this any other way

# ----
# main
# ----

print("TestWCDB2.py")
unittest.main()
print("Done.")
