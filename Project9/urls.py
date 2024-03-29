"""Project9 URL Configuration

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
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from litreview import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login/", LoginView.as_view(template_name="litreview/login.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("review/create/", views.create_review, name="create_review"),
    path("review/<int:review_id>/edit/", views.edit_review, name="edit_review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    # path('review/', views.reviews, name='reviews'),
    path("ticket/create/", views.create_ticket, name="create_ticket"),
    path("ticket/<int:ticket_id>/edit/", views.edit_ticket, name="edit_ticket"),
    path("ticket/<int:ticket_id>/delete/", views.delete_ticket, name="delete_ticket"),
    # path('ticket/', views.tickets, name='tickets'),
    path("feed/", views.feed, name="feed"),
    path("", views.feed, name="root_feed"),
    path("posts/", views.posts, name="posts"),
    path("follow/", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
