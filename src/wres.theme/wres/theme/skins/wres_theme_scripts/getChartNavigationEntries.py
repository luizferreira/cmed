request = context.REQUEST
current_url = request.URL

TEMPLATE_ID = current_url.split('/')[-1]
def createGroup(name):
    return {'group_id': name.lower().replace(' ', '_'),
            'title': name,
            'links': [],
            }
def addLink(group, text, href, icon='document_icon.gif'):
    #from zdb import set_trace; set_trace()
    base = context.chartFolder.absolute_url_path()
    link_template = href.split('/')[-1]
    if TEMPLATE_ID == link_template:
        css = 'currentNavItem'
    else:
        css = ''
    group['links'].append({'text': text,
                           'href': base + href,
                           'icon': icon,
                           'css': css,
                           })

structure = []
mc = createGroup('Medical Chart')
addLink(mc, 'Chart Summary', '/chart_folder_view', icon='action_icon.png')
addLink(mc, 'Consults', '/documents', icon='copy_icon.png')
addLink(mc, 'Impressos', '/impressos', icon='print_icon.png')
addLink(mc, 'Documentos Externos', '/upload', icon='upload_icon.png')
addLink(mc, 'Medicamentos e Prescrições', '/show_medications', icon='add_icon.png')
addLink(mc, 'Histórico de Prescrições', '/prescriptions_history', icon='edit.png')
addLink(mc, 'Problem List', '/show_problem_list', icon='error_icon.gif')
addLink(mc, 'Alergias', '/show_allergies', icon='contentrules_icon.png')
addLink(mc, 'Exames', '/show_exams', icon='exams_icon.png')

structure.append(mc)

#ed = createGroup('External Documents')
#addLink(ed, 'Documentos Gerais', '/upload', icon='folder_icon.gif') 
#addLink(ed, 'Hospital Records', '/hospital_records/documents_view', icon='folder_icon.gif')
##addLink(ed, 'ECG', '/ecg/', icon='folder_icon.gif')
#addLink(ed, 'Imaging', '/imgs/documents_view', icon='folder_icon.gif')
#addLink(ed, 'Legacy', '/legacy/documents_view', icon='folder_icon.gif')
#addLink(ed, 'Misc', '/misc/documents_view', icon='folder_icon.gif')
#structure.append(ed)

#sm = createGroup('Summaries')

##addLink(sm, 'Encounters', '/encounters/show_encounters')
##addLink(sm, 'BLA', '/bla')
#addLink(sm, 'Encounters', '/encounters/show_encounters')
#addLink(sm, 'Históricos', '/show_histories', icon='event_icon.png')
#addLink(sm, 'Vital Signs', '/show_vital_signs', icon='vital_icon.png')
#addLink(sm, 'Medical Hx', '/show_medical_history')
#addLink(sm, 'OB/GYN Hx', '/show_obgyn_history')
#addLink(sm, 'Surgical Hx', '/show_surgical_history')
#addLink(sm, 'Social Hx', '/show_social_history')
#addLink(sm, 'Family Hx', '/show_family_history')
#addLink(sm, 'Plan List', '/plan_list')
#addLink(sm, 'Allergies', '/show_allergies')
#addLink(sm, 'Immunizations', '/show_immunizations')
##addLink(sm, 'Tests', '/show_tests')
##addLink(sm, 'Patient Notes', '/show_patient_notes')
#structure.append(sm)

#fm = createGroup('Forms')
##addLink(fm, 'Questionnaire', '/show_questionnaire', icon='user.gif')
#addLink(fm, 'Signed Forms', '/signed_forms/')
#addLink(fm, 'Directives', '/directives/')
#structure.append(fm)

return structure
