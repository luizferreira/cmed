#coding=utf-8
import random 
from DateTime import DateTime
from wres.archetypes.content.patient import Patient
from wres.policy.utils.utils import create_valid_user_id
from Products.CMFCore.utils import getToolByName

HOJE = DateTime()

def getPatientOwnerFromPath(path):
    splited = path.split('/')
    if len(splited) > 3:
        if splited[2] == "Patients":
            return splited[3]
    return None

def random_birthdate():
    return DateTime(random.randrange(1901,HOJE.year()), random.randrange(1,13), random.randrange(1,28))

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


def create_patient(portal, pr,patient_fname="joao",patient_lname="silva",email="joao@silva.com"):
    patients = getattr(portal, 'Patients')
    new_obj_id = create_valid_user_id(pr, patient_fname, patient_lname)
    patient = create_new_object(portal, patients, new_obj_id, 'Patient')
    fullname = patient_fname + patient_lname
    create_uemr_user(patient, new_obj_id, email=email, fullname=fullname)
    set_patient_information(patient)
    # cria evento manualmente.
    patient.create_event(1000, patient.created(), patient)        

def create_empty_patient(portal, pr,patient_fname="joao",patient_lname="silva",email="joao@silva.com"):
    patients = getattr(portal, 'Patients')
    new_obj_id = create_valid_user_id(pr, patient_fname, patient_lname)
    patient = create_new_object(portal, patients, new_obj_id, 'Patient')
    fullname = patient_fname + patient_lname
    create_uemr_user(patient, new_obj_id, email=email, fullname=fullname)
    # cria evento manualmente.
    patient.create_event(1000, patient.created(), patient) 

def create_new_object(portal, parent, newid, new_obj_type):
    """
    Creates a new object of the type 'new_obj_type' in 'parent'
    """
    _ = parent.invokeFactory(id=newid,type_name=new_obj_type)
    newobj = getattr(parent,newid)
    if newobj == None:
        print "Erro ao criar novo objeto"
    return newobj

def set_patient_information(p
,firstname="Joao"
,lastname="Silva"
,email="joao@silva.com"
,birthdate=random_birthdate()
,phone="123455478"
,socialsecurity="01234567890"
,cphone="99215909"
,):
	
    p.setFirstName(firstname)
    p.setLastName(lastname)
    p.setEmail(email)
    p.setBirthDate(birthdate)
    p.setContactPhone(phone)
    #Preenchimento do Chart
    allergy = {'state':'active','date': '07/05/2012', 'reaction': 'Edema/coceira', 'allergy': 'Camar\xc3\xa3o', 'submitted_by': 'admin'}
    medication = {'status': 'active', 'submitted_by': 'admin', 'use': '1 cp quando houver do de cabe\xc3\xa7a', 'medication': 'Tylenol dc', 'end_date': DateTime('2012/05/07 17:06:14.061165 GMT-3'), 'note': '', 'start': '07/05/2012', 'concentration': '80mg', 'quantity': '12'}
    problem = {'state': 'active', 'submitted_by': 'admin', 'code': 'G43.0', 'end_date': DateTime('2012/05/07 17:09:25.103551 GMT-3'), 'started': DateTime('2012/05/07 00:00:00 GMT-3'), 'note': '', 'submitted_on': DateTime('2012/05/07 17:09:25.103459 GMT-3'), 'problem': 'Enxaqueca sem aura [enxaqueca comum]'}
    exam = {'date': '07/05/2012', 'exam': 'Glicose', 'value': '93 mg/dl'}
    p.chart_data.save_entry(p, 'allergies', **allergy)
    p.chart_data.save_entry(p, 'medications', **medication)
    p.chart_data.save_entry(p, 'problems', **problem)
    p.chart_data.save_entry(p, 'laboratory', **exam)

    p.setHomePhone(phone)
    p.setMobile(cphone)    
    p.setSocialSecurity(socialsecurity)
    p.setIdentidade('MG13082425')
    p.setOrgaoEmissor('ssp')
    p.setSex('Male')
    p.setAddress1('Rua Brasil, 123')
    p.setAddress2('Centro')
    p.setCity('Belo Horizonte')
    p.setState('Minas Gerais')
    p.setZipcode('33600123')
    p.setChart(0)
    p.setEmployerName('Joao Barroso')
    p.setState("Ativo")
    p.setFax("3137422322")
    p.setCTPS("0123456")
    p.setMatricula("2010497859")
    p.setDataDeValidade(DateTime(random.randrange(HOJE.year(),2100),random.randrange(1,13), random.randrange(1,28)))
    p.setConvenio("Vale")
    p.setTipo("Privado")
    p.setIndustry("Vale do rio doce")
    p.setWorkPhone("3137425689")
    p.setRetirementdate(DateTime(random.randrange(HOJE.year(),2100), random.randrange(1,13), random.randrange(1,28)))
    p.setTituloEleitor("1225282038")
    p.setOccupationTitle("Programador")
    p.setDataDeValidade("12/11/2015")
    p.setTitular("Sim")
    p.setPis_pasep("24451.01526")
    p.setCartaoNacionalDeSaude("Cartão de Saude")
    p.setNomeDoPai("Carlos Carlindos da Silva Sauro")
    p.setNomeDaMae("Carla Carlindas da Silva Sauro")
    p.setNacionalidade("Chinesa")
    p.setRace("Amaralera")
    p.setStatus("fulltime")
    p.setMaritalStatus("Amante")
    p.setEducationCompleted("doutorado")
    p.setExtension("45612")

    p.reindexObject()

