## Script (Python) "getDefaultPhoto"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##

from wres.policy.utils.utils import getDefaultPhotoUrl

url = getDefaultPhotoUrl()

return url


