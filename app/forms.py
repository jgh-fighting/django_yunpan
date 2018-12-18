from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator





class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50,required=True,validators=[MaxLengthValidator(limit_value=10),MinLengthValidator(limit_value=5,message='用户名在5-10个字符之间')])
    password = forms.CharField(label='密码',max_length=100,required=True,validators=[MaxLengthValidator(limit_value=10),MinLengthValidator(limit_value=5,message='用户名在5-10个字符之间')],widget=forms.PasswordInput)
    confirm = forms.CharField(label='确认密码',max_length=100,required=True,validators=[MaxLengthValidator(limit_value=10),MinLengthValidator(limit_value=5,message='用户名在5-10个字符之间')],widget=forms.PasswordInput)
    email = forms.EmailField(validators=[EmailValidator(message='请输入正确的邮箱')])

    def validate_username(self):
        pass

    def clean(self):
        pws1 = self.cleaned_data.get('password')
        pws2 = self.cleaned_data.get('confirm')
        if pws1 != pws2:
            raise ValidationError('两次密码输入不一致！')


class Login(forms.Form):
    username = forms.CharField(label='用户名',max_length=50,required=True,)
    password = forms.CharField(label='密码',max_length=100,required=True,widget=forms.PasswordInput)



class personInfo(forms.Form):
    username = forms.CharField(label='用户名',disabled=True)
    email = forms.CharField(label='邮箱',disabled=True)


class changePassword(forms.Form):
    password = forms.CharField(label='新密码', max_length=100, required=True,
                               validators=[MaxLengthValidator(limit_value=10),
                                           MinLengthValidator(limit_value=5, message='密码在5-10个字符之间'),],
                               widget=forms.PasswordInput,help_text='密码在5-10个字符之间')
    confirm = forms.CharField(label='确认密码', max_length=100, required=True,
                              validators=[MaxLengthValidator(limit_value=10),
                                          MinLengthValidator(limit_value=5, message='密码在5-10个字符之间')],
                              widget=forms.PasswordInput,help_text='密码在5-10个字符之间')

    def validate_username(self):
        pass
    def clean(self):
        pws1 = self.cleaned_data.get('password')
        pws2 = self.cleaned_data.get('confirm')
        if pws1 != pws2:
            raise ValidationError('两次密码输入不一致！')

class activateUser(forms.Form):
    username = forms.CharField(label='用户名', max_length=50, required=True,
                               validators=[MaxLengthValidator(limit_value=10),
                                           MinLengthValidator(limit_value=5, message='用户名在5-10个字符之间')])
    password = forms.CharField(label='密码', max_length=100, required=True,
                               validators=[MaxLengthValidator(limit_value=10),
                                           MinLengthValidator(limit_value=5, message='用户名在5-10个字符之间')],
                               widget=forms.PasswordInput)
    email = forms.EmailField(validators=[EmailValidator(message='请输入正确的邮箱')])

class Change_head(forms.Form):

    file = forms.FileField(label='新头像')