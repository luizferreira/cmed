##Script (Python) "getRowColor"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=visit
color = ''
state = visit["getReviewState"]
if state == "Concluida":
    color = "green"
elif state == "Ausente" or state == "Desmarcada":
    color = "red"
elif state == "Confirmada":
    color = "light"
elif state == "Presente":
    color = "yellow"
return color