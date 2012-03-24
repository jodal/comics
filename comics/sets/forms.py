import datetime

from django import forms
from django.template.defaultfilters import slugify

from comics.core.models import Comic
from comics.sets.models import Set

class NewNamedSetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ('name',)

    def save(self, commit=True):
        named_set = super(NewNamedSetForm, self).save(commit=False)
        named_set.name = slugify(named_set.name)
        named_set.last_modified = datetime.datetime.now()
        named_set.last_loaded = datetime.datetime.now()
        if commit:
            named_set.save()
        return named_set

class EditNamedSetForm(forms.ModelForm):
    comics = forms.ModelMultipleChoiceField(
        Comic.objects.filter(active=True), required=False)
    add_new_comics = forms.BooleanField(
        label='Automatically add new comics to the set', required=False,
        help_text='If you check this, all new comics added to the site will ' +
            'automatically be added to your comic set. You may of course '
            'later remove them using this page.')
    hide_empty_comics = forms.BooleanField(
        label='Hide comics without matching releases from view',
        required=False,
        help_text='If you check this, comics without releases in your ' +
            'selected time interval will be hidden.')

    class Meta:
        model = Set
        fields = ('comics', 'add_new_comics', 'hide_empty_comics')

    def save(self, commit=True):
        named_set = super(EditNamedSetForm, self).save(commit=False)
        named_set.last_modified = datetime.datetime.now()
        if commit:
            named_set.save()
            self.save_m2m()
        return named_set
