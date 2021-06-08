from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  .views import post_views,user_views



#from authentication.urls import *
#router = DefaultRouter()
#router.register('posts', views.PostViewSet)
#router.register('register', Register)



urlpatterns = [
    path('posts/', post_views.post_list),
    path('posts/<slug:slug>/', post_views.post_detail),
    #path('api/', include(router.urls)),
    path('user/<str:user_name>/', user_views.user_details),
]

