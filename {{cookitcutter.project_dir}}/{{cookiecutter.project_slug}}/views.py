from django.shortcuts import render


def bad_request(request):
    response = render(request, '400.html')
    response.status_code = 400
    return response


def server_error(request):
    response = render(request, '500.html')
    response.status_code = 500
    return response
