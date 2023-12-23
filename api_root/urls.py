from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bcb-pix/v1/', include('api_rest.urls')),
]
