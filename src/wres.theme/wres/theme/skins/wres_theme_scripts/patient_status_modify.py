##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None

#Define basics variables
request = context.REQUEST.form
action = request['workflow_action']

if action not in ['activate','inactivate']:
    container.REQUEST.RESPONSE.redirect(container.Patients.absolute_url() + "?portal_error_message=Não foi possível realizar a operação")
else:
    if context.portal_type == "ChartFolder":
        # desativando paciente pelo prontuario
        patient = context.getParentNode()
    else:
        # desativando paciente pelo view do paciente
        patient = context

    patient.doWorkflowAction(action) # muda o estado

    patient.showOrHide(action) # expira ou "desespira" o paciente.

    if action == "activate":
        container.REQUEST.RESPONSE.redirect(container.Patients.absolute_url() + "	?portal_status_message=" + context.getFullName() +  " foi reativado com sucesso")
    else:
        container.REQUEST.RESPONSE.redirect(container.Patients.absolute_url() + "	?portal_status_message=" + context.getFullName() +  " foi desativado com sucesso")
