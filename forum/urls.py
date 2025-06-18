from django.contrib import admin
from django.urls import path,include
from boards import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('boards/create/', views.create_board, name='create_board'),
    path('success/', views.board_success, name='board_success'),
    path('boards/<int:board_id>/new/', views.new_topic, name='new_topic'),
    path('boards/<int:board_id>/', views.list_topics, name='list_topics'),
    path('boards/vote/', views.update_vote, name='update_vote'),
    path('boards/<int:board_id>/new/success', views.topic_success, name='topic_success'),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('boards.urls')),
]
