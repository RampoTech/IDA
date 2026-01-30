from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Using standard csrf protection in JS
from .models import ChatMessage
import json

@login_required
@require_POST
def send_message(request):
    try:
        data = json.loads(request.body)
        message_text = data.get('message', '')
        if message_text:
            ChatMessage.objects.create(
                user=request.user,
                message=message_text
            )
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@require_GET
def get_messages(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    data = [{
        'message': msg.message,
        'timestamp': msg.timestamp.strftime('%H:%M'),
        'is_admin_reply': msg.is_admin_reply
    } for msg in messages]
    return JsonResponse({'messages': data})
