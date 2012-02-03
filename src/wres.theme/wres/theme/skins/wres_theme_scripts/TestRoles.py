member = context.portal_membership.getAuthenticatedMember()
return member.has_role('Manager') or member.has_role('Doctor')
