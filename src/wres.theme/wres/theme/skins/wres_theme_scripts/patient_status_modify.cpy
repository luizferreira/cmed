## Controller Python Script "inactive_status_modify"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=workflow_action=None, comment='', type='', note=[], effective_date=None, expiration_date=None, *args
##
from DateTime import DateTime
from Products.CMFPlone.utils import transaction_note

def listToString(a):
    a_str = ''
    for i in list(a):
        a_str += i
    return a_str

note = listToString(note)

new_context = context
portal_workflow = new_context.portal_workflow
current_state = portal_workflow.getInfoFor(new_context, 'review_state')

wfcontext = context

# next state
if workflow_action != current_state:
    next_state = workflow_action
    wfcontext = new_context.portal_workflow.doActionFor(context, \
            workflow_action, comment='', type=type, note=note,)
else:
    next_state = current_state

# context
if not wfcontext:
    wfcontext = new_context

transaction_note(note)

# new state
msg_state = next_state == 'activate' and 'active' or 'inactive'
new_state = state.set(context=wfcontext, \
        portal_status_message='Patient now is '+msg_state+'.')

#if next_state == 'activate':
#    context.REQUEST.RESPONSE.redirect('patient_view')
#else:
#    return new_state

return new_state
