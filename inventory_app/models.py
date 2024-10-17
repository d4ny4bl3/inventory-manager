from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


class Room(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name="Označení")
    description = models.CharField(max_length=100, verbose_name="Popis")

    class Meta:
        verbose_name_plural = 'Místnosti'
        verbose_name = 'Místnost'

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if Room.objects.filter(name=self.name).exists():
            raise ValidationError("Tato místnost již existuje")


class Rack(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Místnost", related_name='racks')
    number = models.IntegerField(verbose_name="Číslo regálu")
    total_shelves = models.IntegerField(verbose_name="Celkový počet polic")

    class Meta:
        verbose_name_plural = 'Regály'
        verbose_name = "Regál"

    def __str__(self):
        return f"{self.room.name}{self.number}"

    def clean(self):
        super().clean()
        if Rack.objects.filter(room=self.room, number=self.number).exists():
            raise ValidationError("Tento regál již existuje.")


class Location(models.Model):
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, verbose_name="Regál", related_name="locations")
    shelf = models.IntegerField(verbose_name="Police", validators=[MinValueValidator(1), MaxValueValidator(20)])

    class Meta:
        verbose_name_plural = 'Umístění'
        verbose_name = 'Umístění'

    def __str__(self):
        return f"{self.rack}.{self.shelf}"

    def clean(self):
        super().clean()
        if Location.objects.filter(rack=self.rack, shelf=self.shelf).exists():
            raise ValidationError("Toto umístění již existuje.")

        if self.shelf > self.rack.total_shelves:
            raise ValidationError({
                "shelf": f"Zvolená police je vyšší než maximální počet v regálu. (max {self.rack.total_shelves})"
            })


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Název")
    brand = models.CharField(max_length=100, verbose_name="Značka")
    product_id = models.CharField(max_length=20, db_index=True, unique=True, verbose_name="Kód")
    location = models.ManyToManyField(Location, blank=True, verbose_name="Umístění")
    old_location = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_check = models.BooleanField(default=True)
    slug = models.SlugField(max_length=150, null=True)

    class Meta:
        verbose_name_plural = "Produkty"
        verbose_name = "Produkt"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def deactivate(self):
        """
        Nastavení produktů které nejsou ve feedu na is_active=False,
        nakopírování location do old_location.
        """
        locations = ", ".join([str(location) for location in self.location.all()])
        self.old_location = locations
        # self.location = "Out"
        self.is_active = False
        self.save()


class Task(models.Model):
    task = models.CharField(max_length=150, verbose_name="Název")
    description = models.TextField(verbose_name="Popis")
    is_done = models.BooleanField(default=False, verbose_name="Vyřízeno")

    class Meta:
        verbose_name_plural = "Úkoly"
        verbose_name = "Úkol"

    def __str__(self):
        return self.task
