from django import forms

MONTH_CHOICES = [
    ('Ocak', 'Ocak'), ('Şubat', 'Şubat'), ('Mart', 'Mart'),
    ('Nisan', 'Nisan'), ('Mayıs', 'Mayıs'), ('Haziran', 'Haziran'),
    ('Temmuz', 'Temmuz'), ('Ağustos', 'Ağustos'), ('Eylül', 'Eylül'),
    ('Ekim', 'Ekim'), ('Kasım', 'Kasım'), ('Aralık', 'Aralık')
]

class AnalyticsForm(forms.Form):
    # Month 1
    month1 = forms.ChoiceField(
        choices=MONTH_CHOICES,
        initial='Ocak',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    value1 = forms.IntegerField(
        min_value=0,
        initial=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    # Month 2
    month2 = forms.ChoiceField(
        choices=MONTH_CHOICES,
        initial='Şubat',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    value2 = forms.IntegerField(
        min_value=0,
        initial=150,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


    # Bar width
