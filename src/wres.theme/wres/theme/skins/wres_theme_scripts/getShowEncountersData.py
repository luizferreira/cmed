#TODO Atualmente não utilizado - Deixar o destino deste script para ser decidido no futuro.
#def proccess_encounters(encounters):
    #result = []
    #for index, encounter in enumerate(encounters):
        #add_encounter(result, index, encounter)
    #return result

#def document_link(document):
    #if document.meta_type == 'ProgressNotes':
        #document = document.doctype
    #return document.absolute_url()

#def add_encounter(container, index, encounter):
    #new = {}
###    new.update(encounter)
    #date = encounter.getDate_of_visit()
    #if not date:
        #return
    #formatted_date = date.strftime('%d/%m/%Y')
    #new['date_of_visit'] = formatted_date
    #new['title'] = encounter.Title()
    #new['link'] = encounter.absolute_url()
    #if (index + 1) % 2 == 0:
        #css_class = 'even'
    #else:
        #css_class = 'odd'
    #new['class'] = css_class
    #new['related_documents'] = related_documents(encounter)
    #new['prescriptions'] = prescriptions(encounter)
    #container.append(new)

#def related_documents(encounter):
    #result = []
    #documents = encounter.getRelated_documents()
    #for document in documents:
        #add_document(result, document)
    #return result

#def add_document(container, document):
    #result = {'link': document_link(document),
              #'title': document.Title(),
              #}
    #container.append(result)

#def prescriptions(encounter):
    #result = []
    #prescriptions = encounter.getPrescription()
    #for prescription in prescriptions:
        #add_prescription(result, prescription)
    #return result

#def add_prescription(container, prescription):
    #container.append(prescription['medication'])

#result = {}
#encounters = context.getEncounters()
#encounters = proccess_encounters(encounters)
#result['encounters'] = encounters
#return result
