# coding=utf-8

"""Definition of the InitialVisit content type
"""
from DateTime import DateTime

from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName

from zope.interface import implements

from Products.Archetypes import atapi
from Products.Archetypes.public import DisplayList
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from wres.archetypes.interfaces import IInitialVisit
from wres.archetypes.config import PROJECTNAME
from wres.archetypes.content.medicaldocument import MedicalDocument
from wres.archetypes.content.schemas.initialvisit import InitialVisitSchema

from wres.policy.utils.utils import getWresSite


class InitialVisit(MedicalDocument):
    """InitialVisit"""
    implements(IInitialVisit)

    meta_type = "InitialVisit"
    schema = InitialVisitSchema

    security = ClassSecurityInfo()
    
    security.declarePublic('Title')

    def getReactionValues(self):
        return DisplayList(( 
                        ('Non Specified', 'Não especificada'),
                        ('Rash', 'Irritação'), ('collapse', 'Colapso'),
                        ('Unable to breath',  'Dificuldade em respirar'),
                        ))

    def getStatusValues(self):
        return DisplayList(( 
                        ('active', 'Ativo'),
                        ('inactive', 'Inativo'),
                        ))
                        
    def at_post_edit_script(self):
        self.distributeNotSignedDocumentData()
        
    def at_post_create_script(self):
        self.setTitle('Primeira Visita')
        vt = getToolByName(self, 'vocabulary_tool')
        vt.extractFieldValues(self)

