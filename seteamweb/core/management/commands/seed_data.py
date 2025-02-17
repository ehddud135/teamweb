from django.core.management.base import BaseCommand
from django.apps import apps
from django_seed import Seed
from datetime import datetime
from django.utils.timezone import make_aware
import random


class Command(BaseCommand):
    help = "Seed database with fake data for all models in all apps."

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # 모든 앱의 모델 가져오기
        all_models = []
        for app_config in apps.get_app_configs():
            if app_config.label not in ['auth', 'contenttypes', 'sessions', 'admin']:
                all_models.extend(app_config.get_models())

        # ForeignKey 처리를 위한 참조 데이터 저장
        data_dict = {model: list(model.objects.all()) for model in all_models}

        for model in all_models:
            try:
                # 모델 필드 체크 및 ForeignKey 처리
                fields = {field.name: field for field in model._meta.fields}
                field_values = {}

                for field_name, field in fields.items():
                    if field.get_internal_type() == "ForeignKey":
                        print(field)
                        related_model = field.related_model
                        print(related_model)
                        if related_model in data_dict and data_dict[related_model]:
                            field_values[field_name] = lambda x: random.choice(data_dict[related_model])
                        else:
                            field_values[field_name] = None

                    # 🔥 DateTimeField 처리 (is_dst 제거)
                    elif field.get_internal_type() == "DateTimeField":
                        field_values[field_name] = lambda x: make_aware(datetime.now())

                    # 🔥 DateField 처리
                    elif field.get_internal_type() == "DateField":
                        field_values[field_name] = lambda x: datetime.now().date()

                # 랜덤 데이터 삽입
                seeder.add_entity(model, 10, field_values)
                self.stdout.write(self.style.SUCCESS(f"   ✅ Added 10 records to {model.__name__}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ Skipped {model.__name__}: {str(e)}"))

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("✅ Seeding complete!"))
