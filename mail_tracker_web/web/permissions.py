from django.contrib.auth.mixins import UserPassesTestMixin


class BaseUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return True


class AnonymousRequiredPermission(BaseUserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated and super().test_func()
