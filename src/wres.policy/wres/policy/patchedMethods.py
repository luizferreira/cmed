# coding=utf-8
#-------------------Imports for patchedUpdate function----------------------------------
from types import ListType, TupleType
import urllib

import zope.interface

from zope.component import getAdapter
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.formlib import namedtemplate

from Acquisition import aq_inner
from Acquisition import aq_base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from plone.app.layout.navigation.root import getNavigationRoot

try:
    # Zope >= 2.13
    from AccessControl.security import checkPermission
except ImportError:
    from Products.Five.security import checkPermission

from Products.ZCTextIndex.ParseTree import ParseError

from plone.app.form._named import named_template_adapter

from Products.Archetypes.config import REFERENCE_CATALOG
from Products.CMFCore.utils import getToolByName
try:
    from plone.uuid.interfaces import IUUID
    HAS_UUID = True
except ImportError:
    HAS_UUID = False
try:
    # Plone >= 4.0
    from plone.sequencebatch import Batch
except ImportError:
    # Plone <= 3.x
    from Products.CMFPlone.PloneBatch import Batch

from archetypes.referencebrowserwidget import utils
from archetypes.referencebrowserwidget.interfaces import IFieldRelation
from archetypes.referencebrowserwidget.interfaces import \
        IReferenceBrowserHelperView
#-------------------Imports for patchedUpdate function----------------------------------
#Arquivo usado para definição de funções custom chamadas pelo collective.monkeypatcher

#Solgema
def patchedGetCustomTitleFormat(self):
    if self.portal_language in ['fr']:
        return '{month: "MMMM yyyy", week: "d[ MMM][ yyyy]{ \'-\' d MMM yyyy}", day: \'dddd, d MMMM yyyy\'}'
    elif self.portal_language in ['de']:
        return '{month: \'MMMM yyyy\', week: "d[ yyyy].[ MMMM]{ \'- \'d. MMMM yyyy}", day: \'dddd, d. MMMM yyyy\'}'
    elif self.portal_language in ['pt']:
        return '{month: \'MMMM yyyy\', week: "d \'de\' MMMM{ \'- \'d \'de\' MMMM yyyy}", day: "dddd, d \'de\' MMMM yyyy"}'
    else:
        return '{month: \'MMMM yyyy\', week: "MMM d[ yyyy]{ \'-\'[ MMM] d yyyy}", day: \'dddd, MMM d, yyyy\'}'
        
def patchedColumnFormat(self):
    if self.portal_language in ['de']:
        return "{month: 'ddd', week: 'ddd d. MMM', day: 'dddd d. MMM'}"
    elif self.portal_language in ['pt']:
        return "{month: 'ddd', week: 'ddd dd/MM', day: 'ddd dd/MM'}"
    else: 
        return "{month: 'ddd', week: 'ddd M/d', day: 'dddd M/d'}"
        
def patchedGetHourFormat(self):
    if self.portal_language in ['fr', 'de', 'it', 'pt']:
        return 'HH:mm'
    else:
        return 'h(:mm)tt'

def patchedUpdate(self):
    context = aq_inner(self.context)

    catalog = getToolByName(context, 'portal_catalog')
    at_result = catalog.searchResults(dict(path={'query': self.at_url,
                                                 'depth': 0}))
    at_brain = len(at_result) == 1 and at_result[0] or None
    if at_brain:
        self.at_obj = at_brain.getObject()
        self.has_brain = True
        self.brainuid = at_brain.UID
    else:
        self.at_obj = context.restrictedTraverse(urllib.unquote(self.at_url))
    self.field = self.at_obj.Schema()[self.fieldRealName]
    self.widget = self.field.widget
    self.multiValued = int(self.field.multiValued)
    self.search_index = self.request.get('search_index',
                                         self.widget.default_search_index)
    self.request.set(self.search_index, self.search_text)

    base_query = self.widget.getBaseQuery(self.at_obj, self.field)
    self.allowed_types = base_query.get('portal_type', '')
    if not self.allowed_types:
        base_query.pop('portal_type')

    if base_query.keys():
        self.request.form.update(base_query)

    # close_window needs to be int, since it is used
    # with javascript
    self.close_window = int(not self.field.multiValued or
                            self.widget.force_close_on_insert)
    self.template = getAdapter(self, namedtemplate.INamedTemplate,'popup_cmed')
    self._updated = True
