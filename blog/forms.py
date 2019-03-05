from django import forms
from .models import Animal_map

class DateInput(forms.DateInput):
    input_type = 'datetime_local'

class DateStep(forms.DateInput):
    type = 'text'

class Dateimgfile(forms.FileInput):
    accept='.gif, .jpg, .png'

class Datesoundfile(forms.FileInput):
    accept='.mp3,.wav'


class Animal_mapForm(forms.ModelForm):

    class Meta:
        model = Animal_map
        fields = ('title', 'Latitude', 'Longitude', 'content','observed_date','soundfile','file')
        widgets = {
            'observed_date': DateInput(),
            'Latitude':DateStep(),
            'Longitude':DateStep(),            
        }

    def __init__(self, *args, **kwargs):
        super(Animal_mapForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False
        self.fields['soundfile'].required = False

