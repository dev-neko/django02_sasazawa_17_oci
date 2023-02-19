from django import forms

class ScrapingForm(forms.Form):
    occupation = forms.CharField(max_length=255, widget=forms.Textarea)
    count = forms.IntegerField()

class SiteForm(forms.Form):
    site = forms.fields.ChoiceField(
        choices = (
            ('green', 'Green'),
            ('recnavi', 'リクナビ'),
            ('geekly', 'ギークリー')
        ),
        required=True,
        widget=forms.widgets.Select
    )