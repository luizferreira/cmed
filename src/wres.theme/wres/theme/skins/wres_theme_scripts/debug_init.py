##parameters=pat=2,doc=2,sec=1,cli=True,adm=0,full=0
#coding=utf-8

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from wres.archetypes.content.patient import Patient
from wres.policy.utils.utils import getWresSite
from wres.policy.utils.utils import create_valid_user_id
import random

#Get Data
HOJE = DateTime()

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
clinic_street = 'Av. Afonso Pena'
clinic_address = 'Av. Afonso Pena, 1500' #used by sec and doctor.
clinic_number = 1500
clinic_complemento = 'Sala 404'
clinic_bairro = 'Centro'
clinic_city = 'Belo Horizonte'
clinic_state = 'mg'
clinic_phone = '313334444'

email = 'teste@communi.com.br'
phone = '3134442255'
cphone = '3188992255'
full_info = full

document_template = "<p>\
<b>QD (Queixa  e Duração)</b> <br />\
<i>Queixa e duração da moléstia atual, outras doenças já diagnosticadas que podem ajudar no entendimento da queixa.</i><br />\
<br />\
<b>HMA (História da Moléstia Atual) </b><br />\
<i>usar, sempre que possível, a técnica hipotético-dedutiva;</i><br />\
<i>usar todos os dados de interesse, sejam eles antecedentes pessoais ou familiares, dados sociais, ou outros;</i><br />\
<i>observar coordenação cronológica;</i><br />\
<i>deixar clara a importância dos sintomas e relação causa-efeito;</i><br />\
<i>usar letra legível com boa apresentação (É UM DOCUMENTO);</i><br />\
<i>evitar usar repetidamente 'o paciente refere'</i><br />\
<i>não assumir a postura de escriba;</i><br />\
<i>não descrever roteiros médicos: “passou no hospital X, depois no hospital Y”</i><br />.<br />\
<br />\
<b> AP (Antecedentes Pessoais)</b><br />\
<i>trauma ou cirurgias (datas); outras doenças, medicamentos, internações;</i><br />\
<i>alergia ou intolerância medicamentosa; imunização: tétano, hepatite, rubéola, etc;</i><br />\
<i>História Obstétrica (Gestações, Partos e Abortos).</i><br />\
<br />\
<b> Hábitos</b><br />\
<i>Tabagismo, Etilismo (Quanto?); atividade física e freqüência/ Alimentação (último colesterol)</i><br />\
<i>Pesquisa de risco de HIV/ uso de drogas/ transfusões</i><br />\
<br />\
<b> AF (Antecedentes Familiares)</b><br />\
<i>Avaliação do potencial mórbido para doenças prevalentes como: Doenças cardiovasculares, Hipertensão Arterial (HAS), Diabetes (DM) e Tuberculose (Tb).</i><br />\
<i>Avaliação de possível participação familiar na gênese do quadro atual.</i><br />\
<br />\
<b> HS (História Social)</b><br />\
<i>Situação no trabalho, família, lazer, etc.</i><br />\
<br />\
<b> ISDA (Interrogatório Sobre Diversos Aparelhos)</b><br />\
<i>Geral: febre, alterações de peso, alteração no dinamismo</i><br />\
<i>Cabeça: Cefaléia, tontura</i><br />\
<i>Olhos: acuidade visual, dor, campo visual</i><br />\
<i>Ouvido: acuidade auditiva, zumbido, vertigem</i><br />\
<i>Nariz/ garganta/ boca: epistaxe, IVAS freqüentes, obstrução, dor de garganta freqüente, sinusite.</i><br />\
<i>Tórax: tosse, expectoração, dor, dispnéia, hemoptise, edemas, palpapitação.</i><br />\
<i>Gastrointestinal: disfagia, azia, pirose, hábito intestinal, sangramento, puxo, tenesmo, dia gástrico.</i><br />\
<i>Gênito-urinário: disúria, poliúria, nictúria, nódulos de mama, Papanicolaou, mamografia</i><br />\
<i>Pele e fâneros: manchas, alopecia</i><br />\
<i>Queixas espontâneas: “O(A) Sr.(a) tem alguma outra queixa?”</i><br />\
<br />\
<b>Exame Físico:</b><br />\
<i>Geral: B(M,R)EG, estado nutricional (caquético, emagrecido, obeso), (des)corado, (desi)hidratado, (a)cianótico, (an)ictérico, (a)febril, (taqui/dis)eupnéico.</i><br />\
<i>Parâmetros vitais, PA (Pressão arterial), FC (Freqüência cardíaca), FR (Freqüência respiratória), T (Temperatura), Peso e Altura, IMC (m(kg) /h2(m)).</i><br />\
<i>Especial: Cabeça e Pescoço, Tórax, Abdômen, Membros</i><br />\
<br />\
<b> HD(Hipótese Diagnóstica): </b><br /> <i>O diagnóstico que o médico der. E lembre-se de colocar os outros diagnósticos já feitos que ainda são atuais, principalmente se for crônico, como HAS, DM.</i><br />\
<br />\
<b> CD (Conduta e Discussão): </b><br /> <i>Medicamentos prescritos, recomendações, encaminhamentos, visita domiciliar  e/ou data do retorno (observações para o retorno se necessário).</i><br />\
</p>"

