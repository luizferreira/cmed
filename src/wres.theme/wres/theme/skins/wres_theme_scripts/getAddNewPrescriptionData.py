from DateTime import DateTime
today = DateTime()
return {'shown_start': today.strftime('%d/%m/%Y')}
