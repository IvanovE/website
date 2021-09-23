from django.urls import path

from . import views

urlpatterns = [
    path('', views.StartingPageView.as_view(), name='starting-page'),
    path('posts', views.PostsView.as_view(), name='posts-page'),
    path('posts/<slug:slug>', views.PostDetailView.as_view(), name='post-detail-page'),
    path('read-later', views.ReadLaterView.as_view(), name='read-later-page'),
    path('login', views.loginPage, name='login'),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('categories/', views.CategoriesView.as_view(), name='categories-page'),
    path('categories/<slug:slug>', views.CategoryView.as_view(), name='category-page'),
    path('search/', views.SearchResultsView.as_view(), name='search-results')
]
