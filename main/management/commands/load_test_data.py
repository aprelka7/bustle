"""
Команда для загрузки тестовых данных: категории, блюда с аллергенами.
Использование: python manage.py load_test_data
"""
from decimal import Decimal

from django.core.management.base import BaseCommand

from main.models import Category, Dish, Allergen


class Command(BaseCommand):
    help = 'Загружает тестовые категории, блюда и назначает аллергены'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Удалить все блюда и категории перед загрузкой (аллергены не трогаем)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Dish.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write('Удалены все блюда и категории.')

        allergens = list(Allergen.objects.all())
        if not allergens:
            self.stdout.write(self.style.WARNING('Нет аллергенов. Сначала примените миграцию 0005_default_allergens.'))
            return

        categories_data = [
            ('Завтрак', 'breakfast'),
            ('Обед', 'lunch'),
            ('Ужин', 'dinner'),
            ('Закуска','snack'),
            ('Десерт', 'dessert'),
            ('Напиток', 'drink'),
        ]

        for name, slug in categories_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
            self.stdout.write(f'Категория: {cat.name}')

        dishes_data = [
            # (name, description, category_slug, price, allergen_names, slug)
            # Завтрак
            ('Яичница с беконом', 'Яичница-глазунья с хрустящим беконом и зеленью', 'breakfast', Decimal('320.00'), ['Яйца', 'Глютен'], 'yaychnica-bekonom'),
            ('Овсяная каша', 'Овсяная каша с ягодами, мёдом и орехами', 'breakfast', Decimal('280.00'), ['Глютен', 'Орехи'], 'ovsyanaya-kasha'),
            ('Сырники со сметаной', 'Нежные творожные сырники с домашней сметаной', 'breakfast', Decimal('350.00'), ['Глютен', 'Яйца', 'Лактоза'], 'syrniki-smetanoy'),
            ('Блины с красной икрой', 'Тонкие блины со сливочным маслом и красной икрой', 'breakfast', Decimal('580.00'), ['Глютен', 'Яйца', 'Рыба', 'Лактоза'], 'bliny-ikroy'),
            ('Авокадо-тост с яйцом пашот', 'Тост из чиабатты с авокадо и яйцом пашот', 'breakfast', Decimal('390.00'), ['Глютен', 'Яйца'], 'avokado-tost'),
            ('Сэндвич с ветчиной и сыром', 'Сэндвич на гриле с ветчиной, сыром и соусом', 'breakfast', Decimal('310.00'), ['Глютен', 'Лактоза', 'Горчица'], 'sendvich-vetchina-syr'),
            ('Гранола с йогуртом', 'Хрустящая гранола с натуральным йогуртом и фруктами', 'breakfast', Decimal('270.00'), ['Глютен', 'Лактоза', 'Орехи'], 'granola-yogurt'),

            # Обед
            ('Бизнес-ланч: Суп + Салат', 'Суп дня и салат "Цезарь" или "Греческий" на выбор', 'lunch', Decimal('550.00'), ['Глютен', 'Яйца', 'Горчица'], 'biznes-lanch-basic'),
            ('Бизнес-ланч: Горячее', 'Горячее блюдо дня (курица/рыба/паста) с гарниром', 'lunch', Decimal('480.00'), ['Глютен', 'Яйца', 'Рыба'], 'biznes-lanch-hot'),
            ('Суп + Сэндвич', 'Суп дня и сэндвич с курицей', 'lunch', Decimal('490.00'), ['Глютен', 'Сельдерей', 'Горчица'], 'sup-sendvich'),
            ('Обеденная пицца Маргарита', 'Пицца 25см с томатами и моцареллой', 'lunch', Decimal('420.00'), ['Глютен', 'Лактоза'], 'pizza-margarita-lunch'),
            ('Куриный бургер с картофелем', 'Сочный бургер с куриной котлетой и картофель фри', 'lunch', Decimal('520.00'), ['Глютен', 'Горчица', 'Соя'], 'burger-chicken-lunch'),

            # Ужин
            ('Стейк из тунца', 'Стейк из тунца с севиче из авокадо и соусом песто', 'dinner', Decimal('850.00'), ['Рыба', 'Орехи'], 'steyk-tuna'),
            ('Утиная грудка', 'Утиная грудка с апельсиновым соусом и пюре из сельдерея', 'dinner', Decimal('780.00'), ['Сельдерей', 'Сульфиты'], 'utinaya-grudka'),
            ('Феттучини с трюфелем', 'Паста феттучини со сливочно-трюфельным соусом', 'dinner', Decimal('720.00'), ['Глютен', 'Лактоза'], 'fettuchini-tryufel'),
            ('Запечённая баранина', 'Баранина, запечённая с розмарином и молодым картофелем', 'dinner', Decimal('920.00'), [], 'zapechennaya-baranina'),
            ('Ролл "Филадельфия" (8 шт)', 'Классический ролл с лососем и сливочным сыром', 'dinner', Decimal('680.00'), ['Рыба', 'Рис', 'Соевый соус'], 'roll-filadelfiya'),

            # Закуска
            ('Брускетта с томатами', 'Гренки с рублеными томатами, базиликом и чесноком', 'snack', Decimal('320.00'), ['Глютен'], 'brusketta-tomaty'),
            ('Карпаччо из говядины', 'Тонкие ломтики говядины с пармезаном и рукколой', 'snack', Decimal('450.00'), ['Горчица', 'Сульфиты', 'Лактоза'], 'karpachcho-govyadina'),
            ('Кальмары в кляре', 'Хрустящие кальмары в пивном кляре с соусом тар-тар', 'snack', Decimal('380.00'), ['Глютен', 'Яйца', 'Рыба', 'Моллюски'], 'kalmary-klare'),
            ('Сырное ассорти', 'Ассорти из трёх видов сыров с орехами и мёдом', 'snack', Decimal('520.00'), ['Лактоза', 'Орехи'], 'syirnoe-assorti'),
            ('Оливки и маринады', 'Миска оливок, маринованных перцев и артишоков', 'snack', Decimal('290.00'), ['Сульфиты'], 'olivki-marinady'),
            ('Гуакамоле с начос', 'Классический гуакамоле с кукурузными чипсами начос', 'snack', Decimal('360.00'), [], 'guakamole-nachos'),

            # Десерт
            ('Мороженое сорбе', 'Лимонное и манговое сорбе в ассортименте', 'dessert', Decimal('300.00'), [], 'morozhenoe-sorbe'),
            ('Эклер ванильный', 'Заварной эклер с ванильным кремом', 'dessert', Decimal('220.00'), ['Глютен', 'Яйца', 'Лактоза'], 'ekler-vanil'),
            ('Пирог "Красный бархат"', 'Влажный шоколадный бисквит с крем-чиз', 'dessert', Decimal('380.00'), ['Глютен', 'Яйца', 'Лактоза'], 'pirog-red-velvet'),
            ('Фондан с малиной', 'Шоколадный фондан с жидкой сердцевиной и малиновым соусом', 'dessert', Decimal('410.00'), ['Глютен', 'Яйца', 'Лактоза'], 'fondan-malina'),
            ('Тарталетка с лимонным курдом', 'Хрустящая тарталетка с нежным лимонным кремом', 'dessert', Decimal('340.00'), ['Глютен', 'Яйца', 'Лактоза'], 'tartaletka-limon'),

            # Напиток
            ('Эспрессо', 'Классический крепкий эспрессо', 'drink', Decimal('150.00'), [], 'espresso'),
            ('Раф кофе', 'Кофе со сливочно-ванильным сиропом и молочной пенкой', 'drink', Decimal('280.00'), ['Лактоза'], 'raf-kofe'),
            ('Мохито безалкогольный', 'Освежающий мохито с лаймом, мятой и содовой', 'drink', Decimal('320.00'), ['Сульфиты'], 'mohito'),
            ('Имбирный лимонад', 'Острый лимонад с имбирём и мёдом', 'drink', Decimal('260.00'), [], 'limonad-imbir'),
            ('Горячий шоколад', 'Густой горячий шоколад со взбитыми сливками', 'drink', Decimal('330.00'), ['Лактоза'], 'goryachiy-shokolad'),
            ('Морс клюквенный', 'Клюквенный морс домашнего приготовления', 'drink', Decimal('200.00'), [], 'mors-klyukva'),
        ]

        slug_to_allergen = {a.name: a for a in allergens}
        slug_to_category = {c.slug: c for c in Category.objects.all()}

        created = 0
        for row in dishes_data:
            name, description, cat_slug, price, allergen_names, slug = row
            cat = slug_to_category.get(cat_slug)
            if not cat:
                continue
            dish, was_created = Dish.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'description': description,
                    'category': cat,
                    'price': price,
                },
            )
            if was_created:
                created += 1
            dish_allergens = [slug_to_allergen[n] for n in allergen_names if n in slug_to_allergen]
            if dish_allergens:
                dish.allergens.set(dish_allergens)

        self.stdout.write(self.style.SUCCESS(f'Готово. Создано блюд: {created}, всего блюд: {Dish.objects.count()}'))
