from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
    TokenBlacklistView
)
from .views import( 
    PostListCreateAPIView, 
    BoardCreateAPIView, BoardDetailAPIView, BoardListAPIView, BoardDeleteAPIView, BoardUpdateAPIView, BoardListCreateAPIView, BoardAPIView,
    TopicListCreateAPIView, 
    BoardDetailAPIView, TopicDetailAPIView,
    PostDetailAPIView
)

'''
router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'posts', PostViewSet, basename='post')
'''
urlpatterns = [
  #  path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/boards/<int:pk>/', BoardAPIView.as_view(), name='boards'),
    path('api/boards/create/', BoardCreateAPIView.as_view(), name='board-create'),
    path('api/boards/list-create/', BoardListCreateAPIView.as_view(), name='board-list-create'),
  # path('api/boards/<int:pk>/', BoardDetailAPIView.as_view(), name='board-details'),
    path('api/boards/<int:pk>/update/', BoardUpdateAPIView.as_view(), name='board-update'),
    path('api/boards/list/', BoardListAPIView.as_view(), name='board-list'),
    path('api/boards/<int:pk>/delete/', BoardDeleteAPIView.as_view(), name='board-delete'),
    path('api/boards/<int:board_id>/topics/', TopicListCreateAPIView.as_view(), name='board-topics'),
    path('api/topics/<int:topic_id>/posts/', PostListCreateAPIView.as_view(), name='topic-posts'),
  #  path('api/boards/<int:pk>/', BoardDetailAPIView.as_view(), name='board-detail'),
    path('api/topics/<int:pk>/', TopicDetailAPIView.as_view(), name='topic-detail'),
    path('api/posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),  # logout

]

