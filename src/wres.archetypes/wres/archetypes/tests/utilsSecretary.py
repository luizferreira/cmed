#coding=utf-8
from DateTime import DateTime
from wres.policy.utils.utils import create_valid_user_id
from Products.CMFCore.utils import getToolByName

HOJE = DateTime()

def create_uemr_user(related_object, user_id, email='', fullname=''):
    pr = getToolByName(related_object, 'portal_registration')
    pm = getToolByName(related_object, 'portal_membership')
    uf = getToolByName(related_object, 'acl_users')
    pr.addMember(
        user_id, 'senha1',
        properties={
            'home_url': related_object.get_home_url(),
            'username': user_id,
            'email': email,
            'fullname': fullname,
            'related_object': '/'.join(related_object.getPhysicalPath()),
        },
    )
    uf.userSetGroups(user_id, [related_object.getGroup()])
    pm.createMemberArea(member_id=user_id) 


def create_secretary(portal, pr,secretary_fname="Anna",secretary_lname="Kournikova",email="ak@gmail.com"):
    secretaries = getattr(portal, 'Secretaries')
    new_obj_id = create_valid_user_id(pr, secretary_fname, secretary_lname)
    secretary = create_new_object(portal, secretaries, new_obj_id, 'Secretary')
    fullname = secretary_fname + secretary_lname
    create_uemr_user(secretary, new_obj_id, email=email, fullname=fullname)
    set_secretary_information(secretary)

def create_new_object(portal, parent, newid, new_obj_type):
    """
    Creates a new object of the type 'new_obj_type' in 'parent'
    """
    _ = parent.invokeFactory(id=newid,type_name=new_obj_type)
    newobj = getattr(parent,newid)
    if newobj == None:
        print "Erro ao criar novo objeto"
    return newobj

def set_secretary_information(d
,firstname="Anna"
,lastname="Kournikova"
,email="ak@gmail.com"
,phone="123455478"
,socialsecurity="01234567890"
,cphone="99215909"
,):
	
    d.setFirstName(firstname)
    d.setLastName(lastname)
    d.setEmail(email)
    d.setPhone(phone)   
    d.setSsn(socialsecurity)
    d.setAddress1('Rua Brasil, 123')
    d.setCity('Belo Horizonte')
    d.setState('Minas Gerais')
    d.setCel(cphone)
    d.reindexObject()

