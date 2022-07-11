"""cerr_curate_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, reverse_lazy
from django.conf.urls import include


from django.contrib import admin

from .views.user import draft
from .views.user import ajax as user_ajax

urlpatterns = [
    re_path(r"^add-role", user_ajax.role_form, name="ajax_get_role"),
    re_path(r"^$", draft.start, name="core_curate_index"),
    re_path(r"^start_curate/edit/(?P<draft_id>\w+)$", draft.EditView.as_view(), name="edit"),

]
