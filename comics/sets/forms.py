import datetime

from bootstrap.forms import BootstrapModelForm
from django import forms
from django.template.defaultfilters import slugify

from comics.core.models import Comic
from comics.sets.models import Set

class NewSetForm(BootstrapModelForm):
    class Meta:
        model = Set
        fields = ('name',)

    def save(self, commit=True):
        set = super(NewSetForm, self).save(commit=False)
        set.name = slugify(set.name)
        set.last_modified = datetime.datetime.now()
        set.last_loaded = datetime.datetime.now()
        if commit:
            set.save()
        return set

class EditSetForm(BootstrapModelForm):
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
        comics_set = super(EditSetForm, self).save(commit=False)
        comics_set.last_modified = datetime.datetime.now()
        if commit:
            comics_set.save()
            self.save_m2m()
        return comics_set
