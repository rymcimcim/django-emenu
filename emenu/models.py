from django.db.models import Model, CharField, TextField, DateTimeField, DecimalField, TimeField, BooleanField, \
    ManyToManyField


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Dish(BaseModel):
    name = CharField(max_length=255, db_index=True, blank=False)
    description = TextField(blank=False)
    price = DecimalField(max_digits=6, decimal_places=2)
    prep_time = TimeField(verbose_name='preparation time')
    vegetarian = BooleanField(default=False, verbose_name="vege")

    class Meta:
        verbose_name_plural = "dishes"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class DishCard(BaseModel):
    name = CharField(max_length=255, db_index=True, unique=True)
    description = TextField()
    dishes = ManyToManyField(Dish, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
