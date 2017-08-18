from django import forms

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
    
    class Meta:
        model = ContactSubmission
        fields = '__all__'
        widgets = {
          'enquiry': forms.Textarea(attrs={'rows':5, 'cols':40}),
        }

