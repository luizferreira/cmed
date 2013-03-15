from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from wres.archetypes.content.patient import Patient
from wres.policy.utils.utils import getWresSite


pc = getToolByName(context,"portal_catalog")

for file_to_delete in context.REQUEST.form.iterkeys():
	#User -6 besides 2 to be independent from host url
	file_path = "/".join(file_to_delete.split("/")[-6:])
	brain_list = pc.searchResults({'path':file_path})
	brain = brain_list[0]
	context.manage_delObjects(brain.id)

return context.REQUEST.response.redirect("/".join(context.getPhysicalPath()))
