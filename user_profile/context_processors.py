from notifications.models import Notification

def user_notifications(request):
    context = {}
    if request.user.is_authenticated:
        nf = Notification.objects.filter(
            user = request.user
        ).order_by('-created_date')
        unseen = nf.exclude(is_seen=True)
        context['notifications'] = nf
        context['unseen'] = unseen.count()

    return context