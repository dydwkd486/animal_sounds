from django import forms
from .models import Animal_map,Animal_Sub_file,UploadFileModel
from betterforms.multiform import MultiModelForm

class DateInput(forms.DateTimeInput):
    input_type = 'datetime'

class DateStep(forms.DateInput):
    type = 'text'

class Animal_mapForm(forms.ModelForm):
    class Meta:
        model = Animal_map
        #observed_date=forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M:%S.%z"])
        fields = ('title','animalclass', 'Latitude', 'Longitude','address', 'content','observed_date','soundfile','imagefile')
        widgets = {
            'observed_date': DateInput(),
            'animalclass': forms.Select,
        }
    def __init__(self, *args, **kwargs):
        super(Animal_mapForm, self).__init__(*args, **kwargs)
        self.fields['imagefile'].required = False
        self.fields['soundfile'].required = False
        self.fields['Latitude'].required = False
        self.fields['Longitude'].required = False

class Animal_Sub_fileForm(forms.ModelForm):
    class Meta:
        model = Animal_Sub_file
        fields = []


class AnimalmapFormMultiform(MultiModelForm):
    form_classes ={
        'animal_map':Animal_mapForm,
        'animal_Sub_file':Animal_Sub_fileForm,
    }

class Animal_classForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel
        fields = ('soundfile',)

    def __init__(self, *args, **kwargs):
        super(Animal_classForm, self).__init__(*args, **kwargs)
        self.fields['soundfile'].required = False

class UploadFileForm(forms.Form):
    file = forms.FileField()