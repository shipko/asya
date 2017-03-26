from datetime import datetime
from api.models import Message, User
from api.helpers import success_response, failure_response, get_param_or_fail, not_logged_response

MESSAGE_TYPES = {
    'all': 1,
    'individual': 2
}

def list(request):
    if not request.client.log_in:
        return not_logged_response()

    messages = Message.objects.values()

    return success_response({
        'items': [entry for entry in messages]
    })


def add(request):
    if not request.client.is_admin():
        return failure_response("You don't have sufficient permissions")
    try:
        title = get_param_or_fail(request, 'title')
        text = get_param_or_fail(request, 'text')
        type = get_param_or_fail(request, 'type')
        user = get_param_or_fail(request, 'user', is_required=False)
        time = datetime.now()

        if user and int(type) == MESSAGE_TYPES['individual']:
            user = User.objects.get(id=user)
            user_id = user.id
        else:
            user_id = 0

        message = Message(title=title, type=type, text=text, time=time, user=user_id)

        message.save()
    except User.DoesNotExist as e:
        return failure_response('User is not found')
    except Exception as e:
        return failure_response(e.args[0])

    return success_response(message.id)



def edit(request):
    if not request.client.is_admin():
        return failure_response("You don't have sufficient permissions")

    id = get_param_or_fail(request, 'id')
    title = get_param_or_fail(request, 'title')
    text = get_param_or_fail(request, 'text')
    type = get_param_or_fail(request, 'type')
    user = get_param_or_fail(request, 'user', is_required=False)
    time = datetime.now()

    try:

        if user and int(type) == MESSAGE_TYPES['individual']:
            user = User.objects.get(id=user)
            user_id = user.id
        else:
            user_id = 0
        message = Message.objects.get(id=id)

        message.title = title
        message.text = text
        message.type = type
        message.time = time
        message.user = user_id

        message.save()
    except Message.DoesNotExist:
        return failure_response("Category with this id is not exists")

    return success_response(message.id)


def delete(request):
    if not request.client.is_admin():
        return failure_response("You don't have sufficient permissions")

    id = get_param_or_fail(request, 'id')

    try:
        quest = Message.objects.get(id=id)
        quest.delete()

        return success_response('1')
    except Message.DoesNotExist:
        return failure_response('Quest is not found')