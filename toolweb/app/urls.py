from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('get/<str:id>/', AppContentView.as_view(), name="app"),
    path("get-apps/", AppListView.as_view(), name="get-apps"),
    path("app-list/", TemplateView.as_view(template_name="app/app_list.html"), name="apps"),
    path("create-app/", CreateAppView.as_view(), name="create-app"),
    path("info/<str:id>/", AppInfoView.as_view(), name="app-info"),
    path("change-html/", ChangeHtmlView.as_view(), name="change-html"),
    path("change-view/", ChangeView.as_view(), name="change-view"),
    path("get-my-apps/", GetUserAppsView.as_view(), name="get-my-apps"),
    path("pre-html/", PreHtmlView.as_view())

]
