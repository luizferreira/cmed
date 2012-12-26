from wres.archetypes.content.chartdata import Event

def atblob_added(context, event):
    '''
    Used to create a chart event for images and files.
    '''
    try:
        # this event is created when migrating too, but is removed later because
        # when migrating we can't determine the author, since here the author will be
        # always admin.
        context.create_event(Event.CREATION, context.created(), context)
    except AttributeError:
        pass