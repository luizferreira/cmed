from Products.CMFCore.utils import getToolByName
from wres.policy.utils.utils import getWresSite
from DateTime import DateTime

vt = getToolByName(context,"vocabulary_tool")
Versao = vt.get_vocabulary("cmed_version")
DataVersao = vt.get_vocabulary("cmed_data")

return "Versão {versao} de {data}".format(versao="".join(Versao), data="".join(DataVersao))