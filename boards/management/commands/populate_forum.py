# yourapp/management/commands/populate_forum.py

from django.core.management.base import BaseCommand
from boards.factories import BoardFactory, TopicFactory, PostFactory, UserFactory
from django.db import transaction
from boards.models import Topic
import random

class Command(BaseCommand):
    help = 'Populate the database with sample forum data'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.stdout.write("Creating Users...")
            users = UserFactory.create_batch(100)

            self.stdout.write("Creating Boards...")
            boards = BoardFactory.create_batch(25)

            self.stdout.write("Creating Topics...")
            topics = []
            for _ in range(100):
                topic = TopicFactory(
                    board=random.choice(boards),
                    starter=random.choice(users)
                )
                topics.append(topic)

            self.stdout.write("Creating Posts...")
            post_count = 0
            for topic in topics:
                for _ in range(random.randint(1, 5)):
                    PostFactory(
                        topic=topic,
                        created_by=random.choice(users),
                        updated_by=random.choice(users)
                    )
                    post_count += 1

            self.stdout.write(self.style.SUCCESS(f"✔ Created {len(users)} users, {len(boards)} boards, {len(topics)} topics, {post_count} posts."))
