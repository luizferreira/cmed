request = context.REQUEST
opener_url = request.get('opener_url')
opener_type = request.get('opener_type', '')
##from Products.zdb import set_trace; set_trace()
if opener_type == 'Visit' or opener_type == 'Visit':
    return context.instantiateVisitObject()
else:
    return context.restrictedTraverse(opener_url)
