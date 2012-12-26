from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from repoze.catalog.catalog import Catalog
from repoze.catalog.document import DocumentMap

class CmedCatalogTool(SimpleItem):
    """ Manage persistent dynamic vocabularies. """

    # General properties
    security = ClassSecurityInfo()
    plone_tool = 1
    id = 'cmed_catalog_tool'
    meta_type = 'VocabularyTool'
    catalogs = []

    def add_catalog(self, catalog_id):
        setattr(self, catalog_id, Catalog())
        setattr(self, catalog_id+'_map', DocumentMap())
        self.catalogs.append(catalog_id)
        return getattr(self, catalog_id)

    def catalog_obj(self, catalog_id, obj):
        try:
            catalog = getattr(self, catalog_id)
            doc_map = getattr(self, catalog_id+'_map')
        except:
            raise Exception("Catalog "+catalog_id+" doenst exist.")

    def clear_catalog(self, catalog_id):
        try:
            catalog = getattr(self, catalog_id)
            doc_map = getattr(self, catalog_id+'_map')
        except:
            raise Exception("Catalog "+catalog_id+" doenst exist.")
        setattr(self, catalog_id, Catalog())
        setattr(self, catalog_id+'_map', DocumentMap())


