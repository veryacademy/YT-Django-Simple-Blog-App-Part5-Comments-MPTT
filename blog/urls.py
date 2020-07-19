from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('<slug:post>/', views.post_single, name='post_single'),
    path('category/<category>/', views.CatListView.as_view(), name='category'),
]
