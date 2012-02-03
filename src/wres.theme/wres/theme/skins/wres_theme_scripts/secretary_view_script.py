##bind container=container
##bind context=context

from DateTime import DateTime

def break_in_groups(list, num):
    groups = []
    stack = []
    while len(list) > 0:
        for i in range(0,num):
            if len(list) != 0:
                stack.append(list.pop(0))
        groups.append(stack)
        stack = []
    return groups

schema = context.Schema()

schematas = schema.getSchemataNames()

lista = []
i=0

for schemata in schematas:
    if schemata not in ['main', 'dates', 'categorization', 'settings', 'default', 'ownership']:
        fields = schema.getSchemataFields(schemata)
        fields_non_empty = []
        for f in fields:
            value = f.getAccessor(context)()
            if value:
                tupla = (f, value)
                fields_non_empty.append(tupla)
        if len(fields_non_empty) is not 0:
            lista.append([schemata])
            groups = break_in_groups(fields_non_empty, 3)
            lista[i].append(groups)
            i+=1
return lista
