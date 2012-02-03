from DateTime import DateTime

request = context.REQUEST
checks = request['checks']
checks_list = checks.split(',')

medications = []
for check in checks_list:
    check = check.replace('[', '').replace(']', '').replace(' ', '').replace("'", "")
    medications.append(context.getMedication(check))

prescription = {}
member = context.portal_membership.getAuthenticatedMember()
prescription['doctor'] = member.id
prescription['date'] = request['date']
prescription['medications'] = medications
id = context.savePrescription(**prescription)
container.REQUEST.RESPONSE.redirect(context.absolute_url()+'/print_prescription?id='+id)
