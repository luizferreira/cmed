##parameters=pat=2,doc=2,sec=1,cli=True,adm=0,full=0

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from wres.archetypes.content.patient import Patient
from wres.policy.utils.utils import getWresSite
from wres.policy.utils.utils import create_valid_user_id
import random

#Get Data
HOJE = DateTime()

#Get Insurance UID
catalog = getToolByName(context,"portal_catalog")
brains = catalog.searchResults({'id':'Bradesco'})
UID = brains[0].getObject().UID()

######## PARAMETROS #########

patient_num = pat
patient_fname = 'Paciente'
patient_lname = 'Teste'

doctor_num = doc
doctor_fname = 'Doutor'
doctor_lname = 'Teste'

secretary_num = sec
secretary_fname = 'Secretaria'
secretary_lname = 'Teste'

admin_num = adm
admin_fname = 'Admin'
admin_lname = 'Teste'

create_clinic = cli
clinic_name = 'CliniMed'
clinic_address = 'Av. Afonso Pena, 1500'
clinic_phone = '313334444'

email = 'teste@communi.com.br'
phone = '3134442255'
cphone = '3188992255'
full_info = full

######## PARAMETROS #########

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

def create_new_object(portal, parent, newid, new_obj_type):
    """
    Creates a new object of the type 'new_obj_type' in 'parent'
    """
    context.plone_log(newid)
    _ = parent.invokeFactory(id=newid,type_name=new_obj_type)
    newobj = getattr(parent,newid)
    if newobj != None:
        context.plone_log("-> %s %s created..." % (new_obj_type, newid))
    else:
        context.plone_log("*** ERROR while creating object")
    return newobj

def random_birthdate():
    return DateTime(random.randrange(1901,HOJE.year()), random.randrange(1,13), random.randrange(1,28))

def set_patient_information(p):
	
    p.setFirstName(patient_fname)
    p.setLastName(patient_lname)
    p.setEmail(email)
    p.setBirthDate(random_birthdate())
    p.setContactPhone(phone)
    #Preenchimento do Chart
    allergy = {'date': '07/05/2012', 'reaction': 'Edema/co\xc3\xa7eira', 'allergy': 'Camar\xc3\xa3o', 'submitted_by': 'admin'}
    medication = {'status': 'active', 'submitted_by': 'admin', 'use': '1 cp quando houver dor de cabe\xc3\xa7a', 'medication': 'Tylenol dc', 'end_date': DateTime('2012/05/07 17:06:14.061165 GMT-3'), 'note': '', 'start': '07/05/2012', 'concentration': '80mg', 'quantity': '12'}
    problem = {'submitted_by': 'admin', 'code': 'G43.0', 'end_date': DateTime('2012/05/07 17:09:25.103551 GMT-3'), 'started': DateTime('2012/05/07 00:00:00 GMT-3'), 'note': '', 'submitted_on': DateTime('2012/05/07 17:09:25.103459 GMT-3'), 'state': 'active', 'problem': 'Enxaqueca sem aura [enxaqueca comum]'}
    exam = {'date': '07/05/2012', 'exam': 'Glicose', 'value': '93 mg/dl'}
    p.chart_data.save_entry(context, 'allergies', **allergy)
    p.chart_data.save_entry(context, 'medications', **medication)
    p.chart_data.save_entry(context, 'problems', **problem)
    p.chart_data.save_entry(context, 'laboratory', **exam)


    if int(full_info):
        p.setType_of_patient('new')
        p.setHomePhone(phone)
        p.setMobile(cphone)    
        p.setSocialSecurity('55351927403')
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
        p.setGuarantor_identidade("MG11789456")
        p.setGuarantor_relationship("Amante")
        p.setGuarantor_name("Pedro Cardoso")
        p.setGuarantor_contact_phone("3137421155")
        p.setGuarantor_orgaoEmissor("marinha")
        p.setMatricula("2010497859")
        p.setDataDeValidade(DateTime(random.randrange(HOJE.year(),2100),random.randrange(1,13), random.randrange(1,28)))
        p.setConvenio("Vale")
        p.setConfirmedChartNumber(False)
        p.setTipo("Privado")
        p.setGuarantor_address1("Rua das Magnolias,456")
        p.setGuarantor_address2("Bairro dos Cornelios")
        p.setGuarantor_city("Tangamandápio")
        p.setGuarantor_state("Acre")
        p.setGuarantor_zipcode("31270213")
        p.setIndustry("Vale do rio doce")
        p.setWorkPhone("3137425689")
        p.setRetirementdate(DateTime(random.randrange(HOJE.year(),2100), random.randrange(1,13), random.randrange(1,28)))
        p.setTituloEleitor("1225282038")
        p.setOccupationTitle("Programador")
        p.setGuarantor_extension("1597")
        p.setInsurance(UID)
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
        p.setEmergency_zipcode("31270215")
        p.setEmergency_state("Sao Paulo")
        p.setEmergency_city("Salvador")
        p.setEmergency_address2("Bairro Sao Lucas")
        p.setEmergency_address1("Rua dos viaviarios")
        p.setEmergency_other_phone("3137421436")
        p.setEmergency_home_phone("3137421346")
        p.setEmergency_work_phone("3137421578")
        p.setEmergency_relationship("Médico")
        p.setEmergency_contact_name("Helio Heal")

    p.reindexObject()

