from rest_framework import viewsets, mixins


class RLViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides default `retrieve()`, and `list()` actions.
    """
    pass

class RUViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides default `retrieve()`, `update()`,
    `partial_update()` actions.
    """
    pass

class RViewSet(mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    
    """
    A viewset that provides default `retrieve()` actions.
    """
    pass

# class ModelViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    viewsets.GenericViewSet):
#     """
#     A viewset that provides default `create()`, `retrieve()`, `update()`,
#     `partial_update()`, `destroy()` and `list()` actions.
#     """
#     pass