from django.urls import path

from .import views

app_name='crop_detector'
urlpatterns=[
    path('',views.index,name="index"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('logout/',views.logoutUser,name="logout"),
    path('delete_image/<str:pk>/', views.delete_image, name="delete_image"),
    path('download/',views.download,name="download"),
]
