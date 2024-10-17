from django import forms

from .models import Location, Product, Task


class LocationForm(forms.ModelForm):
    """Formulář pro model Location."""
    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            "shelf": forms.NumberInput(attrs={"min": 1, "max": 20})
        }


class ProductForm(forms.ModelForm):
    """Formulář pro model Product."""
    class Meta:
        model = Product
        exclude = ["is_active", "is_check", "old_location", "slug"]

    def clean_product_id(self):
        """
        Validuje pole 'product_id' pro zajištění unikátnosti.
        Pokud produkt s daným 'product_id' již existuje, vyvolá ValidationError (kromě aktuálně upravovaného).
        """
        product_id = self.cleaned_data.get("product_id")
        # self.instance.pk: Pokud formulář edituje existující záznam (produkt), má instance produktu své pk,
        # což znamená, že nejde o nový záznam, ale o úpravu existujícího
        if Product.objects.filter(product_id=product_id).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Produkt s tímto kódem již existuje.")
        return product_id


class TaskForm(forms.ModelForm):
    """Formulář pro model Task."""
    class Meta:
        model = Task
        exclude = ["is_done"]
