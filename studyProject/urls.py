from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',include("studyroom.urls")),
    path('admin/', admin.site.urls),
    path('api/', include("studyroom.api.urls"))
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
        #go to this              URL         and get             this FILE 