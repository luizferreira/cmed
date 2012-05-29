from DateTime import DateTime

request = context.REQUEST
id = request['id']
whole_exam = context.chart_data.get_entry_item(id, 'laboratory')
vars = ['exam_form0', 'value_form0', 'date_form0', 'id']
new_exam = whole_exam['data']
for var in vars:
    new_exam[var] = request[var]
member = context.portal_membership.getAuthenticatedMember()

new_exam['edited_by'] = member.id
new_exam['edited_on'] = DateTime()
new_exam['exam'] = new_exam['exam_form0']
new_exam['value'] = new_exam['value_form0']
new_exam['date'] = new_exam['date_form0']

whole_exam['data'] = new_exam

if 'id' in whole_exam.keys():
    del whole_exam['id']
context.chart_data.edit_entry(id, 'laboratory', **whole_exam)
state.set(portal_status_message='Exame editado.')
return state
