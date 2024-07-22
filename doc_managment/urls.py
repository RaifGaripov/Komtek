from django.urls import path

from .views import RefBookListView, RefBookElementsView, RefBookElementCheckView

urlpatterns = [
    path('refbooks/', RefBookListView.as_view(), name='refbook-list'),
    path('refbooks/<int:id>/elements', RefBookElementsView.as_view(), name='refbook-elements'),
    path('refbooks/<int:id>/check_element', RefBookElementCheckView.as_view(), name='refbook-check-element'),
]
