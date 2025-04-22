from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('donate/', views.donate, name='donate'),
    path('reciever/', views.reciever, name='reciever'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('navbar/', views.navbar, name='navbar'),
    path('join/', views.join, name='join'),
    path('contact/', views.contact, name='contact'),
    path('footer/', views.footer, name='footer'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # This is the important one
    path('logout/', views.custom_logout, name='logout'),
] 