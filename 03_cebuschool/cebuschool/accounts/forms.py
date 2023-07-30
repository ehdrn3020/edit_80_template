from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import User

class RegisterModelForm(forms.ModelForm):

    # password_frm = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'name':'register_pw_frm',
    #     'class':'join_pw_frm2', 
    #     'require': True
    # }))

    class Meta :
        model = User
        fields = ('email', 'username', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={
                'name':'register_id',
                'class':'join_login_frm',
                'value':'{{email}}',
                'required': True
            }),
            'username': forms.TextInput(attrs={
                'name':'username',
                'class':'join_login_frm',
                'value':'{{username}}',
                'required': True
            }),
            'password': forms.PasswordInput(attrs={
                'name':'register_pw',
                'class':'join_pw_frm',
                'required': True
            }),
        }


    # def clean_user(self):
    #     email = self.cleaned_data['email']
    #     errors = []

    #     if email == '':
    #         errors.append(forms.ValidationError('이메일을 입력해주세요.'))
    #     elif User.objects.filter(email=email).exists():
    #         errors.append(forms.ValidationError('이미 가입된 이메일입니다.'))
    #     if errors:
    #         raise forms.ValidationError(errors)
    #     return email

# [view.py]
# form = RegisterModelForm(request.POST)
        # print(form.is_valid())
        # if form.is_valid():
        #     user = form.save(commit=False)
        #     user.social_login="이메일아이디"
        #     user.save()
        #     return render(request, 'accounts/register_index.html')
        
        # else:
        #     return render(request, 'accounts/login.html')