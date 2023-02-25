from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление новостей заданной категории'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)





    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))

        category = Category.objects.get(name=options['category'])

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Все новости в категории {category.name} успешно удалены'))  # в случае неправильного подтверждения говорим, что в доступе отказано
        except category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не удалось найти категорию {}'))





