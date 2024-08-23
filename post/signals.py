from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from post.models import Post


@receiver(post_save, sender=Post)
@receiver(pre_save, sender=Post)
def clear_cache_post_data(sender, instance, **kwargs):
    cache.delete('post_list')
    print('Post List cache Deleted')
    post_id = instance.pk
    cache.delete(f'post_detail_{post_id}')
    print('Post Detail cache Deleted')
