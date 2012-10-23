# coding=utf-8
from plone.app.form._named import named_template_adapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#def archetypes.referencebrowserwidget
default_popup_template = named_template_adapter(
    ViewPageTemplateFile('popupReferenceWidget.pt'))