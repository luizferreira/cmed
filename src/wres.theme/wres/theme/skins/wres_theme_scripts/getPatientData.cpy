from DateTime import DateTime
#Usado em print_prescription
doctors = {}
others = {}
patient = context.getPatient()
request = context.REQUEST

today = DateTime()
others['name'] = patient.getFirstName() + ' ' + patient.getLastName()
others['hasaddr'] = patient.getAddress1() != ''
others['address'] = patient.getAddress1() + ' ' + \
                    patient.getAddress2() + ' ' + \
                    patient.getCity() + ' ' + \
                    patient.getState() + ' ' + \
                    patient.getZipcode()
others['phone'] = context.apply_mask(value=patient.getContactPhone(), mask='(dd)dddd-dddd')
others['date'] = today.strftime('%d/%m/%Y')
doctors['info'] = others
return doctors
