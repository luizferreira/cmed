
# def make_transformation(old_str):
#     """
#     Trasform 'past_medical_history' to 'getPastMedicalHistory'
#     """
#     new_str = old_str.replace(old_str[0], old_str[0].upper(), 1)

#     pos = new_str.find('_')
#     while pos != -1:
#         ch = new_str[pos+1]
#         new_str = new_str.replace(ch, ch.upper(), 1)
#         new_str = new_str.replace('_', '', 1)
#         pos = new_str.find('_')

#     new_str = 'get' + new_str
#     return new_str

# chart_map = context.get_chart_data_map()
chart_data_summary = context.chart_data_summary()
chart_keys = chart_data_summary.keys()

resumo = []
for key in chart_keys:
    tupla = (key, getattr(context.chart_data, key))
    resumo.append(tupla)

# dics = {}
# for key in chart_keys:
#     try:
#         method = getattr(context, make_transformation(key))
#         value = method()
#     except:
#         #value = 'O atributo não possui interface de acesso.'
#         value = None
#     dics[key] = value

result = {}
result['resumo'] = resumo
# result['dics'] = dics
result['dics'] = chart_data_summary

return result