#    security.declarePublic('canSignPn')
#    def canSignPn(self, doctor, entered_passwd):
#        error = doctor.validateSignPassword(entered_passwd)
#        return error == None
#
#    prefDict = {} # dicionario de preferencias
#    top = [] # as complaints mais usadas
#    MAX_TOP = 10 # maximo numero de complaints mais usadas
#    MAX_DICT = 1000 # numero maximo de palavras distintas que podem haver 
#                    # no dicionario
#
#    diagnosis_top_size = 10  # ten top diagnosis
#    diagnosis_top = []  # codes most frequently used
#    diagnosis_usage = {}  # stores usage of each diagnose
#
#
#    def getPulseNames(self, instance=None):
#        return PULSE_NAMES
#
#    def getPhysicalNames(self, instance=None):
#        return PHYSICAL_NAMES
#
#    def getReactionValues(self, instance=None):
#        return REACTION_VALUES
#    
#    def getAllergyValues(self, instance=None):
#        return ALLERGY_VALUES
#    
#    def getPrefDict(self):
#        return DocumentType.prefDict
#    getPrefDict = classmethod(getPrefDict)
#
#    def getTop(self):
#        return DocumentType.top
#    getTop = classmethod(getTop)
#
#    def __updateTop(self, complaint):
#        top = DocumentType.top # mais facil de escrever
#        prefD = DocumentType.prefDict
#
#        if complaint not in top:
#            top.append(complaint)
#            # ordena em relacao ao valor da chave no dicionario
#            # do maior valor pro menor valor devido ao - na frente
#            # do cmp
#            top.sort(lambda x, y: -cmp(prefD[x], prefD[y]))
#
#    def __updatePrefDict(self, complaint):
#        """Atualiza o dicionario de classe com a reclamacao passada
#        Incrementando de 1 o valor da chave no dicionario caso exista
#        e setando para 1 caso nao exista"""
#
#        prefD = DocumentType.prefDict
#
#        if prefD.has_key(complaint):
#            prefD[complaint]+=1
#        else:
#            prefD[complaint] = 1
#
#        if len(prefD) >= DocumentType.MAX_DICT:
#            items = prefD.items()
#            items.sort(lambda x, y: -cmp(x[1], x[1])) # retirar os itens de
#                                                      # menor ocorrencia
#            items=items[:DocumentType.MAX_DICT*2/3] # elimina 1/3 do dicionario
#            prefD=dict(items)
#
#    def setChief_complaint(self, value, **kw):
#        self.schema['chief_complaint'].set(self, value, **kw)
#
#        for complaint in value:
#            self.__updatePrefDict(complaint)
#            self.__updateTop(complaint)
#
#        DocumentType.top=DocumentType.top[:DocumentType.MAX_TOP]
#
#    ############# Diagnosis starts here #############
#    
#    def __update_diagnosis_usage(self, code):
#        """ Increments usage frequency. """
#        usage = DocumentType.diagnosis_usage
#        if code != '':
#            if usage.has_key(code):
#                usage[code] += 1
#            else:
#                usage[code] = 1
#    
#    def __existing_code(self, code, list):
#        """ Returns true if code is in list. """
#        for i in list:
#            if i[0] == code:
#                return 1
#        return 0
#    
#    def __update_diagnosis_top(self, code):
#        """ Keeps the top most used codes in __diagnosis_top. """
#        rt = getToolByName(self, REFERENCE_CATALOG)
#        usage = DocumentType.diagnosis_usage
#        top = DocumentType.diagnosis_top
#        obj = rt.lookupObject(code)
#        
#        if not self.__existing_code(code, top) and code != '':
#            top.append((code, obj)) # add code
#        top.sort(lambda a, b: -cmp(usage[a[0]], usage[b[0]]))
#        if len(top) > DocumentType.diagnosis_top_size:
#            top.pop() # remove less frequent code
#    
#    def __diagnosis_item(self, obj):
#        """ Returns a tuple defining the vocabulary item. """
#        value = obj.UID()
#        text = "%s (%s)" %(obj.getId(), obj.getDescriptionDiagnosis())
#        return (value, text)
#    
#    def diagnosis_vocabulary(self, content_instance):
#        """ Returns a list of the most frequently used codes. """
#        vocab = []
#        for code in DocumentType.diagnosis_top:
#            vocab.append(self.__diagnosis_item(code[1])) # code
#        return vocab
#    
#    def setDiagnosis(self, value, **kw):
#        """ Sets diagnose and increments codes frequency. """
#        self.schema['diagnosis'].set(self, value, **kw)
#        for code in value:
#            self.__update_diagnosis_usage(code.get('description'))
#            self.__update_diagnosis_top(code.get('description'))
#    
#    ############# Diagnosis ends here #############
#
#    def setDoctor(self, value, **kw):
#        self.aq_parent.setDoctor(value, **kw)
#    
#    def at_post_create_script(self):
#        self.updateRelatedEncounter()
#        self.setDate(now())
#        self.distributeNotSignedDocumentData()
#        patient = self._getPatient()
#        patient.setType_of_patient('estabilished')
#        if not hasattr(self, 'reviewofsystems'):
#            _createObjectByType('ReviewOfSystems', self, 'reviewofsystems')
#        self.setRos(self.reviewofsystems.UID())
#        birth = self._getPatient().getBirthDate()
#        if birth is None:
#            idade = ''
#        else:    
#            idade = self.calculeAge(birth)
#        self.setCurrent_age(idade)
#
#
#    def manage_beforeDelete(self, item, container):
#        self.deleteNotSignedDocumentData()
#        BaseFolder.manage_beforeDelete(self, item, container)
#
#    def _processForm(self, data=1, metadata=None, REQUEST=None, values=None):
#        BaseFolder._processForm(self, data, metadata, REQUEST, values)
#        request = REQUEST or self.REQUEST
#        if values:
#            form = values
#        else:
#            form = request.form
#        fieldset = form.get('fieldset', None)
#        localonly = form.get('localonly', None)
#
#    def getFiller(self):
#        """ """
#        mt = getToolByName(self, 'portal_membership')
#        member = mt.getAuthenticatedMember()
#        return member.getId()
#
#    def getLastPN(self):
#        pc = getToolByName(self, 'portal_catalog')
#        brains = pc.searchResults(meta_type='ProgressNotes',
#                                  sort_on='Date',
#                                  sort_order='descending',
#                                  sort_limit=3,
#                                  path={'query':self.chartFolder.absolute_url(1)})
#        if len(brains) >= 2:
#            return brains[1].getObject()
#        return ''
#
#    def get_text(self, name):
#        if name == 'abdomen':
#            return 'Abdomen macio, Nenhum problema presente em órgãos e Não há massa palmável'    
#        #return 'Abdomen is soft, Non tender with no organomegaly, No masses are palpable'
#        if name == 'extremities':
#            return 'Pulso femural 3+ e igual, Pulsos distais intactos, Nenhuma deformidade nas juntas, Sem edema no tornozelo, Sinal de agreção ausente'
#        #return 'Femoral pulses 3 + and equal, Distal pulses intact, No joint deformity, No ankle edema \nNo clubbing'
#        if name == 'ge':
#            return 'nenhum distress agudo, sinal de alerta, ou qualquer problema em história médica pregreça'
#        #return 'Appears in no acute distress, Awake, Alert, Oriented times three, Providing proper history'
#        if name == 'gu':
#            return 'difere de GU, exame de próstata nao realizado, genitalia externa com aparencia normal'
#        #return 'Deferred to GU, Prostate exam not done, External genitalia normal in appearance'
#        if name == 'heent':
#            return 'cabeça sem traumatismo cranio encefálico, nao há traumas no canal auditivo, membbrana timpanica intacta,\nPERLA,EOM full, garganta limpa sem exudato, mucosa rosea e umida'
#        #return 'Head is Normocephalic, Ear canal is non traumatic, Tympanic membranes are intact \nPERLA, EOM full, Throat clear without exudates, Mucosa is pink and moist.'
#        if name == 'heart':
#            return 'PMI está no quinto ICS, MCL, impulso apical é normal, nao ha sons no coração, normalidade, nao há murmuros significantes'
#        #return 'PMI is on the 5Th ICS, MCL, Apical impulse is normal \nHeart sounds are normal with normal S1, S2. No S3, S4. \nThere are no significant murmurs, There are no rubs'
#        if name == 'lungs':
#            return 'campos pumorares estao limpos sem chiado, crepitação, ou ronco, pulmoes limpos para auscuta e percussao'
#        #return 'Lung fields are clear without wheezes, rales, crepitations, rubs or rhonchi \nLungs are clear to auscultation and percussion'
#        if name == 'neck':
#            return 'pescoço flexivel sem JVD, pulso carotídeo normal'
#        #return 'Neck is supple with no JVD, Carotid upstrokes are normal, There are no carotid bruits'
#        if name == 'neurological':
#            return 'Reflexo patelar normal e igual bilateralmente, força normal e intacta bilareamente'
#        #return 'Deep tendon reflexes are 3 + and equal bilaterally, Strength and sensation intact bilaterally'
#        if name == 'og':
#            return 'difere ob de gyn, exame pelvico nao realizado,  seios sem massa palpável ou sensibilidade'
#        #return 'Deferred to OB/GYN, Pelvic exam not done, Breasts have no palpable masses or tenderness'
#        if name == 'skin':
#            return 'sem pruridos ulceras e ferimentos recentes'
#        #return 'No rashes, No pressure sores, No recent wounds.'
#        return ''
#
#    def defaultPhysicalText(self):
#        if self.isInitialVisit():
#            return self.getPhysicalDefaultValues()
#        else:
#            return []
#
#    def getPhysicalDefaultValues(self):
#        def createDict(name):
#            return {'name': name,
#                    'description': self.get_text(name),}
#        default_items = ['ge', 'heent', 'neck', 'lungs', 'heart', 'abdomen', 'gu', 'og', 'extremities', 
#                         'neurological', 'skin']
#        return [createDict(item) for item in default_items]
#
#    def getPulseAttributes(self):
#        def createDict(name):
#            if name != 'exhibit':
#                return {'name': name,
#                        'superficial_temporal': '',
#                        'carotid': '',
#                        'axillary': '',
#                        'brachial': '',
#                        'radial': '',
#                        'ulnar': '',
#                        'femoral': '',
#                        'popliteal': '',
#                        'dorsalis_pedis': '',
#                        'posterior_tibial': '',}
#            else:
#                return {'name': name,
#                        'superficial_temporal': '0',
#                        'carotid': '0',
#                        'axillary': '0',
#                        'brachial': '0',
#                        'radial': '0',
#                        'ulnar': '0',
#                        'femoral': '0',
#                        'popliteal': '0',
#                        'dorsalis_pedis': '0',
#                        'posterior_tibial': '0',}
#        pulse_attributes = ['exhibit', 'right', 'left']
#        return [createDict(item) for item in pulse_attributes]
#
#    def isInitialVisit(self):
#        parent = self.aq_parent
#        if parent is None:
#            return False
#        else:
#            return parent.isInitialVisit()
#
#    def getTypeOfVisit(self):
#        from Products.CMFUEMR.utils import getFieldVocabularyName
#        return getFieldVocabularyName(self.aq_parent, 'typeOfVisit')
#
#    def getKeyLabel(self, key):
#        if self.isInitialVisit():
#            return self.iv_mapping.get(key, key)
#        else:
#            return key
#
#    def getBlood_pressure(self):
#        bp = self.blood_pressure
#        if not isinstance(bp, type({})):
#            return {}
#        else:
#            return bp
#
    def deleteNotSignedDocumentData(self):
        patient = self.getPatient()
        source = self.getPhysicalPath()
        patient.chart_data.del_not_signed_allergies(source)

    def distributeNotSignedDocumentData(self):
        patient = self.getPatient()
        date = self.getDateOfVisit()
        source = self.getPhysicalPath()
        allergies = self.getAllergies()
        new_allergies = []
        for allergy in allergies:
            if allergy.get('allergy'):
                new_allergy = {}
                new_allergy['allergy'] = allergy['allergy']
                new_allergy['reaction'] = allergy['reaction']
                new_allergies.append(new_allergy)
        patient.chart_data.add_not_signed_allergies(date, source, new_allergies)

    def distributeDataInChart(self):
        self.deleteNotSignedDocumentData()
        patient = self.getPatient()
        date = self.getDateOfVisit()
        source = self.getPhysicalPath()
        self.__distributePrescriptions(patient, date, source)
        #self.__distributePastHistory(patient, date, source)
        self.__distributeAllergies(patient, date, source)
        #self.__distributePlans(patient, date, source)
        #self.__distributeFollowUp(patient, date, source)
        self.__distributeVitalSigns(patient, date, source)
        self.__distributeLaboratory(patient, date, source)
        self.__distributeMedications(patient, date, source)
        #self.__distributeImmunizations(patient, date, source)
        self.__distributeAllDiagnosis(patient, date, source)
        #self.__updateRelatedEncounter()

    def __distributePrescriptions(self, patient, date, source):
        prescriptions = self.getPrescription()
        for prescription in prescriptions:
            prescription['submitted_by'] = self.getDoctor().getId()
            patient.savePrescription(**prescription)

    def __distributePastHistory(self, patient, date, source):
        histories = patient.chart_data.histories
        past_history = self.getPast_history()
        for id, value in past_history.items():
            histories.add_entry(id, date, source, value)

    def __distributeAllergies(self, patient, date, source):
        allergies = self.getAllergies()
        new_allergies = []
        for allergy in allergies:
            if allergy.get('allergy'):
                new_allergy = {}
                new_allergy['allergy'] = allergy['allergy']
                new_allergy['reaction'] = allergy['reaction']
                new_allergies.append(new_allergy)
        if len(new_allergies) > 0 :
            patient.chart_data.add_entry_to('allergies', date, source, new_allergies)

    #def __distributePlans(self, patient, date, source):
        #plan = self.getNon_prescription()
        #if plan:
            #patient.chart_data.add_entry_to('plans', date, source, plan)

