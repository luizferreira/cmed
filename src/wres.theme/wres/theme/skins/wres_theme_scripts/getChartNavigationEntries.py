request = context.REQUEST
current_url = request.URL

TEMPLATE_ID = current_url.split('/')[-1]
def createGroup(name):
    return {'group_id': name.lower().replace(' ', '_'),
            'title': name,
            'links': [],
            }
def addLink(group, text, href, icon='document_icon.gif'):
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
addLink(mc, 'Eventos', '/show_events', icon='vcal.png')
addLink(mc, 'Consults', '/documents', icon='copy_icon.png')
addLink(mc, 'Impressos', '/impressos', icon='print_icon.png')
addLink(mc, 'Arquivos Externos', '/upload', icon='upload_icon.png')
addLink(mc, 'Medicamentos e Prescrições', '/show_medications', icon='add_icon.png')
addLink(mc, 'Problem List', '/show_problem_list', icon='error_icon.gif')
addLink(mc, 'Alergias', '/show_allergies', icon='contentrules_icon.png')
addLink(mc, 'Exames', '/show_exams', icon='exams_icon.png')

structure.append(mc)

return structure
