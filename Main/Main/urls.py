"""
URL configuration for Main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import accounts.urls as u
import home.urls as q
from django.urls import include, path
from Main.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='AlgoAlpha'),
    path('admin/', admin.site.urls),
    path('accounts/',include(u)),
    path('home/',include(q)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
