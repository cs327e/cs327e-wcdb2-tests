#!/usr/bin/env python

# ---------------------------
# Copyright (C) 2013
# Team: Better Late Than Never
# --------------------------

# -------
# imports
# -------

import xml.etree.ElementTree as ET
import os
import _mysql
import StringIO
import unittest
import sys

from WCDB2 import WCDB2_read, WCDB2_import, WCDB2_login, WCDB2_createTables, WCDB2_query, \
WCDB2_export, WCDB2_solve
# -----------
# TestWCDB1
# -----------

class TestWCDB2 (unittest.TestCase) :
    
    # -----------
    # WCDB2_read
    # -----------
    
    def test_read_1 (self):
        r = StringIO.StringIO("<country>\n<state></state>\n</country>")
        WCDB2_read(r)
        f = open("temp", 'r')
        lines = f.readlines()
        f.close()
        self.assert_(lines[0] == "<country>\n")
        self.assert_(lines[1] == "<state></state>\n")
        self.assert_(lines[2] == "</country>")

    
    def test_read_2 (self):
        r = StringIO.StringIO("<country></country>")
        WCDB2_read(r)
        f = open("temp", 'r')
        lines = f.readlines()
        f.close()
        self.assert_(lines[0] == "<country></country>")

    def test_read_3 (self):
        r = StringIO.StringIO("<a><b></b>\n<c><d>\n</d><e>\n</e></c></a>")
        WCDB2_read(r)
        f = open("temp", 'r')
        lines = f.readlines()
        f.close()
        self.assert_(lines[0] == "<a><b></b>\n")
        self.assert_(lines[1] == "<c><d>\n")
        self.assert_(lines[2] == "</d><e>\n")
        self.assert_(lines[3] == "</e></c></a>")


    # -----------
    # WCDB1_import
    # -----------
    
    def test_import_1 (self):
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        WCDB2_createTables(c)
        s = StringIO.StringIO("""<WorldCrises>
    <Crisis crisisIdent="CW2012">
    </Crisis>
    <Organization organizationIdent="WNG">
    </Organization>
    <Person personIdent="JHickenlooper">
    </Person>
</WorldCrises>""")
        WCDB2_read(s)
        tree = ET.parse('temp')
        WCDB2_import(tree)
        t = WCDB2_query(c,"select * from Crises")
        self.assert_(t == (('CW2012', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None),))

    def test_import_2 (self):
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        WCDB2_createTables(c)
        s = StringIO.StringIO("""<WorldCrises>
    <Crisis crisisIdent="CW2012">
    </Crisis>
    <Organization organizationIdent="WNG">
    </Organization>
    <Person personIdent="JHickenlooper">
    </Person>
</WorldCrises>""")
        WCDB2_read(s)
        tree = ET.parse('temp')
        WCDB2_import(tree)
        t = WCDB2_query(c,"select * from Organizations;")
        self.assert_((('WNG', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None),))

    def test_import_3 (self):
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        WCDB2_createTables(c)
        s = StringIO.StringIO("""<WorldCrises>
    <Crisis crisisIdent="CW2012">
    </Crisis>
    <Organization organizationIdent="WNG">
    </Organization>
    <Person personIdent="JHickenlooper">
    </Person>
</WorldCrises>""")
        WCDB2_read(s)
        tree = ET.parse('temp')
        WCDB2_import(tree)
        t = WCDB2_query(c,"select * from Persons;")
        self.assert_((('JHickenlooper', None, None, None, None, None, None, None, None, None, None, None, None, None, None),)) 
    c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
    WCDB2_query(c, "drop table if exists Crises")
    WCDB2_query(c, "drop table if exists Organizations")
    WCDB2_query(c, "drop table if exists Persons")
    WCDB2_query(c, "drop table if exists Relations")

    # ------------
    # WCDB2_login
    # ------------

    def test_login_1 (self) :
        connection = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        assert str(type(connection)) == "<type '_mysql.connection'>"

    def test_login_2 (self) :
        connection = WCDB2_login("z", "kjs969", "+gW_J3pDyG", "cs327e_kjs969")
        assert str(type(connection)) == "<type '_mysql.connection'>"
        

    def test_login_3 (self) :
        connection = WCDB2_login("z", "bes749", "sng753!!", "cs327e_bes749")
        assert str(type(connection)) == "<type '_mysql.connection'>"

    # ------------
    # WCDB2_createTables
    # ------------

    
    def test_createTables_1 (self) :
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        WCDB2_createTables(c)
        t = WCDB2_query(c, "show COLUMNS from Crises;")
        self.assert_( t == (('CrisisID', 'text', 'YES', '', None, ''), ('Name', 'text', 'YES', '', None, ''), ('Kind', 'text', 'YES', '', None, ''), ('Locality', 'text', 'YES', '', None, ''), ('Region', 'text', 'YES', '', None, ''), ('Country', 'text', 'YES', '', None, ''), ('StartDate', 'text', 'YES', '', None, ''), ('EndDate', 'text', 'YES', '', None, ''), ('HumanImpactType', 'text', 'YES', '', None, ''), ('HumanImpactNumber', 'text', 'YES', '', None, ''), ('EconomicImpact', 'text', 'YES', '', None, ''), ('ResourceNeeded', 'text', 'YES', '', None, ''), ('WaysToHelp', 'text', 'YES', '', None, ''), ('ImageURL', 'text', 'YES', '', None, ''), ('VideoURL', 'text', 'YES', '', None, ''), ('MapURL', 'text', 'YES', '', None, ''), ('SocialNetworkURL', 'text', 'YES', '', None, ''), ('Citation', 'text', 'YES', '', None, ''), ('ExternalLinkURL', 'text', 'YES', '', None, '')))

    def test_createTables_2 (self) :
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        WCDB2_createTables(c)
        t = WCDB2_query(c, "show COLUMNS from Persons;")
        self.assert_(t == (('PersonID', 'text', 'YES', '', None, ''), ('FirstName', 'text', 'YES', '', None, ''), ('MiddleName', 'text', 'YES', '', None, ''), ('LastName', 'text', 'YES', '', None, ''), ('Suffix', 'text', 'YES', '', None, ''), ('Kind', 'text', 'YES', '', None, ''), ('Locality', 'text', 'YES', '', None, ''), ('Region', 'text', 'YES', '', None, ''), ('Country', 'text', 'YES', '', None, ''), ('ImageURL', 'text', 'YES', '', None, ''), ('VideoURL', 'text', 'YES', '', None, ''), ('MapURL', 'text', 'YES', '', None, ''), ('SocialNetworkURL', 'text', 'YES', '', None, ''), ('Citation', 'text', 'YES', '', None, ''), ('ExternalLinkURL', 'text', 'YES', '', None, '')))

    def test_createTables_3 (self) :
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        WCDB2_createTables(c)
        t = WCDB2_query(c, "show COLUMNS from Relations;")
        self.assert_( t == (('CrisisID', 'text', 'YES', '', None, ''), ('PersonID', 'text', 'YES', '', None, ''), ('OrganizationID', 'text', 'YES', '', None, '')))

    c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
    WCDB2_query(c, "drop table if exists Crises")
    WCDB2_query(c, "drop table if exists Organizations")
    WCDB2_query(c, "drop table if exists Persons")
    WCDB2_query(c, "drop table if exists Relations")
    
    # ------------
    # WCDB2_query
    # ------------
    
    WCDB2_createTables(c)
    
    def test_query_1 (self) :
        c = WCDB2_login("z", "dmoodz", "easy","cs327e_dmoodz")
        t = WCDB2_query(c, "select sqrt (3.67) from dual;") 
        self.assert_( t == (('1.9157244060668',),) )

    def test_query_2 (self) :
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        t = WCDB2_query( c, "select concat ('Michael', 'Jackson') as 'NAME' from dual;")
        self.assert_( t == (('MichaelJackson',),) )

    def test_query_3 (self) :
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        t = WCDB2_query( c, "select power (2.512, 5) from dual")
        self.assert_( t == (('100.022608259449',),))    

    c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
    WCDB2_query(c, "drop table if exists Crises")
    WCDB2_query(c, "drop table if exists Organizations")
    WCDB2_query(c, "drop table if exists Persons")
    WCDB2_query(c, "drop table if exists Relations")
    
    # ------------
    # WCDB2_export
    # ------------

    def test_export_1 (self) :
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        w = StringIO.StringIO()
        WCDB2_createTables(c)
        WCDB2_query(c, """insert into Crises values ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s");""")
        WCDB2_query(c, """insert into Relations values ("a", "b", "c");""")
        WCDB2_export(w)
        self.assert_(w.getvalue() == """<WorldCrises>
  <Crisis crisisIdent="a">
    <Name>b</Name>
    <Kind crisisKindIdent="c"/>
    <Location>
      <Locality>d</Locality>
      <Region>e</Region>
      <Country>f</Country>
    </Location>
    <StartDateTime>
      <Date>g</Date>
    </StartDateTime>
    <EndDateTime>
      <Date>h</Date>
    </EndDateTime>
    <HumanImpact>
      <Type>i</Type>
      <Number>j</Number>
    </HumanImpact>
    <EconomicImpact>k</EconomicImpact>
    <ResourceNeeded>l</ResourceNeeded>
    <WaysToHelp>m</WaysToHelp>
    <ExternalResources>
      <ImageURL>n</ImageURL>
      <VideoURL>o</VideoURL>
      <MapURL>p</MapURL>
      <SocialNetworkURL>q</SocialNetworkURL>
      <Citation>r</Citation>
      <ExternalLinkURL>s</ExternalLinkURL>
    </ExternalResources>
    <RelatedPersons>
      <RelatedPerson personIdent="b"/>
    </RelatedPersons>
    <RelatedOrganizations>
      <RelatedOrganization organizationIdent="c"/>
    </RelatedOrganizations>
  </Crisis>
  <CrisisKind crisisKindIdent="c">
    <Name>c</Name>
    <Description/>
  </CrisisKind>
</WorldCrises>
""")

    def test_export_2 (self) :
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        w = StringIO.StringIO()
        WCDB2_createTables(c)
        WCDB2_query(c, """insert into Organizations values ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r");""")
        WCDB2_query(c, """insert into Relations values ("a", "b", "c");""")
        WCDB2_export(w)
        self.assert_(w.getvalue() == """<WorldCrises>
  <Organization organizationIdent="a">
    <Name>b</Name>
    <Kind organizationKindIdent="c"/>
    <Location>
      <Locality>i</Locality>
      <Region>j</Region>
      <Country>l</Country>
    </Location>
    <History>d</History>
    <ContactInfo>
      <Telephone>e</Telephone>
      <Fax>f</Fax>
      <Email>g</Email>
      <PostalAddress>
        <StreetAddress>h</StreetAddress>
        <Locality>i</Locality>
        <Region>j</Region>
        <PostalCode>k</PostalCode>
        <Country>l</Country>
      </PostalAddress>
    </ContactInfo>
    <ExternalResources>
      <ImageURL>m</ImageURL>
      <VideoURL>n</VideoURL>
      <MapURL>o</MapURL>
      <SocialNetworkURL>p</SocialNetworkURL>
      <Citation>q</Citation>
      <ExternalLinkURL>r</ExternalLinkURL>
    </ExternalResources>
    <RelatedCrises/>
    <RelatedPersons/>
  </Organization>
  <OrganizationKind organizationKindIdent="c">
    <Name>c</Name>
    <Description/>
  </OrganizationKind>
</WorldCrises>
""")

    def test_export_3 (self) :
        c = WCDB2_login("z", "dmoodz", "easy", "cs327e_dmoodz")
        w = StringIO.StringIO()
        WCDB2_createTables(c)
        WCDB2_query(c, """insert into Persons values ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o");""")
        WCDB2_query(c, """insert into Relations values ("a", "b", "c");""")
        WCDB2_export(w)
        self.assert_(w.getvalue() == """<WorldCrises>
  <Person personIdent="a">
    <Name>
      <FirstName>b</FirstName>
      <MiddleName>c</MiddleName>
      <LastName>d</LastName>
      <Suffix>e</Suffix>
    </Name>
    <Kind personKindIdent="f"/>
    <Location>
      <Locality>g</Locality>
      <Region>h</Region>
      <Country>i</Country>
    </Location>
    <ExternalResources>
      <ImageURL>j</ImageURL>
      <VideoURL>k</VideoURL>
      <MapURL>l</MapURL>
      <SocialNetworkURL>m</SocialNetworkURL>
      <Citation>n</Citation>
      <ExternalLinkURL>o</ExternalLinkURL>
    </ExternalResources>
    <RelatedCrises/>
    <RelatedOrganizations/>
  </Person>
  <PersonKind personKindIdent="f">
    <Name>f</Name>
    <Description/>
  </PersonKind>
</WorldCrises>
""")
    
    # -----------
    # WCDB2_solve
    # -----------

    def test_solve_1 (self) :
        r = StringIO.StringIO("""<WorldCrises>
  <Crisis crisisIdent="YF1988">
    <Name>Yellowstone Forest Fires of 1988</Name>
    <Kind crisisKindIdent="Wildfire"/>
    <Location>
      <Locality>Yellowstone National Park</Locality>
      <Region>Wyoming</Region>
      <Country>United States of America</Country>
    </Location>
    <HumanImpact>
      <Type/>
      <Number/>
    </HumanImpact>
    <EconomicImpact/>
    <ResourceNeeded/>
    <WaysToHelp/>
    <ExternalResources>
      <ImageURL/>
    </ExternalResources>
    <RelatedPersons/>
    <RelatedOrganizations/>
  </Crisis>
  <CrisisKind crisisKindIdent="Wildfire">
    <Name>Wildfire</Name>
    <Description/>
  </CrisisKind>
</WorldCrises>""")
        w = StringIO.StringIO()
        WCDB2_solve(r, w)
        self.assert_(w.getvalue() == """<WorldCrises>
  <Crisis crisisIdent="YF1988">
    <Name>Yellowstone Forest Fires of 1988</Name>
    <Kind crisisKindIdent="Wildfire"/>
    <Location>
      <Locality>Yellowstone National Park</Locality>
      <Region>Wyoming</Region>
      <Country>United States of America</Country>
    </Location>
    <HumanImpact>
      <Type/>
      <Number/>
    </HumanImpact>
    <EconomicImpact/>
    <ResourceNeeded/>
    <WaysToHelp/>
    <ExternalResources>
      <ImageURL/>
    </ExternalResources>
    <RelatedPersons/>
    <RelatedOrganizations/>
  </Crisis>
  <CrisisKind crisisKindIdent="Wildfire">
    <Name>Wildfire</Name>
    <Description/>
  </CrisisKind>
</WorldCrises>
""")

    def test_solve_2 (self) :
        r = StringIO.StringIO("""<WorldCrises>
  <Organization organizationIdent="WNG">
    <Name>Wyoming National Guard</Name>
    <Kind organizationKindIdent="Government"/>
    <Location>
      <Locality>Washington D.C.</Locality>
      <Region/>
      <Country>United States of America</Country>
    </Location>
    <History>Founded 1870-04-04.</History>
    <ContactInfo>
      <Telephone/>
      <Fax/>
      <Email/>
      <PostalAddress>
        <StreetAddress/>
        <Locality>Washington D.C.</Locality>
        <Region/>
        <PostalCode/>
        <Country>United States of America</Country>
      </PostalAddress>
    </ContactInfo>
    <ExternalResources>
      <ImageURL/>
    </ExternalResources>
    <RelatedCrises/>
    <RelatedPersons/>
  </Organization>
  <OrganizationKind organizationKindIdent="Government">
    <Name>Government</Name>
    <Description/>
  </OrganizationKind>
</WorldCrises>""")  
        w = StringIO.StringIO()
        WCDB2_solve(r, w)
        self.assert_(w.getvalue() == """<WorldCrises>
  <Organization organizationIdent="WNG">
    <Name>Wyoming National Guard</Name>
    <Kind organizationKindIdent="Government"/>
    <Location>
      <Locality>Washington D.C.</Locality>
      <Region/>
      <Country>United States of America</Country>
    </Location>
    <History>Founded 1870-04-04.</History>
    <ContactInfo>
      <Telephone/>
      <Fax/>
      <Email/>
      <PostalAddress>
        <StreetAddress/>
        <Locality>Washington D.C.</Locality>
        <Region/>
        <PostalCode/>
        <Country>United States of America</Country>
      </PostalAddress>
    </ContactInfo>
    <ExternalResources>
      <ImageURL/>
    </ExternalResources>
    <RelatedCrises/>
    <RelatedPersons/>
  </Organization>
  <OrganizationKind organizationKindIdent="Government">
    <Name>Government</Name>
    <Description/>
  </OrganizationKind>
</WorldCrises>
""")  
        
    def test_solve_3(self):
        w  = StringIO.StringIO()
        r = StringIO.StringIO("""<WorldCrises>
  <Person personIdent="RJoseph">
    <Name>
      <FirstName/>
      <MiddleName/>
      <LastName/>
      <Suffix/>
    </Name>
    <Kind personKindIdent="Official"/>
    <Location>
      <Locality/>
      <Region/>
      <Country/>
    </Location>
    <ExternalResources>
      <ImageURL/>
    </ExternalResources>
    <RelatedCrises/>
    <RelatedOrganizations/>
  </Person>
  <PersonKind personKindIdent="Official">
    <Name>Official</Name>
    <Description/>
  </PersonKind>
</WorldCrises>""")
        WCDB2_solve(r, w)
        self.assert_(w.getvalue() == """<WorldCrises>
  <Person personIdent="RJoseph">
    <Name>
      <FirstName/>
      <MiddleName/>
      <LastName/>
      <Suffix/>
    </Name>
    <Kind personKindIdent="Official"/>
    <Location>
      <Locality/>
      <Region/>
      <Country/>
    </Location>
    <ExternalResources>
      <ImageURL/>
    </ExternalResources>
    <RelatedCrises/>
    <RelatedOrganizations/>
  </Person>
  <PersonKind personKindIdent="Official">
    <Name>Official</Name>
    <Description/>
  </PersonKind>
</WorldCrises>
""")

# ----
# main
# ----

print("TestWCDB2.py")
unittest.main()
print("Done.")
