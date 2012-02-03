##parameters=date, format
if not hasattr(date, 'strftime'):
    return date
from wres.policy.utils.utils import convertDateTime2datetime
new_date = DateTime(date)#convertDateTime2datetime(date) @ Peter Migrando, este metodo esta problematico
return new_date.strftime(format)
