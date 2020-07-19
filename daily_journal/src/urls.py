from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('journal/', include('journal.urls')),
    path('admin/', admin.site.urls),
]
