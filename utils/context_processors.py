from accounts.models import Notification
from dashboard.models import Payment

def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(
        user = user,read = False
        ).order_by('-date')[:5] if user.is_authenticated else None
    return {'new_notifications':notifications}



def pending_payments_renderer(request):
    return {'pending_payments': Payment.objects.filter(
            status = Payment.Status.PENDING, user=request.user,
        ).count()} if request.user.is_authenticated else {}

def sticky_notification(request):
    user = request.user
    return {'sticky_notification': user.sticky_notifications.first()} if user.is_authenticated else {}