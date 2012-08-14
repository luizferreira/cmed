clinic = getattr(context, 'Clinic')
if clinic.meta_type != 'Clinic':
    raise Exception('Error, clinic object excepted, but got %s. Maybe you are running this script in the wrong context.', clinic.meta_type)

return_dic = {}

rua = clinic.getStreet()
numero = clinic.getNumber()
if rua == '':
    return_dic['address'] = ''
else:
    return_dic['address'] = rua + ', ' + str(numero)
bairro = clinic.getBairro()
return_dic['complemento'] = clinic.getComplemento()
return_dic['bairro'] = bairro
cidade = clinic.getCity()
return_dic['city'] = cidade
estado = clinic.getState()
return_dic['state'] = estado
return_dic['phone'] = clinic.getPhone()
return_dic['email'] = clinic.getEmail()

query = "%s, %s, %s, %s, %s" % (rua, str(numero), bairro, cidade, estado)

return_dic['map'] = "https://maps.google.com/maps/api/staticmap?center=" + query + "&zoom=15&size=512x512&maptype=roadmap&markers=color:blue%7Clabel:Aqui%7C40." + query + "&sensor=false"

return return_dic