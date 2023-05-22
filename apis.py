from django.urls import path

from .views import AutocompletedViewView, SearchViewView

urlpatterns = [
    path('search/', SearchViewView.as_view()),
    path('autocomplete/', AutocompletedViewView.as_view()),
]

