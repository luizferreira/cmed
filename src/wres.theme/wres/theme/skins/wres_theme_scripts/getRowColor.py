##Script (Python) "getRowColor"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=visit
color = ''
state = visit["getReviewState"]
if state == "concluded":
    color = "green"
elif state == "non-show" or state == "unscheduled":
    color = "red"
elif state == "confirmed":
    color = "light"
elif state == "running":
    color = "yellow"
return color