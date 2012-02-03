##parameters=id=None
if id is None:
    id = 'EmptyVisit'
from wres.policy.utils.utils import createVisitObject
return createVisitObject(context, id)