def set_doctor_information(d):
    d.setProfessional('Provider')
    d.setSsn(12345678910)
    d.setFirstName(doctor_fname)
    d.setLastName(doctor_lname)
    d.reindexObject()

def set_secretary_information(s):
    s.setFirstName(secretary_fname)
    s.setLastName(secretary_lname)
    s.setSsn('12345678910')
    s.setEmail(email)
    s.reindexObject()    

def set_admin_information(a):
    a.setFirstName(admin_fname)
    a.setLastName(admin_lname)
    a.setSsn('12345678910')
    a.setEmail(email)
    a.reindexObject()

def set_clinic_information(clinic):
    clinic.setName(clinic_name)
    clinic.setEndereco(clinic_address)
    clinic.setPhone(clinic_phone)
    clinic.setFax(clinic_phone)
    clinic.setEmail(email)
    clinic.reindexObject()

def create_patients(portal, pr):

    patients = getattr(portal, 'Patients')

    context.plone_log("I will create %s patient(s)..." % patient_num)
    print "I will create %s patient(s) (full_info = %s)..." % (patient_num, full_info)
    for i in range(int(patient_num)):
        new_obj_id = create_valid_user_id(pr, patient_fname, patient_lname)
        patient = create_new_object(portal, patients, new_obj_id, 'Patient')
        fullname = patient_fname + patient_lname
        create_uemr_user(patient, new_obj_id, email=email, fullname=fullname)
        set_patient_information(patient)
        print "> Patient %s created..." % new_obj_id
    return printed

def create_doctors(portal, pr):

    doctors = getattr(portal, 'Doctors')

    context.plone_log("I will create %s doctor(s)..." % doctor_num)
    print "I will create %s doctor(s)..." % doctor_num
    for i in range(int(doctor_num)):
        new_obj_id = create_valid_user_id(pr, doctor_fname, doctor_lname)
        doctor = create_new_object(portal, doctors, new_obj_id, 'Doctor')
        fullname = doctor_fname + doctor_lname
        create_uemr_user(doctor, new_obj_id, email=email, fullname=fullname)
        set_doctor_information(doctor)
        doctor.add_visits_folder()
        print "> Doctor %s created..." % new_obj_id
    return printed   

def create_secretaries(portal, pr):

    secretaries = getattr(portal, 'Secretaries')

    context.plone_log("I will create %s secretary(ies)..." % secretary_num)
    print "I will create %s secretary(ies)..." % secretary_num
    for i in range(int(secretary_num)):
        new_obj_id = create_valid_user_id(pr, secretary_fname, secretary_lname)
        secretary = create_new_object(portal, secretaries, new_obj_id, 'Secretary')
        fullname = secretary_fname + secretary_lname
        create_uemr_user(secretary, new_obj_id, email=email, fullname=fullname)
        set_secretary_information(secretary)
        print "> Secretary %s created..." % new_obj_id
    return printed     

