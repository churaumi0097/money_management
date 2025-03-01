from django.urls import path
from . import views


urlpatterns = [
    path("",views.Home.as_view(),name = "home"),
    path("list",views.List.as_view(),name = "list"),
    path("detail/<int:pk>",views.Detail.as_view(),name = "detail"),
    path("create",views.Create.as_view(),name = "create"),
    path("update/<int:pk>",views.Update.as_view(),name = "update"),
    path("delete/<int:pk>",views.Delete.as_view(),name = "delete"),
    path("cate_create",views.Cate_Create.as_view(),name = "cate_create"),
    path("predict",views.Predict.as_view(),name = "predict"),
]