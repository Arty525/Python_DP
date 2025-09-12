from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.db import transaction


class Command(BaseCommand):
    help = 'Создает группы пользователей с точными правами'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.create_limited_users_group()
            self.create_staff_users_group()
            self.stdout.write(
                self.style.SUCCESS('✅ Группы пользователей успешно созданы и настроены!')
            )

    def create_limited_users_group(self):
        group, created = Group.objects.get_or_create(name='Limited Users')
        group.permissions.clear()

        allowed_permissions = [
            ('restaurant', 'reservation', 'view_reservation'),
            ('restaurant', 'reservation', 'add_reservation'),
            ('restaurant', 'reservation', 'change_reservation'),
            ('restaurant', 'reservation', 'delete_reservation'),

            ('users', 'user', 'view_user'),
            ('users', 'user', 'change_user'),

            ('restaurant', 'feedback', 'add_feedback'),
        ]

        all_perms = []
        for app_label, model, codename in allowed_permissions:
            try:
                perm = Permission.objects.get(
                    content_type__app_label=app_label,
                    content_type__model=model,
                    codename=codename
                )
                all_perms.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'⚠️ Право не найдено: {app_label}.{codename}'))

        group.permissions.add(*all_perms)
        self.stdout.write(self.style.SUCCESS(f'✅ Limited Users: {len(all_perms)} прав'))

    def create_staff_users_group(self):
        group, created = Group.objects.get_or_create(name='Staff Users')
        group.permissions.clear()

        all_perms = Permission.objects.all()

        forbidden_permissions = [
            ('restaurant', 'feedback', 'delete_feedback'),
            ('users', 'user', 'delete_user'),
        ]

        filtered_perms = []
        for perm in all_perms:
            is_forbidden = any(
                perm.content_type.app_label == app_label and
                perm.content_type.model == model and
                perm.codename == codename
                for app_label, model, codename in forbidden_permissions
            )
            if not is_forbidden:
                filtered_perms.append(perm)

        group.permissions.add(*filtered_perms)

        total = len(filtered_perms)
        forbidden_count = all_perms.count() - total

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Staff Users: {total} прав\n'
                f'   • Исключено {forbidden_count} опасных прав'
            )
        )