#    def __distributeFollowUp(self, patient, date, source):
#        followup_number = self.getFollowup_number()
#        quant = followup_number.get('followup_quant', 0)
#        unit = followup_number.get('followup_unit')
#        f_number_filled = (quant > 0) and unit
#        follow_up_notes = self.getFollow_up()
#        if f_number_filled or follow_up_notes:
#            data = {'date': followup_number, 'note': follow_up_notes}
#            chart_data = patient.chart_data
#            chart_data.add_entry_to('follow_up_notes', date, source, data)
#
    def __distributeVitalSigns(self, patient, date, source):
        vital_signs = self.getVital_signs()
        chart_data = patient.chart_data
        for vital in vital_signs:
            chart_data.add_entry_to('vital_signs', date, source, vital)
            
    def __distributeLaboratory(self, patient, date, source):
        labs = self.getLaboratory()
        chart_data = patient.chart_data
        for lab in labs:
            chart_data.add_entry_to('laboratory', date, source, lab)

    #def __distributeImmunizations(self, patient, date, source):
        #immunizations = self.getImmunization()
        #typed = immunizations.get('typed', [])
        #if typed:
            #chart = patient.chart_data
            #chart.add_entry_to('immunizations', date, source, typed)

    def __distributeMedications(self, patient, date, source):
        chart = patient.chart_data
        medications = self.getMedication_taken()
        for medication in medications:
            medication['status'] = 'active'
            chart.add_entry_to('medications', date, source, medication)

    def __distributeAllDiagnosis(self, patient, date, source):
        chart = self.chart_data
        diagnosis = self.getDiagnosis()
        member = self.portal_membership.getAuthenticatedMember()
        for diagnose in diagnosis:
            #if diagnose and diagnose.get('active') == 'active':
            if diagnose:
                problem = {'problem': diagnose['desc'],
                           'code': diagnose['code'],
                           'started': diagnose['date'],
                           'end_date': diagnose['date'],
                           'state': diagnose['status'],
                           'submitted_by': member.id,
                           'submitted_on': DateTime(),
                           'chronicity': '',}
                id = self.generateUniqueId('Problem')
                chart.add_entry_to_problems(id, date, source, problem)

