from django import forms
from historia.models import Persona, Imagen, Archivo, Entrada


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'dni']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['apellido', 'nombre', 'dni', 'email', 'nacimiento', 'sexo']
        widgets = {'nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            current_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{current_classes} form-control'
        
class PacienteFullForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['apellido', 'nombre', 'dni', 'email', 'nacimiento', 'sexo', 'localidad', 'ocupacion', 'telefono', 'sangre',
                   'obraSocial', 'afiliado', 'obraSocial2', 'afiliado2',
                    'peso', 'altura', 'extras']
        widgets = {'nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
                   'peso': forms.NumberInput(attrs={'min': 0, 'max': '999'}),
                   'altura': forms.NumberInput(attrs={'min': 0, 'max': '9'}) # 'class': 'form-control'
                   }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            current_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{current_classes} form-control'

class OpticaExamForm(forms.ModelForm):

    # 21 fields inside 7 json fields
    akr_od = forms.CharField(label="AKR OD", required=False)
    akr_oi = forms.CharField(label="AKR OI", required=False)
    av_sc_od = forms.CharField(label="AV/SC OD", required=False)
    av_sc_oi = forms.CharField(label="AV/SC OI", required=False)
    av_sc_ao = forms.CharField(label="AV/SC AO", required=False)
    av_cc_od = forms.CharField(label="AV/CC OD", required=False)
    av_cc_oi = forms.CharField(label="AV/CC OI", required=False)
    av_cc_ao = forms.CharField(label="AV/CC AO", required=False)
    retinoscopia_od = forms.CharField(label="RET OD", required=False)
    retinoscopia_oi = forms.CharField(label="RET OI", required=False)
    subjetivo_od = forms.CharField(label="SUB/AFI OD", required=False)
    subjetivo_av_od = forms.CharField(label="SUB/AFI AV OD", required=False)
    subjetivo_oi = forms.CharField(label="SUB/AFI OI", required=False)
    subjetivo_av_oi = forms.CharField(label="SUB/AFI AV OI", required=False)
    subjetivo_av_ao = forms.CharField(label="SUB/AFI AV AO", required=False)
    add_od = forms.CharField(label="ADD OD", required=False)
    add_oi = forms.CharField(label="ADD OI", required=False)
    formula_lej_od = forms.CharField(label="Final lejos OD", required=False)
    formula_lej_oi = forms.CharField(label="Final lejos OI", required=False)
    formula_cer_od = forms.CharField(label="Final cerca OD", required=False)
    formula_cer_oi = forms.CharField(label="Final cerca OI", required=False)

    class Meta:
        model = Entrada
        fields = ['motivo_consulta', 'medicamentos', 'antec_medicos', 'antec_oculares', 'obs_segmento', 'obs_generales']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["motivo_consulta"].widget.attrs.update({'class': "myArea"})
        self.fields["medicamentos"].widget.attrs.update({'class': "myArea"})
        self.fields["antec_medicos"].widget.attrs.update({'class': "myArea"})
        self.fields["antec_oculares"].widget.attrs.update({'class': "myArea"})
        self.fields["obs_segmento"].widget.attrs.update({'class': "myArea"})
        self.fields["obs_generales"].widget.attrs.update({'class': "myArea"})
        # Prepopulate inputs from JSON content into form fields on render
        if self.instance and self.instance.pk:
            akr = self.instance.akr or {}
            av_sc = self.instance.av_sc or {}
            av_cc = self.instance.av_cc or {}
            retinoscopia = self.instance.retinoscopia or {}
            subjetivo = self.instance.subjetivo or {}
            add = self.instance.add or {}
            formula = self.instance.formula or {}

            self.fields["akr_od"].initial = akr.get("OD", "")
            self.fields["akr_oi"].initial = akr.get("OI", "")
            self.fields["av_sc_od"].initial = av_sc.get("OD", "")
            self.fields["av_sc_oi"].initial = av_sc.get("OI", "")
            self.fields["av_sc_ao"].initial = av_sc.get("AO", "")
            self.fields["av_cc_od"].initial = av_cc.get("OD", "")
            self.fields["av_cc_oi"].initial = av_cc.get("OI", "")
            self.fields["av_cc_ao"].initial = av_cc.get("AO", "")
            self.fields["retinoscopia_od"].initial = retinoscopia.get("OD", "")
            self.fields["retinoscopia_oi"].initial = retinoscopia.get("OI", "")
            self.fields["subjetivo_od"].initial = subjetivo.get("OD", "")
            self.fields["subjetivo_av_od"].initial = subjetivo.get("AV_OD", "")
            self.fields["subjetivo_oi"].initial = subjetivo.get("OI", "")
            self.fields["subjetivo_av_oi"].initial = subjetivo.get("AV_OI", "")
            self.fields["subjetivo_av_ao"].initial = subjetivo.get("AV_AO", "")
            self.fields["add_od"].initial = add.get("OD", "")
            self.fields["add_oi"].initial = add.get("OI", "")
            self.fields["formula_lej_od"].initial = formula.get("lejos_OD", "")
            self.fields["formula_lej_oi"].initial = formula.get("lejos_OI", "")
            self.fields["formula_cer_od"].initial = formula.get("cerca_OD", "")
            self.fields["formula_cer_oi"].initial = formula.get("cerca_OI", "")
        for name, field in self.fields.items():
            current_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{current_classes} form-control cajita'

    def clean(self):
        cleaned = super().clean()
        # Pack all form inputs back into JSONs on post
        od, oi = cleaned.get("akr_od"), cleaned.get("akr_oi")
        cleaned["akr"] = {"OD": od, "OI": oi} if (od or oi) else {}

        od, oi, ao = cleaned.get("av_sc_od"), cleaned.get("av_sc_oi"), cleaned.get("av_sc_ao")
        cleaned["av_sc"] = {"OD": od, "OI": oi, "AO": ao} if (od or oi or ao) else {}

        od, oi, ao = cleaned.get("av_cc_od"), cleaned.get("av_cc_oi"), cleaned.get("av_cc_ao")
        cleaned["av_cc"] = {"OD": od, "OI": oi, "AO": ao} if (od or oi or ao) else {}

        od, oi = cleaned.get("retinoscopia_od"), cleaned.get("retinoscopia_oi")
        cleaned["retinoscopia"] = {"OD": od, "OI": oi} if (od or oi) else {}

        od, av_od, oi, av_oi, av_ao = cleaned.get("subjetivo_od"), cleaned.get("subjetivo_av_od"), cleaned.get("subjetivo_oi"), cleaned.get("subjetivo_av_oi"), cleaned.get("subjetivo_av_ao")
        cleaned["subjetivo"] = {"OD": od, "AV_OD": av_od, "OI": oi, "AV_OI": av_oi, "AV_AO": av_ao} if any([od, av_od, oi, av_oi, av_ao]) else {}

        od, oi = cleaned.get("add_od"), cleaned.get("add_oi")
        cleaned["add"] = {"OD": od, "OI": oi} if (od or oi) else {}

        lej_od, lej_oi, cer_od, cer_oi = cleaned.get("formula_lej_od"), cleaned.get("formula_lej_oi"), cleaned.get("formula_cer_od"), cleaned.get("formula_cer_oi")
        cleaned["formula"] = {"lejos_OD": lej_od, "lejos_OI": lej_oi, "cerca_OD": cer_od, "cerca_OI": cer_oi} if any([lej_od, lej_oi, cer_od, cer_oi]) else {}


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.akr = self.cleaned_data["akr"]
        instance.av_sc = self.cleaned_data["av_sc"]
        instance.av_cc = self.cleaned_data["av_cc"]
        instance.retinoscopia = self.cleaned_data["retinoscopia"]
        instance.subjetivo = self.cleaned_data["subjetivo"]
        instance.add = self.cleaned_data["add"]
        instance.formula = self.cleaned_data["formula"]
        if commit:
            instance.save()
        return instance



class ImagenUploadForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Imagen
        fields = ['archivo', 'fecha']

class ArchivoUploadForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Archivo
        fields = ['archivo', 'fecha']