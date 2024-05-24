from django.urls import path
from . import views

urlpatterns = [
    path("extract-text/", views.extract_text, name="extract_text"),
    path("replace-text/", views.replace_text, name="replace_text"),
    path("count-tags/", views.count_tags, name="count_tags"),
    path("validate-html/", views.validate_html, name="validate_html"),
]