#    def __updateRelatedEncounter(self):
#        encounter = self.getEncounter()
#        if encounter is not None:
#            encounter.append_related_document(self.UID())
#            encounter_prescs = encounter.getPrescription()
#            prescriptions = self.getPrescription()
#            new_prescs = encounter_prescs + prescriptions
#            encounter.setPrescription(new_prescs)
#
#    def import_allergies(self, content_instance=None, **kw):
#        return self.getAllAllergies()
###        temp = self.getAllAllergies()
###        return [allergy['allergy'] for allergy in temp]
#
    #def getImmunization(self):
        #value = self.immunization
        #if type(value) == type([]):
            #return {'typed': value,
                    #'imported': [],
                    #'checked': False,
                    #}
        #return value
#
#    def import_immunizations(self):
#        result = []
#        patient = self._getPatient()
#        chart = patient.chart_data
#        immunizations = chart.immunizations
#        for value in immunizations.values():
#            if value['came_from'] != 'questionnaire':
#                result.extend(value['data'])
#        return result
#
    #def getMedication_taken(self):
        #value = self.medication_taken
        #if type(value) == type([]):
            #return {'typed': value,
                    #'imported': [],
                    #'checked': False,
                    #}
        #return value

#    def import_medications(self):
#        result = []
#        patient = self._getPatient()
#        chart = patient.chart_data
#        medications = chart.medications
#        for value in medications.values():
#            if value['came_from'] != 'questionnaire':
#                result.extend(value['data'])
#        return result
#        
#    def getDiferenceYears(self, today, bd):
#        return (today.year()-bd.year())
#
#    def getAge(self, age, today, bd):
#        today = DateTime(today.dayOfYear())
#        bd = DateTime(bd.dayOfYear())
#        if today.lessThan(bd):
#            return (age - 1)
#        return age
#
#    def calculeAge(self, birthdate):
#        today = DateTime()
#        bd = birthdate   
#        return self.getAge(self.getDiferenceYears(today, bd), today, bd)
#    
#    
#    def getWorkflowStatus(self):
#        from Products.CMFUEMR.utils import getObjWorkflowStatus
#        return getObjWorkflowStatus(self.portal_workflow, self);
#        
#    def setDoctor(self, value, **kw):
#        field = self.Schema().getField('doctor')
#        field.set(self, value, **kw)
#        doctor = self.getDoctor()
#        setReviewerRole(self, doctor.getId())
#
#    def setRoutableValue(self, id):
#        brains = self.uid_catalog.search({'UID': id})
#        obj = brains[0].getObject()
#        self.setRoutable(obj)
#
#    def getVocabularyProvider(self, content_instance=None, **kw):
#        from Products.CMFCore.utils import getToolByName
#        from Products.Archetypes import config
#        field = kw['field']
#        pairs = []
#        uc = getToolByName(self, config.UID_CATALOG)
#
#        allowed_types = field.allowed_types
#
#        if allowed_types:
#            skw = {'portal_type': allowed_types,
#                   'sort_on': 'Title',
#                   }
#        else:
#            skw = {}
#
#        filter_indexes = getattr(field, 'filter_indexes', False)
#        if filter_indexes:
#            skw.update(filter_indexes)
#        brains = uc.searchResults(**skw)
#        
#        if field.vocabulary_custom_label is not None:
#            label = lambda b:eval(field.vocabulary_custom_label, {'b': b})
#        elif len(brains) > field.vocabulary_display_path_bound:
#            at = i18n.translate(domain='archetypes', msgid='label_at',
#                                context=content_instance, default='at')
#            label = lambda b:'%s %s %s' % (b.Title or b.id, at,
#                                           b.getPath())
#        else:
#            label = lambda b:b.Title or b.id
#
#        pairs = [(b.UID, label(b)) for b in brains]
#
#        if not field.required and not field.multiValued:
#            no_reference = i18n.translate(domain='archetypes',
#                                          msgid='label_no_reference',
#                                          context=content_instance,
#                                          default='<no reference>')
#            pairs.insert(0, ('', no_reference))
#
#        __traceback_info__ = (content_instance, field.getName(), pairs)
#        return DisplayList(pairs)
#
#    def getRouteVocabulary(self, content_instance=None, **kw):
#        from Products.CMFCore.utils import getToolByName
#        from Products.Archetypes import config
#        field = kw['field']
#        pairs = []
#        uc = getToolByName(self, config.UID_CATALOG)
#
#        allowed_types = field.allowed_types
#
#        if allowed_types:
#            skw = {'portal_type': allowed_types,
#                   'sort_on': 'Title',
#                   }
#        else:
#            skw = {}
#
#        filter_indexes = getattr(field, 'filter_indexes', False)
#        if filter_indexes:
#            skw.update(filter_indexes)
#        brains = uc.searchResults(**skw)
#        
#        if field.vocabulary_custom_label is not None:
#            label = lambda b:eval(field.vocabulary_custom_label, {'b': b})
#        else:
#            label = lambda b:b.Title or b.id
#
#        pairs = [(b.UID, label(b)) for b in brains]
#        
#        __traceback_info__ = (content_instance, field.getName(), pairs)
#        return DisplayList(pairs)
#
#    def allowedContentTypes(self):
#        """ returns the types that can be added to the object.
#        if a DocumentType has already been added then remove DocumentType
#        from the allowed types."""
#        if not hasattr(aq_base(self), '_v_act'):
#            self._v_act = BaseFolder.allowedContentTypes(self)
#        act = self._v_act
#        if hasattr(self, 'doctype'):
#            act = [item for item in act if item.Metatype() != 'DocumentTypePlastica']
#        return act
#
#    def manage_afterEdit(self):
#        def getChartFolder(context):
#            while context.meta_type != 'ChartFolder':
#                context = context.aq_parent
#            return context
#        
#        date_of_visit = self.getDateOfVisit()
#        if date_of_visit is None:
#            date_of_visit = self.getDate()
#        
#        encounters = self.get_encounters_of(date_of_visit)
#        if encounters:
#            encounter = encounters[0]
#            date_of_visit = encounter.getDate_of_visit()
#            #print "Already existing encounter gets referred."
#        else:
#            type_name = 'Encounter'
#            chartFolder = getChartFolder(self)
#            id = chartFolder.encounters.generateUniqueId(type_name)
#            chartFolder.encounters.invokeFactory(type_name=type_name, id=id)
#            encounter = chartFolder.encounters[id]
#            encounter.setDate_of_visit(date_of_visit)
#            #print "New encounter is being created."
#        encounter.append_related_document(self.UID())
#        self.setDateOfVisit(date_of_visit)
#        self.setEncounter(encounter.UID())
#        
#        if not ('doctype' in self.objectIds()):
#            from Products.CMFUEMR.PInformationTypes.DocumentType import\
#                 addDocumentType
#            addDocumentType(self, 'doctype')
#            doctype = self['doctype']
#            self.setSoap(doctype.UID())
#   
#    def at_post_create_script(self):
#        self.updateRelatedEncounter()
#        tipo = self.getMajorTypeOfVisit() # sandro migrando - Alterei getTypesOfDocument(self) para self.getMajorTypeOfVisit()
#        if 'ivp' in tipo:
#            _createObjectByType('DocumentTypePlastica', self, 'doctype')
#        elif 'bpo' in tipo:
#            _createObjectByType('DocumentTypeBoletim', self, 'doctype')
#        else:
#            _createObjectByType('DocumentType', self, 'doctype')
#        doctype = self['doctype']
#        self.setSoap(doctype.UID())
#        doctype.at_post_create_script()
#
#    def vocabularyTypeOfVisit(self):
#        mtov = self.getMajorTypeOfVisit()
#        default = TYPES_OF_PROGRESS_NOTES
#        return self.MAPPING_TYPE_OF_VISIT.get(mtov, default)
#
#    def getType(self):
#        mtov = self.getMajorTypeOfVisit()
#        return TYPE_OF_VISIT.getValue(mtov)
#
#    def getMajorTypeOfVisit(self):
#        key = 'majorTypeOfVisit'
#        inst_value = getattr(self, key, 'pn')
#        request = self.REQUEST
#        to_return = request.get(key, inst_value)
#        return to_return
#
#    def isInitialVisit(self):
#        return self.getMajorTypeOfVisit() in ('iv', 'cn')
#
#    def Date(self):
#        dateofvisit = self.getDateOfVisit()
#        if dateofvisit is not None:
#            return dateofvisit
#        return self.getDate()
#    
#    def get_encounters_of(self, date_of_visit):
#        pc = self.portal_catalog
#        chart_folder = self.chartFolder
#        brains = pc.search({'meta_type': 'Encounter',
#                            'path': '/'.join(chart_folder.getPhysicalPath()),
#                            })
#        encounters = [b.getObject() for b in brains if self.isSameDay(b.getObject().date_of_visit, date_of_visit)]
#        return encounters
#
#    def isSameDay(self, d1, d2):
#        if d1 is None or d2 is None:
#            return False
#        return (d1.year() == d2.year() and d1.month() == d2.month() and d1.day() == d2.day())
#
#    def patient_encounters(self):
#        pc = self.portal_catalog
#        chart_folder = self.chartFolder
#        brains = pc.search({'meta_type': 'Encounter',
#                            'path': '/'.join(chart_folder.getPhysicalPath()),
#                            })
#        return [(b.UID, b.Title) for b in brains]
#

atapi.registerType(InitialVisit, PROJECTNAME)
