from wres.policy.utils.utils import getWresSite

portal = getWresSite()

def getDoctors():
    doctor_folder = portal.Doctors
    doctor_list = doctor_folder.listFolderContents()
    doctor_list.sort(key=lambda x:x.firstName) 
    return  doctor_list

def getLoggedDoctor():
	mt = getattr(portal, 'portal_membership')
	if mt.isAnonymousUser():
	    return None
	else:
	    member = mt.getAuthenticatedMember()
	    username = member.getUserName()
	    if member.has_role('Doctor'):
	    	return username
	    else:
	    	return None

result = {}
result['doctors'] = getDoctors()
result['logged_doctor'] = getLoggedDoctor()

return result
