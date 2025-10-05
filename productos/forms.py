from django import forms
from .models import Producto, Medida, ProductoMedida, CategoriaMedida 
from django.forms import inlineformset_factory, modelformset_factory


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio_unitario', 'cantidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ProductoMedidaForm(forms.ModelForm):
    class Meta:
        model = ProductoMedida
        fields = ['medidas', 'longitud']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        grouped_choices = []
        categorias = CategoriaMedida.objects.prefetch_related('medida_set')

        for categoria in categorias:
            opciones = [(medida.id, f"{medida.nombre} ({medida.unidad})") for medida in categoria.medida_set.all()]
            grouped_choices.append((categoria.nombre, opciones))

        self.fields['medidas'].choices = grouped_choices

ProductoFormSet = modelformset_factory(
    Producto,
    form=ProductoForm,
    extra=1,
    can_delete=False
)


ProductoMedidaFormSet = inlineformset_factory(
    Producto,
    ProductoMedida,
    form=ProductoMedidaForm,
    extra=1,
    can_delete=False
)
