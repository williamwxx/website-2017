from django.conf.urls import url,include
from django.contrib import admin
from opstools.views import index,tables,status,login
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^index.html',index,name='index'),
    url(r'^tables.html',tables,name='tables'),
    url(r'^status.html',status,name='status'),
    url(r'^login.html',login,name='login'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)