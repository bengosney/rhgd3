# Django

# Django
from django.urls import path

# Locals
from . import views

app_name = "banner_messages"
urlpatterns = [
    path("dismiss/<slug:slug>", views.dismiss, name="dismiss"),
]
