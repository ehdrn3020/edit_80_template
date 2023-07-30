from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter, app_settings
from allauth.account.utils import filter_users_by_username
from allauth.utils import (
    # build_absolute_uri,
    # email_address_exists,
    # generate_unique_username,
    get_user_model,
    # import_attribute,
)
from django.shortcuts import render, get_object_or_404
from accounts.models import User
from django import forms
import re


#Allauth Save_user Class Override 
class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
    
        social_app_name = sociallogin.account.provider.upper()
        print(social_app_name)
        if social_app_name == "GOOGLE":
            user = User.objects.get(pk=user.pk)
            user.social_login = "구글아이디"
            user.save()
        elif social_app_name == "FACEBOOK":
            user = User.objects.get(pk=user.pk)
            user.social_login = "페이스북아이디"
            user.save()
        elif social_app_name == "KAKAO":
            user = User.objects.get(pk=user.pk)
            user.social_login = "카카오아이디"
            print(user.username)
            user.save()
        elif social_app_name == "NAVER":
            user = User.objects.get(pk=user.pk)
            user.social_login = "네이버아이디"
            user.save()

class AccountAdapter(DefaultAccountAdapter):

    def clean_username(self, username, shallow=False):
        if not re.match("^[a-zA-Z0-9가-힣_]*$", username):
            raise forms.ValidationError(
                "닉네임에 특수문자는 불가합니다.")

        for validator in app_settings.USERNAME_VALIDATORS:
            validator(username)

        # TODO: Add regexp support to USERNAME_BLACKLIST
        username_blacklist_lower = [ub.lower()
                                    for ub in app_settings.USERNAME_BLACKLIST]
        if username.lower() in username_blacklist_lower:
            raise forms.ValidationError(
                self.error_messages['username_blacklisted'])
        # Skipping database lookups when shallow is True, needed for unique
        # username generation.
        if not shallow:
            if filter_users_by_username(username).exists():
                user_model = get_user_model()
                username_field = app_settings.USER_MODEL_USERNAME_FIELD
                error_message = user_model._meta.get_field(
                    username_field).error_messages.get('unique')
                if not error_message:
                    error_message = self.error_messages['username_taken']
                raise forms.ValidationError(
                    error_message,
                    params={
                        'model_name': user_model.__name__,
                        'field_label': username_field,
                    }
                )
        return username