def create_admins(portal, pr):

    admins = getattr(portal, 'Admins')

    context.plone_log("I will create %s admin(s)..." % admin_num)
    print "I will create %s admin(s)..." % admin_num
    for i in range(int(admin_num)):
        new_obj_id = create_valid_user_id(pr, admin_fname, admin_lname)
        admin = create_new_object(portal, admins, new_obj_id, 'Admin')
        fullname = admin_fname + admin_lname
        create_uemr_user(admin, new_obj_id, email=email, fullname=fullname)
        set_admin_information(admin)
        print "> Admin %s created..." % new_obj_id
    return printed      

def set_clinic(portal, pr):

    clinic = getattr(portal, 'Clinic')

    context.plone_log("I will initialize clinic...")
    print "I will initialize clinic..."
    set_clinic_information(clinic)
    print "> Clinic initialized..."
    return printed
    
def create_other(portal):
    templates = getattr(portal, "Templates")
    context.plone_log("Creating templates")
    print "Creating templates"
    new_id = "consulta-"+str(random.randint(0, 9999))
    consulta = create_new_object(portal, templates.Consultas, new_id, "Template")
    consulta.setTemplate_body("<br><b>Meu Modelo de Primeira Consulta.</b><br><br> Queixa Principal: <br><br> História da Moléstia Atual:")
    consulta.setTitle("Primeira Consulta")
    consulta.reindexObject()
    new_id = "impresso-"+str(random.randint(0, 9999))
    impresso = create_new_object(portal, templates.Impressos, new_id, "Template")
    impresso.setTemplate_body("<br><b>Meu Modelo de Licença Médica.</b><br><br>Atesto para os devidos fins que: <b>José Carlos de Oliveira</b> \
    se encontrou enfermo entre 07/05/2012 e 12/05/2012 e incapaz de exercer suas atribuições normalmente. CID A09.")
    impresso.setTitle("Licença Médica")
    return printed

def init():

    intro = """==========================================================
INITIALIZATION SCRIPT

Summary: Used to automate the creation of cmed users. 

Params:
> pat = number of patients to be created (Default = 2)
> doc = number of doctors to be created (Default = 2)
> sec = number of secretaries to be created (Default = 2)
> adm = number of admins to be created (Default = 0)
> cli = 1 | 0. Initialize clinic? (Default = 1 (True))
> > 0: No. I don't wanna initialize clinic.
> > 1: Yes. I wanna initialize clinic.
> full = 1 | 0. Level of information for patients. (D = 0)
> > 0: set only required fields.
> > 1: set all fields.

Example of usage:
.../debug_init?pat=10&doc=1&sec=0&adm=2&cli=0&full=1
==========================================================
    """

    print intro

    portal = getWresSite()
    pr = getToolByName(portal, 'portal_registration')

    context.plone_log("---------------------------------------------")
    context.plone_log("Inicializando instância...")

    print 'Initializing...\n'

    context.plone_log( "P: %d, D: %d, S: %d, A: %d, C: %d" % (int(patient_num), int(doctor_num), int(secretary_num), int(admin_num), int(create_clinic)) )

    if int(patient_num) > 0:
        print create_patients(portal, pr)
    else:
        print 'I will not create patients.\n'
    
    if int(doctor_num) > 0:
        print create_doctors(portal, pr)
    else:
        print 'I will not create doctors.\n'

    if int(secretary_num) > 0:
        print create_secretaries(portal, pr)
    else:
        print 'I will not create secretaries.\n'

    if int(admin_num) > 0:
        print create_admins(portal, pr)
    else:
        print 'I will not create admins.\n'
        
    if int(create_clinic):
        print set_clinic(portal, pr)
    else:
        print 'I will not set clinic information.\n'
        
    create_other(portal)

    context.plone_log("---------------------------------------------\n")

    print 'DONE!'
    return printed

######################################################################################

portal = getWresSite()
mt = getToolByName(portal, 'portal_membership')
member = mt.getAuthenticatedMember()
if member.has_role('Manager'):
    print init()
else:
    context.plone_log("You must have the 'Manager' role to run the debug_init script.")
    print "You must have the 'Manager' role to run the debug_init script."

return printed
