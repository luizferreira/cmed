##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=special_vocab, field, related_field
##
fieldname = field.getName()
related = related_field
current_key = context[related.accessor]()
str_keys = ', '.join([("'%s'" % key) for key in special_vocab.keys() \
                      if key != 'default'])
if str_keys:
    str_keys = ', ' + str_keys
controller = "var controller_%(fieldname)s = new VocabularyController('%(fieldname)s:list', '%(current_key)s'%(str_keys)s);\n"\
              % {'fieldname': fieldname,
                 'current_key': current_key,
                 'str_keys': str_keys}
for key, vocab in special_vocab.items():
    if key != 'default':
        controller += "var aux = controller_%s;\n" % fieldname
        for entry in vocab.items():
            controller += "aux.addElementVocabulary('%s', %s);\n"\
                          % (key, str(list(entry)))
controller += \
""" var to_observe = getInputsElementByName('%(related_field)s');
    for(var i=0; i<to_observe.length; i++){
        if(to_observe[i].addEventListener){
            to_observe[i].addEventListener("change", function(e){controller_%(fieldname)s.changeList(e)}, false);
        }
        else{
            to_observe[i].attachEvent("onclick", function(){controller_%(fieldname)s.changeList()});
        }
    }
""" % {'related_field': related.getName(), 'fieldname': fieldname}

return controller