from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main_menu.urls', 'main_menu'), namespace='main_menu')),
]
