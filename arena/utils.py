def add_client_data(request, data):
    data['ip_address'] = request.META.get('REMOTE_ADDR')
    data['user_agent'] = request.META.get('HTTP_USER_AGENT')

    return data


def add_user_to_post_data(request, key_name='user'):
    data = request.POST.copy()
    data[key_name] = request.user.id

    return data