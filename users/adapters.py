from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user = super().save_user(request, user, form, False)

        name = data.get("name")
        is_korean = data.get("is_korean")

        if name:
            user.name = name
        if is_korean:
            user.is_korean = is_korean

        user.save()

        return user

    # email verification redirected to the frontend part
    # 해당 url을 프론트엔드로 보내면 프론트는 url의 key를 받아서 백엔드에 'post' 메소드로 보내야 함
    def get_email_confirmation_url(self, request, emailconfirmation):
        return settings.URL_FRONT + "verify/email?code=" + emailconfirmation.key
