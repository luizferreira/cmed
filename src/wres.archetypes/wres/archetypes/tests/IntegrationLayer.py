from Products.PloneTestCase import ptc
from plone.app.testing import PloneSandboxLayer


from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from zope.configuration import xmlconfig
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName
class WresArchetypes(PloneSandboxLayer):

	defaultBases = (PLONE_FIXTURE,)
        
	def setUpZope(self, app, configurationContext):
		# Load ZCML
		import wres.policy
		import wres.archetypes
		import wres.brfields
		import wres.theme

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
		
		xmlconfig.file('configure.zcml',
			wres.policy,
			context=configurationContext)

		z2.installProduct(app, 'wres.policy')


	def setUpPloneSite(self, portal):
		applyProfile(portal, 'wres.archetypes:default')
		applyProfile(portal, 'wres.brfields:default')
		applyProfile(portal, 'wres.theme:default')
		applyProfile(portal, 'wres.policy:default')
                

		#create_uemr_user(portal, DOCTOR_TEST_USER_ID, 'Doctor')

	def tearDownZope(self, app):
		z2.uninstallProduct(app, 'wres.archetypes')
		z2.uninstallProduct(app, 'wres.brfields')
		z2.uninstallProduct(app, 'wres.theme')	
		z2.uninstallProduct(app, 'wres.policy')
		
WRES_ARCHETYPES_FIXTURE = WresArchetypes()
WRES_ARCHETYPES_INTEGRATION_TESTING = IntegrationTesting(bases=(WRES_ARCHETYPES_FIXTURE,), name="WresArchetypes:Integration")
