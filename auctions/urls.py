from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name='listing'),
    path("add_bid/<int:listing_id>", views.add_bid, name='add_bid'),
    path("edit_watchlist/<int:listing_id>", views.edit_watchlist, name='edit_watchlist'),
    path("close_auction/<int:listing_id>", views.close_auction, name='close_auction'),
    path("add_comment/<int:listing_id>", views.add_comment, name='add_comment'),
    path("watchlist", views.watchlist, name='watchlist'),
    path("categories", views.categories, name='categories'),
    path("<str:category>", views.show_category, name='show_category')
]

