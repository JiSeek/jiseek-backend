from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        users = User.objects.all()
        user = super().save_user(request, user, form, False)
        # 추가 저장 필드: profile_image
        name = data.get("name")
        is_korean = data.get("is_korean")
        if name:
            user.name = name
        if is_korean:
            user.is_korean = is_korean

        user.save()
        return user
