# -*- coding: utf-8 -*-

def ds_checkrequest_form():
    if request.method == 'POST':
        return "required.method = POST"
    else :
        return "else return"
    return 

def ds_return_check():
    return HttpResponse('this is used by return_check')

    