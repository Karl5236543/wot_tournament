from django import forms

class ReplayForm(forms.Form):
    replay = forms.ImageField(
        widget=forms.widgets.ClearableFileInput(attrs={'multiple': True}),
        label='Выберите файл'
    )  