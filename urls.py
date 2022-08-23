
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todos/', include('todos.urls')),
    #endpoint to generate the auth token 
    path('auth/', obtain_auth_token),
]
