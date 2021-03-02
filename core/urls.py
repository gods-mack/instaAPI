from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  . import views
#from authentication.urls import *
router = DefaultRouter()
router.register('posts', views.PostViewSet)
#router.register('register', Register)



urlpatterns = [
    path('posts/', views.post_list),
    path('posts/<slug:slug>/', views.post_detail),
    path('api/', include(router.urls))
]