######## PARAMETROS #########

def create_uemr_user(related_object, user_id, email='', fullname=''):
    pr = getToolByName(related_object, 'portal_registration')
    pm = getToolByName(related_object, 'portal_membership')
    uf = getToolByName(related_object, 'acl_users')
    
    #If for random password to patients
    
    if related_object.getGroup() == 'Patient':
        import string, random
        password = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(20)])
        context.plone_log("Senha: %s" % password)
        pr.addMember(
            user_id, password,
            properties={
                'home_url': related_object.get_home_url(),
                'username': user_id,
                'email': email,
                'fullname': fullname,
                'related_object': '/'.join(related_object.getPhysicalPath()),
            },
        )
    else:
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
    newobj.unmarkCreationFlag() # prevent at_post_created_script to be executed the first time the object is edited.
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
    allergy = {'state':'active','date': '07/05/2012', 'reaction': 'Edema/coceira', 'allergy': 'Camar\xc3\xa3o', 'submitted_by': 'admin'}
    medication = {'status': 'active', 'submitted_by': 'admin', 'use': '1 cp quando houver do de cabe\xc3\xa7a', 'medication': 'Tylenol dc', 'end_date': DateTime('2012/05/07 17:06:14.061165 GMT-3'), 'note': '', 'start': '07/05/2012', 'concentration': '80mg', 'quantity': '12', 'use_type':'Interno'}
    problem = {'state': 'active', 'submitted_by': 'admin', 'code': 'G43.0', 'end_date': DateTime('2012/05/07 17:09:25.103551 GMT-3'), 'started': DateTime('2012/05/07 00:00:00 GMT-3'), 'note': '', 'submitted_on': DateTime('2012/05/07 17:09:25.103459 GMT-3'), 'problem': 'Enxaqueca sem aura [enxaqueca comum]'}
    exam = {'date': '07/05/2012', 'exam': 'Glicose', 'value': '93 mg/dl'}
    p.chart_data.save_entry(p, 'allergies', **allergy)
    p.chart_data.save_entry(p, 'medications', **medication)
    p.chart_data.save_entry(p, 'problems', **problem)
    p.chart_data.save_entry(p, 'laboratory', **exam)

    if int(full_info):
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

def set_doctor_information(d):
    d.setProfessional('Provider')
    d.setSsn(12345678910)
    d.setFirstName(doctor_fname)
    d.setLastName(doctor_lname)
    d.setStreet1(clinic_address)
    d.setStreet2('Centro')
    d.setCity('Belo Horizonte')
    d.setState('Minas Gerais')
    d.setZipcode('33600123')
    d.setWebsite('www.communimed.com.br')
    d.setPhone(phone)
    d.setCel(cphone)
    d.setFax(phone)
    d.setEmail(email)
    d.setSpecialty1('general')
    d.setSignPassword('senha1')
    d.reindexObject()

def set_secretary_information(s):
    s.setFirstName(secretary_fname)
    s.setLastName(secretary_lname)
    s.setSsn('12345678910')
    s.setEmail(email)
    s.setAddress1(clinic_address)
    s.setCity('Belo Horizonte')
    s.setState('Minas Gerais')
    s.setPhone(phone)
    s.setCel(cphone)
    s.reindexObject()

def set_admin_information(a):
    a.setFirstName(admin_fname)
    a.setLastName(admin_lname)
    a.setSsn('12345678910')
    a.setEmail(email)
    a.reindexObject()

def set_clinic_information(clinic):
    clinic.setName(clinic_name)
    clinic.setStreet(clinic_street)
    clinic.setNumber(clinic_number)
    clinic.setComplemento(clinic_complemento)
    clinic.setBairro(clinic_bairro)
    clinic.setCity(clinic_city)
    clinic.setState(clinic_state)
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
        patient.setReaderLocalRole()
        fullname = patient_fname + patient_lname
        create_uemr_user(patient, new_obj_id, email=email, fullname=fullname)
        set_patient_information(patient)
        # cria evento manualmente.
        patient.create_event(1000, patient.created(), patient)
        #Set chartSystemData
        #patientFolder = patient.getParentNode()
        #nextChartSystemID = patientFolder.getLastChartSystemID() + 1
        #patient.setChartSystemID(nextChartSystemID)
        #patientFolder.setLastChartSystemID(nextChartSystemID)
        #Force to create chartFolder_hidden accessing chartFolder
        accessChartFolder = patient.chartFolder
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
    consulta.setTemplate_body(document_template)
    consulta.setTitle("Primeira Consulta")
    consulta.reindexObject()
    new_id = "impresso-"+str(random.randint(0, 9999))
    impresso = create_new_object(portal, templates.Impressos, new_id, "Template")
    impresso.setTemplate_body("<p>Atesto para os devidos fins que: <b>José Carlos de Oliveira</b> \
    se encontrou enfermo entre 07/05/2012 e 12/05/2012 e incapaz de exercer suas atribuições normalmente. CID A09.</p>")
    impresso.setTitle("Licença Médica")
    impresso.reindexObject()
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
> full = 1 | 0. Level of information for patients. (D = 1)
> > 0: set only required fields.
> > 1: set all fields.

Example of usage:
.../debug_init?pat=10&doc=1&sec=0&adm=2&cli=0&full=0
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
