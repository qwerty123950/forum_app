from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from boards import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/table/', views.home_table, name='home_table'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'), 
    path('boards/create/', views.create_board, name='create_board'),
    path('boards/<int:board_id>/delete/', views.delete_board, name='delete_board'),
    path('success/', views.board_success, name='board_success'),
    path('boards/<int:board_id>/new/', views.new_topic, name='new_topic'),
    path('boards/<int:board_id>/', views.list_topics, name='list_topics'),
    path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('boards/vote/', views.update_vote, name='update_vote'),
    path('boards/<int:board_id>/new/success', views.topic_success, name='topic_success'),
    path('api-auth/', include('rest_framework.urls')),
    path('forum/', include('boards.urls')),
]
