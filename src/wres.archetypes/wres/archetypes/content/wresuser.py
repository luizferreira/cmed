# encoding=utf-8

"""Definition of the WRESUser content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

from AccessControl import ClassSecurityInfo

from plone import api

from wres.archetypes.interfaces import IWRESUser
from wres.archetypes.config import PROJECTNAME
from wres.policy.utils.utils import create_base_of_id

def create_id(portal_registration, first_name, last_name):
    """ Essa função testa se o id já está em uso e caso
    afirmativo concatena um número ao id para desambiguação
    Chamada por generateNewId()
    """
    base = create_base_of_id(first_name, last_name)
    new_id = base
    num = 0
    pr = portal_registration
    while not pr.isMemberIdAllowed(new_id):
        num += 1
        new_id = "%s%s" % (base, num)
    return new_id

#
#def verify_id_coherence(id, first_name, last_name):
#    base = create_base_of_id(first_name, last_name)
#    starts_with_base = id.startswith(base)
#    import re
#    pattern = re.compile('^\d*$')
#    ends_with_numbers = re.match(pattern, id[len(base):])is not None
#    return starts_with_base and ends_with_numbers

def create_uemr_user(related_object, user_id, email='', fullname=''):
    pr = getToolByName(related_object, 'portal_registration')
    pm = getToolByName(related_object, 'portal_membership')
    uf = getToolByName(related_object, 'acl_users')
    if email == '':
        email = 'sem@email.com'

    if related_object.getGroup() == 'Patient':
        import string, random
        password = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(20)])
        pr.addMember(
            user_id, password,
            properties={
                'home_url': related_object.get_home_url(),
                'username': user_id,
                'email': email,
                'fullname': fullname,
                'related_object': '/'.join(related_object.getPhysicalPath()[2:]), # removing instance name from path.
            },
        )
    else:
        pr.addMember(
            user_id, 'senha1',
            properties={
                'home_url': related_object.get_home_url(),
                'username': user_id,
                'email': email,
                'fullname': fullname,
                'related_object': '/'.join(related_object.getPhysicalPath()[2:]), # removing instance name from path.
            },
        )
    #uf.changeUser(user_id, groups=[related_object.getGroup()])
    #pm.setLocalRoles(obj=related_object, member_ids=(user_id,), member_role='Owner')
    uf.userSetGroups(user_id, [related_object.getGroup()])
    pm.createMemberArea(member_id=user_id)

WRESUserSchema = folder.ATFolderSchema.copy()

schemata.finalizeATCTSchema(
    WRESUserSchema,
    folderish=True,
    moveDiscussion=False
)


class WRESUser(folder.ATFolder):
    """WRESUser type for WRES website"""
    implements(IWRESUser)

    meta_type = "WRESUser"
    schema = WRESUserSchema

    security = ClassSecurityInfo()

    def isAtCreation(self):
        return getattr(self, '_at_creation_flag')

    def getFullName(self):
        return self.getFirstName() + ' ' + self.getLastName()

    def get_home_url(self):
        """ Standard method to return the user home url.
        If it is necessary to use a specific method, it can be defined in
        user specific class. """
        return self.absolute_url_path()

    def getGroup(self):
        """ returns the group the user belongs. Must be redefined in the
            subclasses.
        """

#    Se for patient, o login sera luizfonseca, senao sera lfonseca.
#    No estagio atual, falta modificar o title. No membership ja
#    esta criando um usuario com a id certa.
    def at_post_create_script(self):
        """ Esse método é chamado no momento da criação de um objeto da classe.
        Ele cria um membro no acl_users com as informações obtidas da classe filha.
        """
        self.formatName()
        user_id = self.getId()

        pm = getToolByName(self, 'portal_membership')
        uf = getToolByName(self, 'acl_users')
        member = pm.getMemberById(user_id)
        fullname = self.getFullName()
        email = self.getEmail()
        if member is None:
            create_uemr_user(self, user_id, email=email, fullname=fullname)
        # when migrating (importing) the member will be already created.
        else:
            pm.createMemberArea(member_id=user_id)
            uf.userSetGroups(user_id, [self.getGroup()])
            member.setMemberProperties(dict(home_url=self.get_home_url(),
                                related_object = '/'.join(self.getPhysicalPath()[2:]))) # removing instance name from path.

#        else:
#            update_member_data(member, self, fullname=fullname, email=email)

    def at_post_edit_script(self):
        self.formatName()

    #===========================================================================
    # _at_rename_after_creation = True faz com que o metodo generateNewId seja
    # chamado no momento da criação de um novo usuário
    #===========================================================================
    _at_rename_after_creation = True
    def generateNewId(self):
        """ Create an id based on the last name of an user.
        """
        lname = self.getLastName()
        fname = self.getFirstName()
        old_id = self.getId()
        pm = getToolByName(self, 'portal_membership')
        if not pm.getMemberById(old_id):
            pr = getToolByName(self, 'portal_registration')
            return create_id(pr, fname, lname)
        else:
            return old_id

    def formatName(self):
        firstName = self.capitalizeLetters(self.getFirstName())
        lastName = self.capitalizeLetters(self.getLastName())
        self.setFirstName(firstName)
        self.setLastName(lastName)
        self.reindexObject()

    def capitalizeLetters(self, name):
        ignored_words = ['da','de','di','do','das','dos','e']
        cap_name = []
        name = unicode(name, "utf-8")
        parts = name.lower().split(' ')
        for part in parts:
            if part not in ignored_words:
                part = part.capitalize()
            cap_name.append(part)
        cap_name = ' '.join(cap_name)
        return cap_name

    def post_validate(self, REQUEST, errrors):
        """
        o Aqui mudamos a senha. Importante destacar que, neste momento, a 
          senha atual e as novas senhas já foram validadas. (no validador 
          individual no campo password e no método pre_validate)
        o Utilizamos esse método porque ele garante que todas as validações já
          foram feitas. Se isso não fosse verdade, a validação da senha atual
          não passaria, uma vez que acabamos de mudá-la.
        """
        # precisamos verificar que o objeto possui o campo newPassword, uma vez 
        # que, apesar de não possuir uma senha, o paciente também é um wresuser.
        if hasattr(self, 'getNewPassword'):
            if self.getNewPassword():

                rtool = self.portal_registration
                rtool.editMember(self.getId(), properties={}, password=self.getNewPassword())

                # não precisamos armazenar nada nos campos de passwords, eles são
                # usados apenas como método de entrada e validação. Além disso, eles
                # não criptografam os valores armazendos.
                self.setPassword('')
                self.setNewPassword('')
                self.setNewPasswordConfirmation('')

                try:
                    # envia e-mail notificando usuário da mudança de senha.
                    doctor_mail = self.getEmail()
                    message = "Sua senha foi alterada com sucesso!\n\n"
                    message += "--\n"
                    message += "Equipe CommuniMed\n"
                    api.portal.send_email(
                        recipient=doctor_mail,
                        sender='suporte@communi.com.br',
                        subject="CommuniMed: alteração de senha",
                        body=message,
                    )
                except:
                    pass

    def pre_validate(self, REQUEST, errrors):
        """
        o pre_validate é um método especial, que caso esteja presente na classe é
          chamado antes da validação de cada campo individualmente. 
        o Existe também post_validate, que é chamado depois.
        o O funcionamento é simples, acesse os campos e valores pela variável REQUEST
          e escreva os erros no dicionário errrors.
        o Este método:
            o confirma que as duas novas senhas são iguais
            o garante que o campo Senha Atual está preenchido (caso seja o próprio
              usuário mudando a sua senha).
            o torna o campo newPassword obrigatório caso esteja se criando um novo
              usuário.
            o torna o campo newPassword obrigatório caso o usuário preencheu a senha
              atual.
        """
        if 'newPassword' in REQUEST.form:
            if REQUEST.form['newPassword']:
                if REQUEST.form['newPassword'] != REQUEST.form['newPasswordConfirmation']:
                    errrors['newPassword']='Senha não confere.'
                    errrors['newPasswordConfirmation']='Senha não confere.'
                # caso o campo senha atual não esteja sendo mostrado (no caso de um
                # UemrAdmin estar editando a senha de outro médico, por exemplo), não
                # verificamos se a senha atual foi preenchida.
                if self.showPasswordCondition():
                    if not REQUEST.form['password']:
                        errrors['password']='Você precisa fornecer a senha atual.'
            # caso seja um novo usuário, precisamos nos certificar que a senha está sendo
            # preenchida.
            elif self.isAtCreation():
                    errrors['newPassword']='Você precisa definir uma senha para o novo usuário.'
                    errrors['newPasswordConfirmation']='Você precisa confirmar a senha do novo usuário.'
            # o campo password estará no formulário apenas se é o o próprio usuário
            # editando o seus dados.
            elif 'password' in REQUEST.form:
                if REQUEST.form['password']:
                    errrors['newPassword']='Você precisa fornecer a nova senha.'
                    errrors['newPasswordConfirmation']='Você precisa confirmar a nova senha.'

    def showPasswordCondition(self):
        """
        O campo password (Senha Atual) só é mostrado caso o usuário autenticado
        seja o próprio usuário ao qual o conteúdo Doctor se refere (ele esteja
        mudando a própria senha). Pois não faz sentido ele colocar a sua senha 
        atual quando estiver editando a senha de outro membro.
        """
        return self.portal_membership.getAuthenticatedMember().getId() == self.getId()                

atapi.registerType(WRESUser, PROJECTNAME)
