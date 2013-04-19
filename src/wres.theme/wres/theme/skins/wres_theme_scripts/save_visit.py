## Script (Python) "edit_and_publish"
  ##title=Edit content
  ##bind container=container
  ##bind context=context
  ##bind namespace=
  ##bind script=script
  ##bind state=state
  ##bind subpath=traverse_subpath
  ##parameters=
  ##
  import ipdb;ipdb.set_trace()
  from Products.CMFCore.utils import getToolByName

  #Save changes normal way
  context.processForm()
  portal_workflow = getToolByName(context, 'portal_workflow', None)
  #change workflow
  if portal_workflow.getInfoFor(context,'review_state') != 'published':
      try:
          portal_workflow.doActionFor(context,'publish')
          portal_status_message = "Changes saved and document published"
      except:
          pass
  return context.REQUEST.RESPONSE.redirect("%s?portal_status_message=%s"%(
      context.absolute_url(),portal_status_message))