## coding=utf-8

import transaction


def initialize_medications_use_type(context):
    print "Inicializando o campo use_type dos medicamentos"

    catalog = context.portal_catalog
    query = dict(meta_type="Patient")
    brains = catalog.searchResults(query)
    for b in brains:
        obj = b.getObject()

        meds = obj.chart_data.get_entry('medications').values()

        prescriptions = obj.chart_data.get_entry('prescriptions').values()
        for presc in prescriptions:
            meds += presc['data']['medications']

        for med in meds:
            if 'use_type' not in med['data']:
                med['data']['use_type'] = '--'
                print 'Paciente: %s' % obj.getFullName()
            else:
                if med['data']['use_type'] == '':
                    med['data']['use_type'] = '--'
                    print 'Paciente: %s' % obj.getFullName()
    transaction.commit()
    print "..."
    print "Pronto!\n"
