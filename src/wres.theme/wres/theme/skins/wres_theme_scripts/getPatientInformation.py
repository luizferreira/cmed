##bind context=context

#return {'getLastVisitDate': context.getLastVisitDate(), 'getContactPhone': context.getContactPhone(), 'UID': context.UID(), 'getExt': context.getExt()}

return context.getInformation()
