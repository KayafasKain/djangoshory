from django import forms
from .models import Link
from .utils import check_url_util as ch_url

class CreateLinkModelForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['basic_link']
        labels = {'here goes link, you want to get shorter'}
        help_texts = {'pass your link here and press "submit" button'}
        error_messages = {
            'basic_link': {
                'required': 'please, don`t leave field blank',
                'invalid_url': 'please, provide us with valid URL'
            }
        }

    def clean(self):
        if not ch_url.is_valid_url(self.data['basic_link']):
            raise forms.ValidationError({
                'basic_link': self.Meta.error_messages['basic_link']['invalid_url']
            })
