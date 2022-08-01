import mimetypes
import os
from django.http.response import HttpResponse
from django.shortcuts import render


def downloadfile(request, filename=''):
    if filename != '':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # define file path
        filepath = BASE_DIR + '/mysite/static' + filename
        # open the file for reading content
        path = open(filepath, 'rb')
        # set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # set the Http header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename

        # return the response value
        return response
    else:
        return render(request, 'jazda/index.html')