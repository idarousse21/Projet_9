"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView
import authentication.views
from review.views import (
    ViewFlux,
    CreateTicket,
    UpdateTicket,
    DeleteTicket,
    create_review,
    UpdateReview,
    DeleteReview,
    ViewPosts,
    Subscription,
    ViewSubscription,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        LoginView.as_view(template_name="authentication/login.html"),
        name="login",
    ),
    path("logout/", authentication.views.logout_user, name="logout"),
    path("flux/", ViewFlux.as_view(), name="flux"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("create-ticket/", CreateTicket.as_view(), name="create_ticket"),
    path(
        "update-ticket/<pk>/",
        UpdateTicket.as_view(),
        name="update-ticket",
    ),
    path("delete-ticket/<int:pk>/", DeleteTicket.as_view(), name="delete-ticket"),
    path("create-review/", create_review, name="create_review"),
    path(
        "update-review/<pk>/",
        UpdateReview.as_view(),
        name="update-review",
    ),
    path("delete-review/<pk>/", DeleteReview.as_view(), name="delete-review"),
    path("posts/", ViewPosts.as_view(), name="posts"),
    path("subscription/", Subscription.as_view(), name="subscription"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
