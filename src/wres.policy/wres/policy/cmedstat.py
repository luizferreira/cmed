import requests
from Products.CMFCore.utils import getToolByName

def request_stat_registration(context):

    prefix = 'cmed_'
    site = "http://cstat.communi.com.br/cmed_stat"

    mt = getToolByName(context, 'portal_membership')
    member = mt.getAuthenticatedMember()
    username = member.getUserName()

    params = {}
    params[prefix + 'url'] = context.REQUEST.URL
    params[prefix + 'user'] = username
    params[prefix + 'roles'] = '__'.join(member.getRoles())

    try:
        result = requests.get(site, params=params)
    except requests.ConnectionError:
        result = None

    return result