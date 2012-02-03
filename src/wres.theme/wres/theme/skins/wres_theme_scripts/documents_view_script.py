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
        datagrid_fields = []
        for f in fields:
            value = f.getAccessor(context)()
            if isinstance(value, DateTime):
                value = value.strftime('%d/%m/%Y')
            if f.getName() == 'doctor':
                value = value.getFullName()
            if value:
                tupla = (f, value)
                if f.getWidgetName() == 'DataGridWidget':
                    datagrid_fields.append(tupla)
                else:
                    fields_non_empty.append(tupla)
        if len(fields_non_empty) is not 0 or len(datagrid_fields) is not 0:
            lista.append([schemata])
            groups = break_in_groups(fields_non_empty, 3)
            if len(datagrid_fields) is not 0:
                for j in range(len(datagrid_fields)):
                    groups.append([datagrid_fields[j]])
            lista[i].append(groups)
            
            
            i+=1
            

                       
                      
return lista
