from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from wres.archetypes.content.patient import Patient
from wres.policy.utils.utils import getWresSite

imgURL = context.REQUEST.get("imgURL")
pc = getToolByName(context,"portal_catalog")

brains = pc.searchResults({'Type':'Image'})
brains += pc.searchResults({'Type':'File'})

for brain in brains:
	if brain.getURL() == imgURL:
		obj = brain.getObject()
		uf = obj.aq_parent
		uf.manage_delObjects([obj.getId()])

return context.REQUEST.response.redirect("/".join(context.getPhysicalPath()))
