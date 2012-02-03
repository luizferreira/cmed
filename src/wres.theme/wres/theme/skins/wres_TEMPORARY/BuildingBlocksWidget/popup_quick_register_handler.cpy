## Script (Python) "popup quick register"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id=''
##
REQUEST = context.REQUEST
SESSION = REQUEST.SESSION

old_id = context.getId()

try:
    new_context = context.portal_factory.doCreate(context, id)
except AttributeError:
    # Fallback for AT + plain CMF where we don't have a portal_factory
    new_context = context
new_context.processForm()

# Get the current language and put it in request/LANGUAGE
form = REQUEST.form
if form.has_key('current_lang'):
    form['language'] = form.get('current_lang')

portal_status_message = context.translate(
    msgid='message_content_changes_saved',
    domain='archetypes',
    default='Content changes saved.')

portal_status_message = REQUEST.get('portal_status_message', portal_status_message)


env = state.kwargs
reference_source_url = env.get('reference_source_url')
if reference_source_url is not None:
    reference_source_url = env['reference_source_url'].pop()
    reference_source_field = env['reference_source_field'].pop()
    reference_source_fieldset = env['reference_source_fieldset'].pop()
    portal = context.portal_url.getPortalObject()
    reference_obj = portal.restrictedTraverse(reference_source_url)
    portal_status_message = context.translate(
        msgid='message_reference_added',
        domain='archetypes',
        default='Reference Added.')

    edited_reference_message = context.translate(
        msgid='message_reference_edited',
        domain='archetypes',
        default='Reference Edited.')

    # update session saved data
    uid = new_context.UID()
    saved_dic = SESSION.get(reference_obj.getId(), None)
    if saved_dic:
        saved_value = saved_dic.get(reference_source_field, None)
        if same_type(saved_value, []):
            # reference_source_field is a multiValued field, right!?
            if uid in saved_value:
                portal_status_message = edited_reference_message
            else:
                saved_value.append(uid)
        else:
            if uid == saved_value:
                portal_status_message = edited_reference_message
            else:
                saved_value = uid
        saved_dic[reference_source_field] = saved_value
        SESSION.set(reference_obj.getId(), saved_dic)
    
    # XXX disabled mark creation flag
    ## context.remove_creation_mark(old_id)

    kwargs = {
        'status':'success_add_reference',
        'context':reference_obj,
        'portal_status_message':portal_status_message,
        'fieldset':reference_source_fieldset,
        'field':reference_source_field,
        'reference_focus':reference_source_field,
        }
    return state.set(**kwargs)

if state.errors:
    errors = state.errors
    s_items = [(s, schemata[s].keys()) for s in schemata.keys()]
    fields = []
    for s, f_names in s_items:
        for f_name in f_names:
            fields.append((s, f_name))
    for s_name, f_name in fields:
        if errors.has_key(f_name):
            REQUEST.set('fieldset', s_name)
            return state.set(
                status='failure',
                context=new_context,
                portal_status_message=portal_status_message)

if not state.errors:
#    from Products.Archetypes import transaction_note
    from Products.Archetypes.utils import transaction_note
    transaction_note('Edited %s %s at %s' % (new_context.meta_type, new_context.title_or_id(), new_context.absolute_url()))

return state.set(status='success',
                 context=new_context,
                 portal_status_message=portal_status_message)
