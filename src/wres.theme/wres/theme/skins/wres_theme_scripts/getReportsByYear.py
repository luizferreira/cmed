##parameters=year, type, index

from Products.CMFCore.utils import getToolByName

ano = year #ano pesquisado
ano_passado = str(int(ano)-1)

months = {'Jan':(DateTime(ano+'-01-01 00:00:00.000 US/Eastern'),DateTime(ano+'-01-31 23:59:00.000 US/Eastern')),
          'Feb':(DateTime(ano+'-02-01 00:00:00.000 US/Eastern'),DateTime(ano+'-02-28 23:59:00.000 US/Eastern')),
          'Mar':(DateTime(ano+'-03-01 00:00:00.000 US/Eastern'),DateTime(ano+'-03-31 23:59:00.000 US/Eastern')),
          'Apr':(DateTime(ano+'-04-01 00:00:00.000 US/Eastern'),DateTime(ano+'-04-30 23:59:00.000 US/Eastern')),
          'May':(DateTime(ano+'-05-01 00:00:00.000 US/Eastern'),DateTime(ano+'-05-31 23:59:00.000 US/Eastern')),
          'Jun':(DateTime(ano+'-06-01 00:00:00.000 US/Eastern'),DateTime(ano+'-06-30 23:59:00.000 US/Eastern')),
          'Jul':(DateTime(ano+'-07-01 00:00:00.000 US/Eastern'),DateTime(ano+'-07-31 23:59:00.000 US/Eastern')),
          'Aug':(DateTime(ano+'-08-01 00:00:00.000 US/Eastern'),DateTime(ano+'-08-31 23:59:00.000 US/Eastern')),
          'Sep':(DateTime(ano+'-09-01 00:00:00.000 US/Eastern'),DateTime(ano+'-09-30 23:59:00.000 US/Eastern')),
          'Oct':(DateTime(ano+'-10-01 00:00:00.000 US/Eastern'),DateTime(ano+'-10-31 23:59:00.000 US/Eastern')),
          'Nov':(DateTime(ano+'-11-01 00:00:00.000 US/Eastern'),DateTime(ano+'-11-30 23:59:00.000 US/Eastern')),
          'Dec':(DateTime(ano+'-12-01 00:00:00.000 US/Eastern'),DateTime(ano+'-12-31 23:59:00.000 US/Eastern')),
         }

result = {}
result['year'] = year

pesquisa = index #indice pesquisado
tipo = type #tipo pesquisado (string vazio '' para pesquisar todos)

pc = getToolByName(context, 'portal_catalog')

contador = 0
results = pc({pesquisa: {'query':(DateTime(ano+'-01-01 00:00:00.000 US/Eastern'),DateTime(ano+'-12-31 23:59:00.000 US/Eastern')),'range': 'min:max'}}, meta_type = tipo)

#Conta o total de visitas em 1 ano:
for register in results:
    #print register.getObject()
    contador = contador + 1
result['contador'] = str(contador)

#Conta total de visitas por mes:
for key in months:
    contador = 0
    results = pc({pesquisa: {'query':months[key],'range': 'min:max'}}, meta_type = tipo)
    for register in results:
        contador = contador+1
    result[str(key)] = contador

return result
