if context.meta_type == "Template":
    schema = context.Schema()
    schematas = schema.getSchemataNames()
    list_schemas = []
    for schemata in schematas:
        if schemata in ['main','Principal','dates','categorization','settings','ownership']:
            continue
        list_fields = schema.getSchemataFields(schemata)
        list_data = []
        list_data.append(schemata)
        for field in list_fields:
            value = field.getAccessor(context)()

            if value is "" or value is () or value is None or value is []:
                continue
            #Olhar se widget do tipo checkbox esta vazio
            if field.widget.getName() == "MultiSelectionWidget":
                brake=True
                for x in value:
                    if x is not '':
                        brake=False
                        continue
                if brake:
                    continue
            #Olhar se widget do tipo DataGrid com 2 colunas(dir,esq) está vazio, se sim, é ignorado.
            if field.widget.getName() == "DataGridWidget" and 'dir' in field.columns and 'esq' in field.columns:
                brake = True
                for i in range(len(field.getAccessor(context)())):
                    for y in value[i]['esq']:
                        if y is not '':
                            brake=False
                            continue
                    for y in value[i]['dir']:
                        if y is not '':
                            brake = False
                            continue
                if brake:
                    continue        
            #Ignorar Medico e Data, pegos pelo template cmed_document_view, no cabeçalho e rodapé
            field_name = field.getName()
            if field_name == 'doctor' or field_name == 'dateOfVisit' or field_name == 'date'  :
                continue
            if field_name == 'gdocument_body':
                tupla_name_label = (field_name,'')
            else:
                tupla_name_label = (field_name,field.widget.label)
            list_data.append(tupla_name_label)
        if len(list_data) > 1:
            list_schemas.append(list_data)
    return list_schemas
return None
