from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main_menu.urls', 'main_menu'), namespace='main_menu')),
    path('accounts/', include(('accounts.urls','accounts'),namespace='accounts')),
]