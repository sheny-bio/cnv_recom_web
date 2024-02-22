"""cnv_recom_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('met', views.home_met, name='met'),
    path('analyze', views.analyze, name='analyze'),
    path('analyze_met', views.analyze_met, name='analyze_met'),
    path('upload', views.upload, name='upload'),
    path('upload_met_bai', views.upload_met_bai, name='upload_met_bai'),
    path('upload_met_bam', views.upload_met_bam, name='upload_met_bam'),
    path('upload_met_gene', views.upload_met_gene, name='upload_met_gene'),
    path('download_demo', views.download_demo, name='download_demo'),
    path('download_demo_met', views.download_demo, name='download_demo_met'),
]
