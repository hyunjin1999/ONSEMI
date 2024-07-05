from django.db.models.signals import post_save
from django.dispatch import receiver
from orders_app.models import Order
from management_app.models import Care

@receiver(post_save, sender=Order)
def create_shop_care(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        Care.objects.create(
            care_type='SHOP',
            title=f'SHOP 서비스 요청 - {instance.id}',
            content=f'주문 번호 {instance.id}에 대한 SHOP 서비스 요청입니다.',
            user_id=user,
            care_state='NOT_APPROVED',
        )