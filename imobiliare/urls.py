from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    # path('login/', views.loginPage, name='login'),
    path('login/', LoginPage.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    # path('admin/', views.adminPage, name='admin'),

    path('announce_details/<int:id>/', AnnounceDetails.as_view(), name='announce_details'),
    path('my_announces/', MyAnnounces.as_view(), name='my_announces'),
    path('create_announce/', CreateAnnounce.as_view(), name='create_announce'),
    path('update_announce/<int:id>/', UpdateAnnounce.as_view(), name='update_announce'),
    path('delete_announce/<int:id>/', DeleteAnnounce.as_view(), name='delete_announce'),
    path('search', SearchAnnounce.as_view(), name='search_announce'),
    path('calculator/', Calculator.as_view(), name='calculator')
]