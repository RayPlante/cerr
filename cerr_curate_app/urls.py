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
from django.urls import include, path
from django.conf.urls import include

from django.contrib import admin

from .views.user import draft
from .views.user import ajax as user_ajax

app_name = "start_curate"

urlpatterns = [
    path("enter-data/ajax/ajax_get_role/", user_ajax.role_form, name="ajax_get_role"),
    path("enter-data/<str:draft_id>", draft.EditView.as_view(), name="edit"),
    path("", draft.start, name="start"),
]
