from rest_framework.routers import APIRootView, DefaultRouter

from core.rest import GenerateTemplates, RetrieveTemplates


class AllAPIRootView(APIRootView):
    permission_classes = [ ]

class AllDefaultRouter(DefaultRouter):
    APIRootView = AllAPIRootView


router = AllDefaultRouter()
router.register(r'topic-submit', GenerateTemplates, basename='topic-submit')
router.register(r'slides', RetrieveTemplates)



