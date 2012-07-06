from wres.archetypes.content.chartdata import Event

def atblob_added(context, event):
    '''
    Used to create a chart event for images and files.
    '''
    try:
        context.create_event(Event.CREATION, context.created(), context)
    except AttributeError:
        pass