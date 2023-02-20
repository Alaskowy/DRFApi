from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_delete


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self) -> None:
        post_migrate.connect(self.load_base_tier_plans, sender=self)
        from .models import Image, Thumbnail
        from .signals import delete_image, delete_thumbnail
        post_delete.connect(delete_image, sender=Image)
        post_delete.connect(delete_thumbnail, sender=Thumbnail)

    @classmethod
    def load_base_tier_plans(cls, **kwargs):
        from .models import Tier
        if not Tier.objects.filter(name='Basic').exists():
            Tier.objects.bulk_create([
                Tier(name='Basic', thumbnail_size=[200]),
                Tier(name='Premium', thumbnail_size=[200, 400], original_link_flag=True),
                Tier(name='Enterprise', thumbnail_size=[200, 400], original_link_flag=True, binary_image_link_flag=True)
            ])

