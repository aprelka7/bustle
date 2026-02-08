# Generated manually

from django.db import migrations


def create_default_allergens(apps, schema_editor):
    Allergen = apps.get_model('main', 'Allergen')
    defaults = [
        ('Глютен', 'gluten'),
        ('Лактоза', 'lactose'),
        ('Орехи', 'nuts'),
        ('Яйца', 'eggs'),
        ('Рыба', 'fish'),
        ('Моллюски', 'shellfish'),
        ('Соя', 'soy'),
        ('Горчица', 'mustard'),
        ('Сельдерей', 'celery'),
        ('Кунжут', 'sesame'),
        ('Сульфиты', 'sulphites'),
        ('Арахис', 'peanuts'),
    ]
    for name, slug in defaults:
        Allergen.objects.get_or_create(slug=slug, defaults={'name': name})


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_add_allergens'),
    ]

    operations = [
        migrations.RunPython(create_default_allergens, noop),
    ]
