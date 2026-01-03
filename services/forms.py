from django import forms
from .models import ServiceProvider, Category
from locations.models import State,District, Village

class ProviderRegistrationForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['full_name', 'phone_number', 'category', 'state', 'district', 'village', 'profile_photo', 'description']
        
        # Yahan hum Design (CSS Classes) jod rahe hain
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'अपना पूरा नाम लिखें'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '10 अंकों का मोबाइल नंबर'}),
            'category': forms.Select(attrs={'class': 'form-select'}), # Dropdown ke liye form-select
            'state': forms.Select(attrs={'class': 'form-select'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
            'village': forms.Select(attrs={'class': 'form-select'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'अपने काम के बारे में बताएं...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Logic 1: Default Khali Rakho
        self.fields['district'].queryset = District.objects.none()
        self.fields['village'].queryset = Village.objects.none()

        # Logic 2: Agar Form Submit hua (Dropdown Change)
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        # Logic 3: Edit Page (Purana Data Load karo)
        elif self.instance.pk and self.instance.state:
            self.fields['district'].queryset = District.objects.filter(state=self.instance.state).order_by('name')

        # Logic 4: Same for Village
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['village'].queryset = Village.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.district:
            self.fields['village'].queryset = Village.objects.filter(district=self.instance.district).order_by('name')

#Location changes karke dekhne ke liye 
class LocationSelectForm(forms.Form):
    state = forms.ModelChoiceField(queryset=State.objects.all(), label="Rajya (State)", widget=forms.Select(attrs={'class': 'form-select'}))
    district = forms.ModelChoiceField(queryset=District.objects.none(), label="Zila (District)", widget=forms.Select(attrs={'class': 'form-select'}))
    village = forms.ModelChoiceField(queryset=Village.objects.none(), label="Gaon (Village)", widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # --- Wahi HTMX Magic ---
        self.fields['state'].widget.attrs.update({
            'hx-get': '/services/ajax/load-districts/',
            'hx-target': '#id_district'
        })

        self.fields['district'].widget.attrs.update({
            'hx-get': '/services/ajax/load-villages/',
            'hx-target': '#id_village'
        })

        # Logic taaki error hone par data gayab na ho
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['village'].queryset = Village.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass            