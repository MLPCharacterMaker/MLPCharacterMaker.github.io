from django import forms

from .models import Character, Influence, HangUp, Perk, BackgroundBond


class CharacterForm(forms.ModelForm):
    level = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        label="Level",
    )
    influences = forms.ModelMultipleChoiceField(
        queryset=Influence.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select up to 3 influences."
    )
    perks = forms.ModelMultipleChoiceField(
        queryset=Perk.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select any relevant perks."
    )
    hangups = forms.ModelMultipleChoiceField(
        queryset=HangUp.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select the required number of hang-ups."
    )
    background_bonds = forms.ModelMultipleChoiceField(
        queryset=BackgroundBond.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Character
        fields = [
            'name', 'pronouns', 'level', 'origin', 'pegasus_movement', 'role', 'special_talent',
            'description', 'image', 'cutie_mark_image',
            'base_strength', 'strength_status', 'base_speed', 'speed_status', 'base_smarts', 'smarts_status',
            'base_social', 'social_status', 'public', 'influences', 'perks', 'hangups'
        ]
        widgets = {
            'influences': forms.CheckboxSelectMultiple,
            'perks': forms.CheckboxSelectMultiple,
            'hang_ups': forms.CheckboxSelectMultiple,
        }

        strength = forms.IntegerField(min_value=0, max_value=15, label="Strength")
        speed = forms.IntegerField(min_value=0, max_value=15, label="Speed")
        smarts = forms.IntegerField(min_value=0, max_value=15, label="Smarts")
        social = forms.IntegerField(min_value=0, max_value=15, label="Social")

        strength_status = forms.ChoiceField(
            choices=Character.STATUS_CHOICES, label="Strength Status"
        )
        speed_status = forms.ChoiceField(
            choices=Character.STATUS_CHOICES, label="Speed Status"
        )
        smarts_status = forms.ChoiceField(
            choices=Character.STATUS_CHOICES, label="Smarts Status"
        )
        social_status = forms.ChoiceField(
            choices=Character.STATUS_CHOICES, label="Social Status"
        )

    pegasus_movement = forms.ChoiceField(
        choices=[
            ('15 feet ground, 45 feet air', '15 feet ground, 45 feet air'),
            ('30 feet ground, 30 feet air', '30 feet ground, 30 feet air'),
            ('45 feet ground, 15 feet air', '45 feet ground, 15 feet air'),
        ],
        required=False,  # Make this optional unless it's a Pegasus
        label="Pegasus Movement",
    )

    def clean(self):
        cleaned_data = super().clean()
        strength = cleaned_data.get('strength', 0)
        speed = cleaned_data.get('speed', 0)
        smarts = cleaned_data.get('smarts', 0)
        social = cleaned_data.get('social', 0)
        statuses = [
            cleaned_data.get('strength_status'),
            cleaned_data.get('speed_status'),
            cleaned_data.get('smarts_status'),
            cleaned_data.get('social_status'),
        ]

        # Ensure all statuses are unique
        if len(set(statuses)) != len(statuses):
            raise forms.ValidationError("Each stat must have a unique status (Diamond, Gold, Silver, Bronze).")
        total_points = strength + speed + smarts + social

        return cleaned_data
