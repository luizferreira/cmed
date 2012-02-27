from DateTime import DateTime

request = context.REQUEST
checks = request['checks']
checks_list = checks.split(',')

medications = []
for check in checks_list:
    check = check.replace('[', '').replace(']', '').replace(' ', '').replace("'", "")
    medications.append(context.chart_data.get_entry_item(check, 'medications'))

prescription = {}
member = context.portal_membership.getAuthenticatedMember()
prescription['doctor'] = member.id
prescription['date'] = request['date']
prescription['medications'] = medications
id = context.chart_data.save_entry(context, 'prescriptions', **prescription)
import ipdb; ipdb.set_trace()
container.REQUEST.RESPONSE.redirect(context.absolute_url()+'/print_prescription?id='+id)
