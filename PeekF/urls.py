"""PeekPeek URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# from django.urls import path

# from PeekF.views import index
from django.contrib import admin
from django.conf.urls import url

from django.urls import include, path
from . import views

urlpatterns = [
    # path('app1/', include('PeekVAr.urls')),
    # path('admin/', admin.site.urls),
    path('test1/', views.test, name='index'),
    path('tryboot/', views.tryboot),

    path('test2/',views.showlinediagram),
    path('test2/index.html', views.showlinediagram2),

    path('index/', views.tab_home),
    path('nav/nav_conf', views.tab_Conf),
    path('nav/nav_monitor', views.tab_Monitor),
    path('nav/nav_monitor_deal', views.tab_Monitor_deal,name='nav_monitor_deal'),


    path('nav/nav_compare', views.tab_Compare),
    path('nav/nav_compare_deal', views.tab_Compare_deal, name='nav_monitor_deal'),

    path('nav/nav_vis', views.tab_Vis),
    path('nav/nav_vis_anay', views.tab_Vis2)

]
