from Products.CMFCore.utils import getToolByName
from wres.policy.utils.utils import getWresSite
from DateTime import DateTime

today = DateTime()
last_update = today - today.week() - 1

return "Última atualização em " + last_update.strftime('%d/%m/%Y')

# vt = getToolByName(context,"vocabulary_tool")
# Versao = vt.get_vocabulary("cmed_version")
# DataVersao = vt.get_vocabulary("cmed_data")

# return "Versão {versao} de {data}".format(versao="".join(Versao), data="".join(DataVersao))