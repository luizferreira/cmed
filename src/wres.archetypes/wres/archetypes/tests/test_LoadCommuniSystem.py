import unittest2 as unittest
from wres.archetypes.tests.IntegrationLayer import WRES_ARCHETYPES_INTEGRATION_TESTING

class TestSetup(unittest.TestCase):
    layer = WRES_ARCHETYPES_INTEGRATION_TESTING

    def test_LoadCommuniSystem(self):
        #Simple test just load the system layer
        print "\n"
        print "--------------------------------------"
        print "Testing Load Communi System start"
        print "Testing Load Communi System end"
        print "--------------------------------------"
