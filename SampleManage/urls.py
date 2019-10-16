from django.urls import path
from . import views

app_name = 'SampleManage'
urlpatterns = [
     path('', views.index, name='index'),
     path('upload',views.upload,name='upload'),
     path('resultechart',views.resultechart,name = 'resultechart'),
     path('testform',views.testform,name='testform'),
     path('visualizees', views.visualizees, name='visualizees'),
     path('detectes',views.detectes,name='detectes'),
     path('predictes',views.predictes,name='predictes'),
     path('<path:pathtest>/retages',views.retages,name='retages'),
     path('train',views.train,name='train'),
     path('mulvisualize',views.mulvisualize,name='mulvisualize'),
     path('testform',views.testform,name='testform'),
     path('comparees',views.comparees,name='comparees')
]