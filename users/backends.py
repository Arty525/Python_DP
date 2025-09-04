from django.contrib.auth.backends import ModelBackend


class LimitedPermissionsBackend(ModelBackend):
    def has_perm(self, user_obj, perm, obj=None):
        # Базовая проверка
        has_perm = super().has_perm(user_obj, perm, obj)

        # Дополнительные проверки для ограниченных пользователей
        if perm == 'blog.change_reservation' and obj:
            return obj.user == user_obj

        return has_perm
