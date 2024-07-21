from django.urls import path

from . import views

urlpatterns = [
    path('employees/list/', views.EmployeesListAPIView.as_view(), name='employees'),
    path('registered-qr-codes/list/', views.RegisteredQRCodesListAPIView.as_view(), name='registered_qr_codes'),
    path('winners/list/', views.WinnersListAPIView.as_view(), name='winners'),
    path('winner/create/', views.CreateWinnerAPIView.as_view(), name='create_winner'),
]
