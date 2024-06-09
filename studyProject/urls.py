from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include("studyroom.urls")),
    path('admin/', admin.site.urls),
]
