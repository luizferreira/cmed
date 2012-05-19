import unittest2 as unittest
from wres.policy.testing import WRES_POLICY_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName

class TestSetup(unittest.TestCase):
    
    layer = WRES_POLICY_INTEGRATION_TESTING
    
    def test_portal_title(self):
        print "Teste se o produto foi instalado"
        portal = self.layer['portal']
        self.assertEqual("CommuniMed", portal.getProperty('title'))
