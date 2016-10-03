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
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^kabinet/$', views.UserView().kabinet),
    url(r'^login/$', views.UserView().login),
    url(r'^logout/$', views.UserView().logout),
    url(r'^contacts/$', views.ContactView.as_view()),
    url(r'^register/$', views.UserView.register),
    url(r'^pass_change/$', views.UserEditView().password_change),
    url(r'^delete_acc/$', views.UserEditView().delete_user),
    url(r'^new_avatar/$', views.AvatarView().new_avatar),
    url(r'^change_avatar/$', views.AvatarView().change_avatar),
    url(r'^delete_avatar/$', views.AvatarView().delete_avatar),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^vk_login/$', RedirectView.as_view(url=settings.VK_REDIRECT)),
    url(r'^vk_callback/', views.vk_callback),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
