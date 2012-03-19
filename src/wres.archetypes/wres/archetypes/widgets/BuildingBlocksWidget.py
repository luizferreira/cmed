# coding=utf-8

from AccessControl import ClassSecurityInfo

from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.public import ReferenceWidget
from Products.Archetypes.public import DisplayList

from Products.CMFCore.Expression import Expression
from Products.CMFCore.Expression import createExprContext
from Products.CMFCore.utils import getToolByName

def getAttributeValue(obj, attr_name, **extras):
    attr = getattr(obj, attr_name)
    if callable(attr):
        return attr(**extras)
    return attr

class BuildingBlocksWidget(ReferenceWidget):
    _properties = ReferenceWidget._properties.copy()
    _properties.update({'macro':'building_blocks_widget_template',
                        'helper_js': ('uemr_widgets/js/buildingblockswidget.js',),
                        'blocks': (),
                        'vocabulary_display_path_bound': 100,
                        'filter_vocabulary': (),
                       })

    security = ClassSecurityInfo()

    security.declarePublic('getBlock')
    def getBlock(self, id):
        for block in self.blocks:
            if block['id'] == id:
                return block
        return {}

    def getSpecialVocabulary(self, instance, field):
        """ """
        field.vocabulary_display_path_bound = self.vocabulary_display_path_bound
        filter_vocabulary = self.filter_vocabulary
        if filter_vocabulary:
            if len(filter_vocabulary) > 2:
                method_id = filter_vocabulary[2]
                method = getattr(instance, method_id)
                return method()
            related_field = self.getRelatedField(instance, field)
            if related_field:
                self.this_vocabulary = field.Vocabulary(instance)
                related_value = instance[related_field.accessor]()
                extended = self.getExtendedVocabulary(instance)
                extended['default'] = extended[related_value]
                return extended
        self.this_vocabulary = field.Vocabulary(instance)
#       A modificação abaixo é para contornar um problema na migração
#       dessa widget. É importante destacar que ela faz com que a widget
#       não use mais o seu vocabulário (Em P3 isso já não funcionava).        
        return {'default': []}
#        return {'default': self.this_vocabulary}

    def getExtendedVocabulary(self, instance):
        """ """
        items = self.this_vocabulary.items()
        ref_objs = self.getReferencedObjs(instance, items)
        filter_attr_id = self.filter_vocabulary[0]
        splitted = self.splitListByAttrValue(filter_attr_id, ref_objs)
        result = {}
        for key in splitted.keys():
            result[key] = self.objs2DisplayList(splitted[key])
        return result

    def objs2DisplayList(self, objs):
        uids = [obj.UID() for obj in objs[:10]]
        items = self.this_vocabulary.items()
        filtered = [item for item in items if item[0] in uids]
        return DisplayList(filtered)

    def splitListByAttrValue(self, attr_name, list_objs):
        """ break a list of objects in sublists based on the value of an
        attribute of the object. The result will be a dict where the keys are
        the attribute values and the values are the sublists."""
        result = {}
        for obj in list_objs:
            attr_value = getAttributeValue(obj, attr_name)
            if not result.has_key(attr_value):
                result[attr_value] = []
            result[attr_value].append(obj)
        return result

    def getReferencedObjs(self, instance, items):
        rc = getToolByName(instance, 'reference_catalog')
        return [rc.lookupObject(item[0]) for item in items]

    def getRelatedField(self, instance, field):
        """ """
        if self.filter_vocabulary[1].startswith('$'):
            related_field_id = self.filter_vocabulary[1][1:]
            return instance.getField(related_field_id)
        return None

    security.declarePublic('eval')
    def eval(self, source, globals=None, locals=None):
        """ must be improved. XXX where this is used?"""
        if globals and locals:
            return eval(source, globals, locals)
        elif globals:
            return eval(source, globals)
        elif locals:
            return eval(source, locals=locals)
        else:
            return eval(source)

    def base_url(self, instance, field):
        #the next line should be like that only when instance is being created
        #in the way we're doing with Visits
        base = instance.aq_parent.absolute_url()
        return base

    def _quick_register_querystring(self, instance, field, template=True):
        def get_default_values(instance, block, replace_variables):
            default_values = block.get('default_values', {})
            if default_values:
                result = []
                for name, description  in default_values.items():
                    if replace_variables:
                        related_field = None
                        if description[0].__class__ == ''.__class__ and description[0].startswith('$'):
                            related_field = instance.getField(description[0][1:])
                        if related_field:
                            accessor = related_field.accessor
                            result.append('%s=%s'%(name, instance[accessor]()))
                    else:
                        result.append('%s=%s'%(name, description[0]))
                return '&' + '&'.join(result)
            return ''

        field_id = field.getName()
        block = self.getBlock('popup_quick_register')
        replace_variables = not template
        default = get_default_values(instance, block, replace_variables)

        return ('field_id=%s' % field_id) + default

    def quick_register_onclick(self, instance, field, template=False):
        base = self.base_url(instance, field)
        qs = self._quick_register_querystring(instance, field, template)
        opener_type = instance.meta_type
        url = '%s/popup_quick_register_script?%s&opener_type=%s' % (base, qs,
                                                                    opener_type)
        target = '_blank'
        parameters = 'width=355,height=520,scrollbars=yes,resizable=yes'
        return "window.open('%s', '%s', '%s')" % (url, target, parameters)

    def _popup_search_querystring(self, instance, field, block, template):
        script_id = block.get('script', 'popup_search_script')
        script = getattr(instance, script_id)()
        if template:
            qs = script(field)
        else:
            qs = script(field, replace_variables=True)
        return qs

    def popup_search_onclick(self, instance, field, block, template=False):
        base = self.base_url(instance, field)
        qs = self._popup_search_querystring(instance, field, block, template)
        opener_type = instance.meta_type
        template_id = block.get('search_template', 'popup_search_template')
        # a inclusao destes parametros na string faz com que o topo nao seja carregado
        not_load_top = "ajax_load=1&ajax_include_head=1"
        url = '%s/%s?%s&opener_type=%s&%s' % (base, template_id, qs, opener_type, not_load_top)
        target = '_blank'
        parameters = 'width=800,height=525,scrollbars=yes,resizable=yes'
        return "window.open('%s','%s','%s')" % (url, target, parameters)

registerWidget(BuildingBlocksWidget,
               title="Building Blocks Widget",
               description="",
               used_for=('Products.Archetypes.Field.ReferenceField',),
               )
