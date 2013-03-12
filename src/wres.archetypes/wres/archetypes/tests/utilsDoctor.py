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


def create_doctor(portal, pr,doctor_fname="DR. VICTOR",doctor_lname="Frankenstein",email="vfrank@gmail.com"):
    doctors = getattr(portal, 'Doctors')
    new_obj_id = create_valid_user_id(pr, doctor_fname, doctor_lname)
    doctor = create_new_object(portal, doctors, new_obj_id, 'Doctor')
    fullname = doctor_fname + doctor_lname
    doctor.at_post_create_script()
    set_doctor_information(doctor)

def create_new_object(portal, parent, newid, new_obj_type):
    """
    Creates a new object of the type 'new_obj_type' in 'parent'
    """
    _ = parent.invokeFactory(id=newid,type_name=new_obj_type)
    newobj = getattr(parent,newid)
    if newobj == None:
        print "Erro ao criar novo objeto"
    return newobj

def set_doctor_information(d
,firstname="Dr. Victor"
,lastname="Frankenstein"
,email="vfrank@gmail.com"
,phone="123455478"
,socialsecurity="01234567890"
,cphone="99215909"
,):
	
    d.setFirstName(firstname)
    d.setLastName(lastname)
    d.setEmail(email)
    d.setPhone(phone)
    d.setProfessional('Provider')    
    d.setSsn(socialsecurity)
    d.setStreet1('Rua Brasil, 123')
    d.setStreet2('Centro')
    d.setCity('Belo Horizonte')
    d.setState('Minas Gerais')
    d.setZipcode('33600123')
    d.setFax("3137422322")
    d.setWebsite("www.communi.com.br")
    d.setCel("31 9877 0801")
    d.setSpecialty1("cardiology")
    d.setSpecialty2("other")
    d.setInitial("V. Frank")
    d.setSignature("Vitao")
    d.setCredentials("Credenciado Plus")
    d.reindexObject()

