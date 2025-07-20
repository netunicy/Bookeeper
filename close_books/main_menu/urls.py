from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main_menu'

urlpatterns = [
    path('', views.main_menu, name='main_menu'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
