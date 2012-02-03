##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##
return state.set(status='success',\
                 portal_status_message='Your changes have been saved')
