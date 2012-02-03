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
          'collective.quickupload == 1.3.1',
          'Products.Clouseau == 1.0',
          'wres.brfields',
          'wres.archetypes',
          'wres.theme',
          # 'PIL==1.1.6',
          # Pillow e lxml sao p413
          # -*- Extra requirements: -*-
      ],
      extras_require = {
          'test': [
                  'plone.app.testing',
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
