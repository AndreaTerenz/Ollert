from django import template
from website.models import Notifications

register = template.Library()


@register.inclusion_tag('notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    # ritorna solamente le notifiche che non sono viste
    notifications = Notifications.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')
    return {'notifications': notifications}
