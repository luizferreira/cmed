##parameters=member=None 
if member is None:
    mtool = context.portal_membership
    member = mtool.getAuthenticatedMember()
ro = member.getProperty('related_object')

return context.restrictedTraverse(ro.split('/')[1:])
