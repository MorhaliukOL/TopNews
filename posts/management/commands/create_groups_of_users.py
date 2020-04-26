from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from posts.models import Post


class Command(BaseCommand):
    help = 'Create groups for users'

    def handle(self, *args, **kwargs):
        """
        Create user groups: users, redactors and admins.
        Create permission "Can approve posts for publication".
        Give created permission to redactors and admins.
        """
        users_group, _ = Group.objects.get_or_create(name='users')
        redactors_group, _ = Group.objects.get_or_create(name='redactors')
        admins_group, _ = Group.objects.get_or_create(name='admins')

        ct = ContentType.objects.get_for_model(Post)

        approve_posts_permission, _ = Permission.objects.get_or_create(
            codename='approve_posts',
            name='Can approve posts for publication',
            content_type=ct
        )

        redactors_group.permissions.add(approve_posts_permission)
        admins_group.permissions.add(approve_posts_permission)
        self.stdout.write('users, redactors and admins groups created successfully')
