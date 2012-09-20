from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from zope.configuration import xmlconfig
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName
import gocept.selenium.plonetesting.testing_plone
import gocept.selenium.plonetesting.testing
import plone.app.testing.layers

DOCTOR_TEST_USER_ID = 'doctor_test_user_id'
DOCTOR_TEST_USER_NAME = 'doctor_test_user_name'
SECRETARY_TEST_USER_ID = 'secretary_test_user_id'
SECRETARY_TEST_USER_NAME = 'secretary_test_user_name'
PATIENT_TEST_USER_ID = 'patient_test_user_id'
PATIENT_TEST_USER_NAME = 'patient_test_user_name'

MANAGER_ROLES = ['Manager']
DOCTOR_ROLES = ['Manager','Doctor', 'Member', 'Contributor', 'Reviewer']
SECRETARY_ROLES = ['Secretary', 'Member', 'Contributor']
PATIENT_ROLES = ['Patient', 'Member']

# TEST_USER_ID = 'admin'

def create_uemr_user(portal, user_id, group, email='', fullname=''):
    pr = getToolByName(portal, 'portal_registration')
    pm = getToolByName(portal, 'portal_membership')
    uf = getToolByName(portal, 'acl_users')
    if email == '':
        email = 'sem@email.com'
    pr.addMember(
        user_id, 'senha1',
        properties={
            'username': user_id,
            'email': email,
            'fullname': fullname,
        },
    )
    uf.userSetGroups(user_id, [group])
    pm.createMemberArea(member_id=user_id) 


class WresPolicy(PloneSandboxLayer):

	defaultBases = (PLONE_FIXTURE,)
        
	def setUpZope(self, app, configurationContext):
		# Load ZCML
		import wres.policy
		import wres.archetypes
		import wres.brfields
		import wres.theme
		import wres.tour

		xmlconfig.file('configure.zcml',
			wres.archetypes,
			context=configurationContext)

		# Instala o produto que utiliza o antigo initialize(). No
		# caso do wres.archetypes eh necessario porque ele instala
		# algumas coisas relacionadas com os seus Archetypes atraves
		# do initialize do seu __init__.py (e.g as permissoes de adicao
		# dos Arquetypes).
		z2.installProduct(app, 'wres.archetypes')

		xmlconfig.file('configure.zcml',
			wres.brfields,
			context=configurationContext)

		z2.installProduct(app, 'wres.brfields')
			
		xmlconfig.file('configure.zcml',
			wres.theme,
			context=configurationContext)		
			
		z2.installProduct(app, 'wres.theme')				
		
		# xmlconfig.file('configure.zcml',
		# 	wres.tour,
		# 	context=configurationContext)

		# z2.installProduct(app, 'wres.tour')

		xmlconfig.file('configure.zcml',
			wres.policy,
			context=configurationContext)

		z2.installProduct(app, 'wres.policy')


	def setUpPloneSite(self, portal):
        	applyProfile(portal, 'wres.archetypes:default')
		applyProfile(portal, 'wres.brfields:default')
		applyProfile(portal, 'wres.theme:default')
#		applyProfile(portal, 'wres.tour:default')
		applyProfile(portal, 'wres.policy:default')
                

		#create_uemr_user(portal, DOCTOR_TEST_USER_ID, 'Doctor')

	def tearDownZope(self, app):
		z2.uninstallProduct(app, 'wres.archetypes')
		z2.uninstallProduct(app, 'wres.brfields')
		z2.uninstallProduct(app, 'wres.theme')	
	#	z2.uninstallProduct(app, 'wres.tour')	
		z2.uninstallProduct(app, 'wres.policy')

class WresPolicySelenium(PloneSandboxLayer):

	defaultBases = (gocept.selenium.plonetesting.testing.layer,PLONE_FIXTURE,)
       
	def setUpZope(self, app, configurationContext):
		# Load ZCML
		import wres.policy
		import wres.archetypes
		import wres.brfields
		import wres.theme
		import wres.tour

		xmlconfig.file('configure.zcml',
			wres.archetypes,
			context=configurationContext)

		z2.installProduct(app, 'wres.archetypes')

		xmlconfig.file('configure.zcml',
			wres.brfields,
			context=configurationContext)

		z2.installProduct(app, 'wres.brfields')
			
		xmlconfig.file('configure.zcml',
			wres.theme,
			context=configurationContext)		
			
		z2.installProduct(app, 'wres.theme')				
		
		# xmlconfig.file('configure.zcml',
		# 	wres.tour,
		# 	context=configurationContext)

		# z2.installProduct(app, 'wres.tour')

		xmlconfig.file('configure.zcml',
			wres.policy,
			context=configurationContext)

		z2.installProduct(app, 'wres.policy')


	def setUpPloneSite(self, portal):
        	applyProfile(portal, 'wres.archetypes:default')
		applyProfile(portal, 'wres.brfields:default')
		applyProfile(portal, 'wres.theme:default')
#		applyProfile(portal, 'wres.tour:default')
		applyProfile(portal, 'wres.policy:default')
                

		#create_uemr_user(portal, DOCTOR_TEST_USER_ID, 'Doctor')

	def tearDownZope(self, app):
		z2.uninstallProduct(app, 'wres.archetypes')
		z2.uninstallProduct(app, 'wres.brfields')
		z2.uninstallProduct(app, 'wres.theme')	
	#	z2.uninstallProduct(app, 'wres.tour')	
		z2.uninstallProduct(app, 'wres.policy')
		
		
WRES_POLICY_FIXTURE = WresPolicy()
WRES_POLICY_INTEGRATION_TESTING = IntegrationTesting(bases=(WRES_POLICY_FIXTURE,), name="WresPolicy:Integration")
WRES_POLICY_FUNCTIONAL_TESTING = FunctionalTesting(bases=(WRES_POLICY_FIXTURE,), name="WresPolicy:Functional")

WRES_POLICY_SELENIUM_FIXTURE = WresPolicySelenium()
WRES_POLICY_SELENIUM_FUNCTIONAL_TESTING = FunctionalTesting(bases=(WRES_POLICY_SELENIUM_FIXTURE,), name="WresPolicySelenium:Functional")
