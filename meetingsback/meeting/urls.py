"""meetings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from meeting import views
from .views import resolve_stockholder
from . import pdfmaker

urlpatterns = [
    path('meetings/', views.MeetingList.as_view()),
    path('meetings/<int:pk>/', views.MeetingDetail.as_view()),
    path('members/', views.MembershipList.as_view()),
    path('members/<int:pk>/', views.MembershipDetail.as_view()),
    path('employees/', views.EmployeeList.as_view()),
    path('proceedings/', views.ProceedingList.as_view()),
    path('proceedings/<int:pk>/', views.ProceedingDetail.as_view()),
    path('participants/', views.ParticipantList.as_view()),
    path('participants/<int:pk>/', views.ParticipantDetail.as_view()),
    path('resolutions/', views.ResolutionList.as_view()),
    path('resolutions/<int:pk>/', views.ResolutionDetail.as_view()),
    path('resolutiontypes/', views.ResolutionTypeList.as_view()),
    path('searchres/', views.SearchRes.as_view()),
    path('resstockholder/', resolve_stockholder),
    path('printproc/<int:pk>/', pdfmaker.PDFMaker.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('profile/', views.StockholderDetail.as_view()),
    path('procupload/<int:proceeding>/', views.FileUploadView.as_view()),
    path('downloadproc/<str:foldername>/<str:filename>/', views.download_file),
]
