#! /usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^car_index/$',views.test),
    url(r'^car_index/$', views.CarView.as_view(), name='car_index'),
    # url(r'^car_create/$', views.car_create, name='car_create'),
    url(r'^car_create_ajax/$', views.car_create_ajax, name='car_create_ajax'),
    url(r'^car_detail_ajax/$', views.car_detail_ajax, name='car_detail_ajax'),
    url(r'^get_car_info_ajax/$', views.get_car_info_ajax, name='get_car_info_ajax'),
    url(r'^car_search/$', views.CarSearchView.as_view(), name='car_search'),
    url(r'^static_car/$', views.static_car, name='static_car'),
    url(r'^car_by_year/$', views.car_by_year, name='car_by_year'),
    url(r'^car_by_month/$', views.car_by_month, name='car_by_month'),
    url(r'^car_by_day/$', views.car_by_day, name='car_by_day'),
    url(r'^car_by_year_detail/(?P<year>\d{4})/$', views.car_by_year_detail, name='car_by_year_detail'),
    url(r'^car_by_month_detail/(?P<year>\d{4})/(?P<month>\d{1,})/$', views.car_by_month_detail, name='car_by_month_detail'),
    url(r'^car_by_day_detail/(?P<year>\d{4})/(?P<month>\d{1,})/(?P<day>\d{1,})/$', views.car_by_day_detail, name='car_by_day_detail'),
    url(r'^static_car_month/(?P<year>\d{4})/(?P<month>\d{1,})/$', views.static_car_month, name='static_car_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,})/(?P<day>\d{1,})/(?P<name>[-\w]+)/$', views.car_detail, name="car_detail"),
    url(r'^driver/$', views.driver, name='driver'),
    url(r'^saler/$', views.saler, name='saler'),
    url(r'^driver_salary/(?P<name>\w+)/$', views.driver_salary, name='driver_salary'),
    url(r'^driver_salary_list/$', views.driver_salary_list, name='driver_salary_list'),
    url(r'^saler_salary/(?P<name>\w+)/$', views.saler_salary, name='saler_salary'),
    url(r'^saler_salary_list/$', views.saler_salary_list, name='saler_salary_list'),
    url(r'^ajax_by_year/$', views.ajax_by_year, name='ajax_by_year'),
]
