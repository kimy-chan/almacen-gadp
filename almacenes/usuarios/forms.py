from django import forms
from .models import Usuario


class Usuario_formulario(forms.ModelForm):
    confirmar_password= forms.CharField(label='confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}) )
    class Meta:
        model=Usuario
        fields=['username','password','oficina','confirmar_password','email','encargado', 'item','rol','crear','editar','eliminar','unidad']
        widgets={
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'confirmar_password':forms.PasswordInput(attrs={'class': 'form-control'}),
            'encargado':forms.Select(attrs={'class': 'form-control'}),
            'crear': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
             'editar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
              'eliminar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
              'rol':forms.Select(attrs={'class': 'form-control'})
             
        }
        
       

      
        
    def save(self, commit=True):
        user = super(Usuario_formulario, self).save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    def clean(self):
        clean_data= super().clean()
        password = clean_data.get('password')
        confirmar_password=clean_data.get('confirmar_password')
        if(password != confirmar_password):
            self.add_error('confirmar_password', 'Las contraseñas no son iguales')

        