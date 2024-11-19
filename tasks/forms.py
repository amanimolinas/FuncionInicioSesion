from django import forms 


class TaskCreationForm(forms.Form): 
    title = forms.CharField(label='Titulo', max_length=255)
    Content= forms.CharField(label='Contenido', widget=forms.Textarea())