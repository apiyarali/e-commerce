from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new",views.create_listing, name="create_listing"),
    path("category", views.category, name="category"),
    path("category/<int:category_id>", views.categorylist, name="categorylist"),
    path("list/<int:list_id>", views.listing, name="list"),
    path("list/<int:list_id>/comment", views.listcomment, name="listcomment"),
    path("list/<int:list_id>/bid", views.bid, name="bid"),
    path("watchlist", views.watchlist_view, name="watchlist_view"),
    path("watchlist/<int:list_id>", views.watchlist_add, name="watchlist_add")
]
