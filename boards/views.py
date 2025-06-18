from .models import Board, Topic, Post
from .forms import BoardForm, NewTopicForm
from .serializers import BoardSerializer, TopicSerializer, PostSerializer
from .pagination import BoardPagination
from django.contrib.auth.models import User 
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import  BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ( ListAPIView, CreateAPIView, 
                                     RetrieveAPIView, DestroyAPIView, 
                                     UpdateAPIView, ListCreateAPIView, 
                                     RetrieveUpdateDestroyAPIView )
import json


def home(request):
    try:
        boards = Board.objects.all()
        return render(request, 'home.html', {'boards': boards})
    except Exception as e:
        from django.http import HttpResponse
        return HttpResponse(f"❌ Error: {str(e)}")

    


def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('board_success')
    else:
        form = BoardForm()
    return render(request, 'create_board.html', {'form': form})

def board_success(request):
    return render(request, 'success.html')

def new_topic(request, board_id):

    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board

            user = User.objects.first() 
            topic.starter = user
            topic.save()

            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )

            return redirect('topic_success', board_id=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_success(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    topics = board.topics.all()
    return render(request, 'topic_success.html', {'board':board, 'topics':topics})

def list_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    query = request.GET.get('q', '')
    if query:
        topics = board.topics.filter(subject__icontains=query).prefetch_related('posts')
    else:
        topics = board.topics.all().prefetch_related('posts')

    return render(request, 'list_topics.html', {
        'board': board, 
        'topics': topics,
        'query': query
        })

@csrf_exempt
def update_vote(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            try:
                topic_id = int(data.get('topic_id'))
            except (TypeError, ValueError):
                return JsonResponse({'success': False, 'error': 'Invalid topic ID'})
           
            action = data.get('action')
            topic = Topic.objects.get(pk=topic_id)
            
            if not hasattr(topic, 'vote_count'):
                topic.vote_count = 0

            if action == 'upvote':
                topic.vote_count +=1
            elif action == 'downvote':
                topic.vote_count -=1
            topic.save()
            return JsonResponse({'success': True, 'new_count': topic.vote_count})
        except Topic.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Topic not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid Request'})

'''
class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = BoardPagination

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
'''

class BoardCreateAPIView(CreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]


class BoardListCreateAPIView(ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = BoardPagination()


class BoardDetailAPIView(RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]


class BoardUpdateAPIView(UpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]

class BoardDeleteAPIView(DestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]


class BoardListAPIView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = BoardPagination()

class BoardAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = BoardPagination()

   
'''        
class BoardDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get_object(self, pk):
        return get_object_or_404(Board, pk=pk)
    
    def patch(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        board = self.get_object(pk)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''


class TopicListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, board_id):
        topics = Topic.objects.filter(board_id=board_id)
        serializer = TopicSerializer(topics, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, board_id):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(board_id=board_id, starter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopicDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    
    def get_object(self, pk):
        return get_object_or_404(Topic, pk=pk)
    
    def patch(self, request, pk):
        topic = self.get_object(pk)
        serializer = TopicSerializer(topic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        topic = self.get_object(pk)
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostListCreateAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, topic_id):
        posts = Post.objects.filter(topic_id=topic_id)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, topic_id):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(topic_id=topic_id, created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get_object(self, pk):
        return get_object_or_404(Topic, pk=pk)
    
    def patch(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  