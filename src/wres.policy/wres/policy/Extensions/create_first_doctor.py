# -*- coding: utf-8 -*-

import Products.GenericSetup.context as import_context
import Products.GenericSetup.interfaces as interfaces
import wres.policy

def getOrCreateType(portal, atobj, newid, newtypeid):
    """
    Gets the object specified by newid if it already exists under
    atobj or creates it there with the id given in newtypeid
    """
    try:
        newobj = getattr(atobj,newid) #get it if it already exists
    except AttributeError:  #newobj doesn't already exist
        try:
            _ = atobj.invokeFactory(id=newid,type_name=newtypeid)
        except ValueError:
            _createObjectByType(newtypeid, atobj, newid)
        except Unauthorized:
            _createObjectByType(newtypeid, atobj, newid)
        newobj = getattr(atobj,newid)
    return newobj

def parseFirstDoctorInputFile(infile):
    lines = infile.readlines()
    if len(lines) < 2:
        return None
    dic = {}
    # if communimed site register form changes, this list will probably have to be updated.
    keys = ['Nome Completo', 'CRM', 'Telefone de Contato', 'Seu endereço de e-mail', 'Confirmação do e-mail', 'Especialidade 1', 'Especialidade 2', 'Nome da Clínica/Consultório', 'Avenida/Rua', 'Número', 'Complemento', 'Cidade', 'Estado', 'Telefone', 'E-mail', 'Como nos conheceu?']
    for key in keys:
        dic[key] = None

    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
        if lines[i] in dic.keys():
            try:
                # remove \n from next line.
                lines[i+1] = lines[i+1].replace('\n', '')
                # maybe the next line is a form label (in case the current label was left blank)
                if lines[i+1] in dic.keys():
                    continue
                else:
                    dic[lines[i]] = lines[i+1]
            except IndexError:
                # the IndexError indicates that the list is over, nothing to do here.
                pass
    return dic

def main(self):
    '''
    if there is a doctor in firstdoctor_info.txt, then this function creates that doctor.
    '''
    base = import_context.BaseContext(self, import_context.SetupEnviron())
    context = import_context.DirectoryImportContext(self, base)
    PROFESSIONAL_SITE = True
    from wres.policy.utils.utils import create_base_of_id
    path = wres.policy.__path__[0]
    # read firstdoctor_info and create a doctor if there is information there.
    infile = context.openDataFile('profiles/default/firstdoctor_info.txt', path)
    doctor_info = parseFirstDoctorInputFile(infile)
    full_name = doctor_info['Nome Completo'].split(' ')
    firstname = full_name[0].lower(); lastname = full_name[-1].lower()
    doctor_id = create_base_of_id(firstname, lastname)

    if doctor_info is not None:
        doctor_folder = getattr(self, 'Doctors')
        clinic = getattr(self, 'Clinic')
        if not PROFESSIONAL_SITE:
            # removing permissions from anonymous, so he cant see initial page anymore.
            doctor_folder.manage_permission('Access contents information', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE], acquire = False)
            clinic.manage_permission('View', [MANAGER_ROLE, UEMRADMIN_ROLE, DOCTOR_ROLE, SECRETARY_ROLE, TRANSCRIPTIONIST_ROLE, PATIENT_ROLE, ANONYMOUS_ROLE], acquire = False)
            doctor_folder.reindexObject()
        doctor = getOrCreateType(self, doctor_folder, doctor_id, 'Doctor')
        doctor.fillFirstDoctorInfo(doctor_info)
        clinic.fillClinicInformation(doctor_info)
        doctor.reindexObject()
        clinic.reindexObject() 
