#from Products.CMFCore.utils import getToolByName

#def getPortal(self):
    #utool = getToolByName(self, 'portal_url')
    #return utool.getPortalObject()

#def getWhoAmI(context):
    #list1 = []
    #portal = getPortal(context)
    #ms = portal.portal_membership
    #mb = ms.getAuthenticatedMember()
    #list1.append(mb.getId())
    #list1.append(mb.getRoles())
    #lista.append(list1)

#def getAllDoctors(self):
    #list2 = []
    #pc = getToolByName(self,"portal_catalog")
    #brs = pc.search({"meta_type":"Doctor"})
    #for br in brs:
        #list2.append(br.getObject().getId())
        ##import ipdb;ipdb.set_trace()
    #lista.append(list2)

#def getAllSecretaries(self):
    #list3 = []
    #pc = getToolByName(self,"portal_catalog")
    #brs = pc.search({"meta_type":"Secretary"})
    #for br in brs:
        #list3.append(br.getObject().getId())
        ##import ipdb;ipdb.set_trace()
    #lista.append(list3)

#def getAllAdmins(self):
    #list4 = []
    #pc = getToolByName(self,"portal_catalog")
    #brs = pc.search({"meta_type":"Manager"})
    #for br in brs:
        #list4.append(br.getObject().getId())
        ##import ipdb;ipdb.set_trace()
    #lista.append(list4)

#def getAllPatients(self):
    #list5 = []
    #pc = getToolByName(self,"portal_catalog")
    #brs = pc.search({"meta_type":"Patient"})
    #for br in brs:
        #list5.append(br.getObject().getId())
        ##import ipdb;ipdb.set_trace()
    #lista.append(list5)

#lista = []
#getWhoAmI(context)
#getAllDoctors(context)
#getAllSecretaries(context)
#getAllAdmins(context)
#getAllPatients(context)

#return lista

#Excluir TODO Nome estranho

