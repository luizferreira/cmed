##parameters=patient
import string
my_filter = lambda x: x in string.digits
phone = ''.join(filter(my_filter, patient.getContactPhone()))
return phone