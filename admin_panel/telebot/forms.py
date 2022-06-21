from django import forms


class AddForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': "Введите ..."}),
                              label="Текст сообщения для рассылки:")
