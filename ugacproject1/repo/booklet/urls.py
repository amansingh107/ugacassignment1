from django import views
from django.urls import path ,include
from booklet.views import LoginPageView, SignupPageView, BookletListView, BookletUploadView, BookletDeleteView
from django.contrib.auth import views as auth_views

from .views import CustomLogoutView

urlpatterns = [
    path('', LoginPageView.as_view(), name='login'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('booklets/', BookletListView.as_view(), name='booklet_list'),
    path('booklets/upload/', BookletUploadView.as_view(), name='booklet_upload'),
    path('booklets/delete/<int:pk>/', BookletDeleteView.as_view(), name='booklet_delete'),
     path('booklets/download/<int:pk>/', views.download_booklet, name='download_booklet'),
    path('booklets/view/<int:pk>/', views.ViewBookletView.as_view(), name='view_booklet'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

