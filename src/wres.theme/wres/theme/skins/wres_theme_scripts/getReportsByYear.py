##parameters=year, type, index

from Products.CMFCore.utils import getToolByName

ano = year #ano pesquisado

#dicionário de retorno
result = {'year':year,'Jan':0,'Feb':0,'Mar':0,'Apr':0,'May':0,'Jun':0,'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0,}

pesquisa = index #indice pesquisado
tipo = type #tipo pesquisado (string vazio '' para pesquisar todos)

pc = getToolByName(context, 'portal_catalog')

results = pc({pesquisa: {'query':(DateTime(int(ano), 1,1) , DateTime(int(ano), 12, 31, 23, 59, 59)),'range': 'min:max'}}, meta_type = tipo)

#Conta o total de visitas em 1 ano:
result['contador'] = len(results)

#Conta total de visitas por mes:
for register in results:
    mes = getattr(register, index, '').strftime('%b')
    result[mes] = result[mes] + 1

return result
