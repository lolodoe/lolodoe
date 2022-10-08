from django.contrib import admin
from django.urls import path
from django.views.generic import edit

import users
from posts.views import MainView, PostDetailView, CreatePostView,edit
from django.conf import settings
from django.conf.urls.static import static
from users.views import register_view, login_view, logout_view, set_password, personal_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('posts/<pk>/detail/', PostDetailView.as_view()),
    path('posts/create/', CreatePostView.as_view()),
    path('users/register/', register_view),
    path('users/login/', login_view),
    path('users/logout/', logout_view),
    path('posts/<int:id>/edit/', edit),
    path('users/<int:id>/change_password/', set_password),
    path('personal/', personal_info),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






