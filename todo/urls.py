from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/',index,name='ind'),
    path('management/',manage,name='manage'),
    path('',loginmanager,name='login'),
    path('register/',addemp,name='add'),
    path('management/prev/',prev,name='prev'),
    path('report/',report,name='rep'),
    path('listemp/',listemp,name='list'),
    path('delete/<id>',delb,name="delb"),
    path('editemployee/<str:pk>/',edit, name='edit'),
    path('download/<filename>',download_file,name='download_file'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
