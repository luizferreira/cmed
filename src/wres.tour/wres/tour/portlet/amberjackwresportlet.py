from plone.portlets.interfaces import IPortletDataProvider
class IAmberjackWresPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    user_title = schema.TextLine(
                        title=_(u"Describe this set of tours"),
                        description=_(u"This text will appear as portlet's title"),
                        required=False,
                        )

    tours = schema.List(
                title=_(u"Choose the tours"),
                description=_(u"Select the tours that can be choosen by an user on this portlet"),
                value_type=schema.Choice(
                              vocabulary="collective.amberjack.core.tours",
                              required=True)
                )


    skinId = schema.Choice(title=_(u"Choose the skin"),
                              description=_(u"Indicate the tour's window layout"),
                              vocabulary="collective.amberjack.skins",
                              default="sunburst")