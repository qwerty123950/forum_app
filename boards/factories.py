import factory
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from faker import Faker

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')

class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    name = factory.Sequence(lambda n: f'Board-{n}')
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=6))

class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    subject = factory.LazyAttribute(lambda _: fake.sentence(nb_words=4))
    board = factory.SubFactory(BoardFactory)
    starter = factory.SubFactory(UserFactory)
    vote_count = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=100))

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    message = factory.LazyAttribute(lambda _: fake.paragraph(nb_sentences=3))
    topic = factory.SubFactory(TopicFactory)
    created_by = factory.SubFactory(UserFactory)
    updated_by = None
