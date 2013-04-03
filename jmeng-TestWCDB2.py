#!/usr/bin/env python

"""
To test the program:
% TestWCDB1.py >& TestWCDB1.out
"""

# -------
# imports
# -------

import StringIO
import unittest

from WCDB2 import *


# -----------
# TestWCDB1
# -----------

c = login()

class Node(object):
  
  ''' Test class to represent an ambiguous object with attribute "text". '''

  def __init__(self, text=None):
    self.text = text


class TestWCDB2(unittest.TestCase) :
  # -------
  # Login
  # -------
  
  def test_Login_1(self):
    conn = login()
    self.assert_(conn)

  #--------
  #Get_text
  #--------

  def test_get_text(self):
    node = Node()
    self.assert_(get_text(node) == '""')

  def test_get_text_2(self):
    node = Node()
    node.text = "some text"
    self.assert_(get_text(node) == '"some text"')

  def test_get_text_3(self):
    node = Node("more text")
    self.assert_(get_text(node) == '"more text"')

  #--------
  #Escape_quote
  #--------

  def test_escape_quote_1(self):
    text = 'test this " text'
    self.assert_(escape_quote(text) == 'test this \\" text')

  def test_escape_quote_2(self):
    text = 'try with two "" text'
    self.assert_(escape_quote(text) == 'try with two \\"\\" text')

  def test_escape_quote_3(self):
    text = 'test "" this " text'
    self.assert_(escape_quote(text) == 'test \\"\\" this \\" text')

  #--------
  #Import
  #--------

  def test_import_1(self):
    root = ET.parse("Acc_Test1.xml").getroot()
    wcdb2_import(root)
    self.assert_(query(c, 'SELECT * from Person') == ())
    self.assert_(query(c, 'SELECT * from Crisis') == ())
    self.assert_(query(c, 'SELECT * from Organization') == ())
    self.assert_(query(c, 'SELECT * from Location') == ())
    self.assert_(query(c, 'SELECT * from HumanImpact') == ())
    self.assert_(query(c, 'SELECT * from WaysToHelp') == ())

  def test_import_1(self):
    root = ET.parse("WCDB1.xml").getroot()
    wcdb2_import(root)
    t = query(c, 'SELECT * from Person')
    self.assert_(t == (('BHObama', 'Barack', 'Hussein', 'Obama', 'II', 'PR'), \
('OBLaden', 'Osama', 'bin Mohammed bin Awad', 'bin Laden', None, 'LD'), \
('GWBush', 'George', 'Walker', 'Bush', None, 'PR'), \
('JVStalin', 'Joseph', 'Vissarionovic', 'Stalin', None, 'LD'), \
('BHGates', 'Bill', 'Henry', 'Gates', 'III', 'PH'), \
('MHThatcher', 'Margaret', 'Hilda', 'Thatcher', None, 'PM'), \
('KPapoulias', 'Karolos', None, 'Papoulias', None, 'PR'), \
('JGZuma', 'Jacob', 'Gedleyihlekisa', 'Zuma', None, 'PR'), \
('AMRAl-Zawahiri', 'Ayman', 'Mohhammed Rabie', 'al-Zawahiri', None, 'LD'), \
('RNMcEntire', 'Reba', 'Nell', 'McEntire', None, 'SNG')))

  def test_import_3(self):
    root = ET.parse("Acc_Test2.xml").getroot()
    wcdb2_import(root)
    self.assert_(query(c, 'SELECT * from Person') == (('SLi', \
'Shirley', None, 'Li', None, 'PR'),))
    self.assert_(query(c, 'SELECT * from WaysToHelp') == (('1', \
'Shirley_WAR_2013', ''),))

  #--------
  #Export
  #--------
  
  def test_export_1(self):
    wcdb2_import(ET.fromstring("<WorldCrises/>"))
    outroot = wcdb2_export(c)
    outstring = ET.tostring(outroot, pretty_print=True)
    self.assert_(outstring == '<WorldCrises/>\n')

  def test_export_2(self):
    wcdb2_import(ET.fromstring("<WorldCrises></WorldCrises>"))
    outroot = wcdb2_export(c)
    outstring = ET.tostring(outroot, pretty_print=True)
    self.assert_(outstring == '<WorldCrises/>\n')

  def test_export_3(self):
    wcdb2_import(ET.parse("Acc_Test3.xml"))
    outroot = wcdb2_export(c)
    outstring = ET.tostring(outroot)
    self.assert_(outstring == '<WorldCrises><Crisis crisisIdent="Shirley_WAR_2013"><Name>2013 Great Attack of Shirley</Name><Kind crisisKindIdent="WAR"/><Location><Locality>Houston</Locality><Country>USA</Country></Location><StartDateTime><Date>2013-12-01</Date></StartDateTime><HumanImpact><Type>Death</Type><Number>2147483647</Number></HumanImpact><EconomicImpact></EconomicImpact><ResourceNeeded></ResourceNeeded><WaysToHelp></WaysToHelp><ExternalResource/><RelatedPersons/><RelatedOrganizations/></Crisis><CrisisKind crisisKindIdent="WAR"><Name>War</Name><Description>An organized and often "prolonged conflict is carried out by states and/or non-state actors.</Description></CrisisKind><OrganizationKind organizationKindIdent="HO"><Name>Humanitarian Organization</Name><Description>Organization that provides humanitarian aid</Description></OrganizationKind><PersonKind personKindIdent="PR"><Name>President</Name><Description>Leader or the government of some countries</Description></PersonKind></WorldCrises>')


# main
# ----

print "TestWCDB2.py"
unittest.main()
print "done."
