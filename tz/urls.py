"""tz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from tz import views, settings
from django.conf.urls.static import static


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^kabinet/$', views.kabinet),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^contacts/$', views.contact),
    url(r'^register/$', views.register),
    url(r'^pass_change/$', views.password_change),
    url(r'^delete_acc/$', views.delete_user),
    url(r'^new_avatar/$', views.new_avatar),
    url(r'^change_avatar/$', views.change_avatar),
    url(r'^delete_avatar/$', views.delete_avatar),
    url(r'^captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
