from DateTime import DateTime
doctors = {}

#TODO remover parte comentada
#unique = []

#for item in (context.getHistoricalPrescriptionData())['prescriptions']:
    #if not (item['signed_by'] in unique):
        #unique.append(item['signed_by'])
##        doctors[item['signed_by']] = []
        #doctors[item['submitted_by']] = []
    #doctors[item['submitted_by']].append(item)
##    doctors[item['signed_by']].append(item)

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
