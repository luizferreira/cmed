from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='wres.policy',
      version=version,
      description="Policy product for WRES website",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['wres'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'Products.Archetypes',
          'plone.app.portlets',
          'Pillow',
          'lxml',
          'Solgema.fullcalendar == 1.9',
          'Products.DataGridField == 1.8b2',
          'collective.quickupload == 1.5.2',
          'Products.Clouseau == 1.0',
          'repoze.catalog == 0.8.2',
          'requests == 2.20.0',
          # 'Products.TinyMCE == 1.2.14',
          'Products.TinyMCE',
          'plone.api',
          'wres.brfields',
          'wres.archetypes',
          'wres.theme',
          'wres.tour',
          # 'PIL==1.1.6',
          # Pillow e lxml sao p413
          # -*- Extra requirements: -*-
      ],
      extras_require = {
          'test': [
                  'plone.app.testing',
                  'Products.PloneTestCase',
                  'collective.testcaselayer',
                  'selenium',
                  'gocept.selenium[plone]',
              ]
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
