##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field, related_field, button, url
fieldname = field.getName()
object = '%s_%s' % (button, fieldname)
if related_field:
    js = """
    <!--
    var other = document.getElementById('popup_%(button)s_%(fieldname)s');
    if(other){
        var %(object)s = new MyObject(other, '%(related_field)s', '%(url)s', other.getAttribute('onclick_template'));
        var to_observe = getInputsElementByName('%(related_field)s');
        for(var i=0; i<to_observe.length; i++){
            if(to_observe[i].addEventListener){
                to_observe[i].addEventListener("change", function(e){%(object)s.changeQs(e)}, false);
            }
            else{
                to_observe[i].attachEvent("onchange", function(){ %(object)s.changeQs()});
            }
        }
    }
    -->""" % {'fieldname': fieldname,
              'related_field': related_field.getName(),
              'object': object,
              'button': button,
              'url': url,
              }
else:
    js = """ """

return js