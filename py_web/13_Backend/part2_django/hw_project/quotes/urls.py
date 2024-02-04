from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="main"),
    path("<int:page>", views.main, name="root_paginate"),
    path("author/<str:author_id>", views.show_author_info, name="author"),
    path("add-author/", views.add_author, name="add-author"),
    path("add-quote/", views.add_quote, name="add-quote"),
]
