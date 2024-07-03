from django.db.models.signals import post_save
from django.dispatch import receiver
from orders_app.models import Order
from management_app.models import Care

# 주문이 접수가 되면 바로 SHOP 서비스를 요청한 셈이니까 이를 고려하여 작성
@receiver(post_save, sender=Order)
def create_shop_care(sender, instance, created, **kwargs):
    if created:
        user = instance.user  # 주문을 생성한 사용자
        Care.objects.create(
            care_type='SHOP',
            title=f'SHOP 서비스 요청 - {instance.id}',
            content=f'주문 번호 {instance.id}에 대한 SHOP 서비스 요청입니다.',
            user_id=user,
            care_state='NOT_APPROVED',
        )