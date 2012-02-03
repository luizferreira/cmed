from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from Acquisition import aq_base, aq_parent, aq_inner

def add_types_to_portal_factory(portal, types=()):
    portal_factory = portal.portal_factory
    old_types = portal_factory.getFactoryTypes().keys()
    new_types = tuple(old_types) + tuple(types)
    portal_factory.manage_setPortalFactoryTypes(listOfTypeIds=new_types)

def install_product(portal, product):
    qi = portal.portal_quickinstaller
    if not qi.isProductInstalled(product):
        qi.installProduct(product)
        # Refresh skins
        if shasattr(portal, '_v_skindata'):
            portal._v_skindata = None
        if shasattr(portal, 'setupCurrentSkin'):
            portal.setupCurrentSkin()
        print '   Installed %s' % product
    else:
        print '   %s already installed' % product

def install_dependencies(self, dependencies=()):
    for dependency in dependencies:
        try:
            install_product(self, dependency)
        except:
            print '%s already installed' % dependency
    return True

def create_metadatas(portal, names, catalog='portal_catalog'):
    pc = getToolByName(portal, catalog)
    schema = pc.schema()
    for name in names:
        if name not in schema:
            pc.addColumn(name)

class DictWrapper:
    def __init__(self, dict):
        self.dict = dict
    def __getattr__(self, item):
        return self.dict[item]

def add_index(portal, name, type, extra=None, catalog='portal_catalog'):
    catalog = getToolByName(portal, catalog)
    if not name in catalog.indexes():
        #this conditional is needed because of a bug in zope 2.7.4
        #if we passed a dictionary, the attributes would be ignored
        if extra is not None:
            extra = DictWrapper(extra)
        catalog.addIndex(name, type, extra=extra)

def add_layer(portal, layer, skin, index="custom"):
    layers = portal.portal_skins.getSkinPath(skin)
    path = layers.split(',')
    if layer in path:
        position = path.index(layer)
        path.pop(position)
    if index in path:
        position = path.index(index)
    else:
        position = -1
    path.insert(position+1, layer)
    layers = ','.join(path)
    portal.portal_skins.addSkinSelection(skin, layers)
    return layers

def install_reinstall_types(portal, types_install, types_reinstall,
                            package='CMFUEMR'):
    at = portal.archetype_tool
    for type in types_install:
        at.manage_installType(typeName=type, package=package)

    for type in types_reinstall:
        at.manage_installType(typeName=type, uninstall=1)
        at.manage_installType(typeName=type, package=package)

def reindex_objects(portal, contenttype):
    pc = getToolByName(portal, 'portal_catalog')
    brains = pc.search({'meta_type': contenttype})
    objs = [b.getObject() for b in brains]
    objs_size = len(objs)
    for obj in objs:
        obj.reindexObject()
        print "Contagem Regressiva: " + str(objs_size)
        objs_size -= 1

def reinstall_workflow(portal, workflow_id):
    def _workflow_type(workflow_object):
        return "%s (%s)" % (workflow_object.id, workflow_object.title)
    portal_workflow = portal.portal_workflow
    if hasattr(portal_workflow, workflow_id):
        workflow_object = getattr(portal_workflow, workflow_id)
        workflow_type = _workflow_type(workflow_object)
        portal_workflow.manage_delObjects([workflow_id])
        portal_workflow.manage_addWorkflow(workflow_type, workflow_id)

def associate_metatype_to_workflow(self, meta_type, workflow_id):
    self.portal_workflow.setChainForPortalTypes([meta_type], [workflow_id])

def inheritAllPermissions(self):
    perms = self.possible_permissions()
    self.manage_acquiredPermissions(perms)

def create_cache_manager(obj, id, request_vars=[]):
    if not hasattr(obj, id):
        factory = obj.manage_addProduct['StandardCacheManagers'].\
                  manage_addRAMCacheManager
        factory(id)
        cache_manager = getattr(obj, id)
        current = cache_manager.getSettings()
        current['request_vars'] = request_vars
        cache_manager.manage_editProps(id, settings=current)

def add_tools(portal, tools):
    addTool = portal.manage_addProduct['CMFUEMR'].manage_addTool
    for tool in tools:
        try: addTool(tool, None)
        except: pass

def set_security(obj, to_set = {}, to_unset = {}):
    for role, new_perms in to_set.items():
        permissions = obj.permissionsOfRole(role)
        my_filter = lambda x: x['selected']
        selected_permissions = filter(my_filter, permissions)
        selected_permissions = [item['name'] for item in selected_permissions]
        selected_permissions.extend(new_perms)
        obj.manage_role(role, selected_permissions)

def add_types_portal_factory(portal, types=[]):
    portal_factory = portal.portal_factory
    old_types = portal_factory.getFactoryTypes().keys()
    types = tuple(types)
    old_types = tuple(old_types)
    new_types = old_types + types
    portal_factory.manage_setPortalFactoryTypes(listOfTypeIds=new_types)

def updateRoleMappingsById(self, workflow_id):
    wfs = {}
    wf = self.getWorkflowById(workflow_id)
    if hasattr(aq_base(wf), 'updateRoleMappingsFor'):
        wfs[id] = wf
    portal = aq_parent(aq_inner(self))
    count = self._recursiveUpdateRoleMappings(portal, wfs)
    return count
