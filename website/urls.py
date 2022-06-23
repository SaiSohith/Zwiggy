from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.loginuser, name='loginuser'),
    path('profile', views.profile, name="profile"),

    path('updateprofile', views.updateprofiledetails, name="updateprofile"),
    path('register', views.Register, name="Register"),
    path('aboutus', views.aboutus),
    path('foodview', views.foodrecommendations),
    # path('aboutus', views.aboutus),
    path('logout', views.logoutuser),
    path('upload', views.upload),
    path('contactus', views.contactus),
    path('foodcard', views.foodcard),
    path('samplechart', views.sample_charts),
    path('restdetails/<restid>', views.restaurant_details),
    path('searchrestaurant', views.findrestaurant),
    path('restdetails/booktable', views.restaurant_details, name="booktable"),
    path('restdetails/orderfood', views.restaurant_details, name="orderfood"),
    path('orderhistory', views.updatefoodorder, name='orderhistory'),

    path('updatebooktable/<restid>',
         views.tableupdatehandler, name="updatebooktable"),
    path('canceltablebooking', views.canceltablebooking, name='canceltablebooking'),
    path('cancelorderfood', views.cancelorderfood, name='cancelorderfood'),
    path('hotelview', views.gethotels, name='gethotels'),
    path('roombook', views.roombook, name='roombook'),




]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
