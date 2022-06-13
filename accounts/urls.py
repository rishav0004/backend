from django.urls import path
from . import views

urlpatterns = [
    # path('managers',views.ManagerView.as_view()),
    path('profile/',views.UserProfileView.as_view()),
    path('login/',views.UserLoginView.as_view(),name='login' ),
    path('users/',views.AllUsersView.as_view(),name='users'),
    path('users/<int:pk>',views.AllUsersView.as_view(),name='users'),
    path('vehicles/',views.AllVehicles.as_view(),name='vehicles'),
    path('vehicles/<int:pk>',views.AllVehicles.as_view(),name='vehicles'),
    path('drivers/',views.AllDrivers.as_view(),name='drivers'),
    path('drivers/<int:pk>',views.AllDrivers.as_view(),name='drivers'),
    path('drivers/update/<int:pk>',views.UpdateDriverView.as_view(),name='drivers'),
    path('drivers/delete/<int:pk>',views.DeleteDriverView.as_view(),name='drivers'),
    path('alldrivers/',views.AllUserDriver.as_view(),name='drivers'),
    path('alldrivers/<int:pk>',views.AllUserDriver.as_view(),name='drivers'),
    path('managers/',views.AllManagers.as_view(),name='managers'),
    path('managers/<int:pk>',views.AllManagers.as_view(),name='managers'),
    path('managers/update/<int:pk>',views.UpdateManagerView.as_view(),name='update-managers'),
    path('vehicle/update/<int:pk>',views.UpdateVehicleView.as_view(),name='update-vehicle'),
    path('vehicle/delete/<int:pk>',views.DeleteVehicleView.as_view(),name='delete-vehicle'),
    path('update/<int:pk>',views.UpdateProfileView.as_view(),name='update'),
    path('delete/<int:pk>',views.DeleteProfileView.as_view(),name='delete'),
    path('changepassword/',views.UserChangePassword.as_view(),name='changepassword'),
    path('head/register/',views.HeadSignupView.as_view()),
    path('vehicle/register/',views.VehicleSignupView.as_view()),
    path('driver/register/',views.DriverSignupView.as_view()),
    path('manager/register/',views.ManagerSignupView.as_view()),
    path('send-reset-password-email/',views.SendPasswordResetEmailView.as_view(),name='send-rest-password-email'),
    path('reset-password/<uid>/<token>/',views.UserPasswordResetView.as_view(),name='rest-password'),
    path('driveradd/',views.newDriver.as_view())
    
]