from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('bibliography', views.bibliography, name="bibliography"),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('events/', include('events.urls')),
    path('statute', views.statute, name="statute"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
