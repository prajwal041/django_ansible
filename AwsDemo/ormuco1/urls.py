"""ormuco1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from AwsDemo.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import ansviews,logout

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', ansviews, name='ansviews'),
    url(r'^logout/', logout, name='logout'),
    url(r'^home/', ansviews, name='ansviews')
]
