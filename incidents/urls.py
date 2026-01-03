from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path


app_name = 'incidents'

router = DefaultRouter() 
router.register('incident', views.IncidentViewSet, basename='incident')

urlpatterns = router.urls

urlpatterns += [
    path('incident/choices/', views.ChoicesView.as_view(), name='choices'),
]