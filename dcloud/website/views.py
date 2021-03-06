from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from restful.models import File
from django.views import View
from django.core.files.base import ContentFile
from django.middleware import csrf
from dcloud import settings
from django.http import HttpResponse
import os
import requests


def home(request):
    return render(request, 'website/home.html')


@login_required
def file_list(request, path):
	cookies = {'sessionid' : request.session.session_key}
	files = requests.get('http://localhost:8000/restapi/list/'+path, cookies=cookies)
	ret = files.json()
	ret['path'] = path
	return render(request, 'website/file_list.html', ret)

@login_required
def file_upload(request, path):
	file = request.FILES.get('file')
	cookies = {'sessionid' : request.session.session_key}
	cookies['csrftoken'] = csrf.get_token(request)
	headers = {'X-CSRFToken': cookies['csrftoken']}
	requests.post('http://localhost:8000/restapi/list/'+path, files={'file': file}, headers=headers, cookies=cookies)
	# TODO delete mdeia/file
	return redirect('file_list', path=path)

@login_required
def make_folder(request, path):
	dir_name = request.POST.get('dir_name')
	cookies = {'sessionid' : request.session.session_key}
	cookies['csrftoken'] = csrf.get_token(request)
	headers = {'X-CSRFToken': cookies['csrftoken']}
	files = requests.put('http://localhost:8000/restapi/list/'+path, headers=headers, cookies=cookies)
	return redirect('file_list', path=path)

@login_required
def file_delete(request, path):
	cookies = {'sessionid' : request.session.session_key}
	cookies['csrftoken'] = csrf.get_token(request)
	headers = {'X-CSRFToken': cookies['csrftoken']}
	requests.delete('http://localhost:8000/restapi/file/'+path, headers=headers, cookies=cookies)
	new_path = "/".join(path.split("/")[:-1])
	if new_path != '':
		new_path = new_path+'/'
	return redirect('file_list', path=new_path)

@login_required
def file_download(request, path):
	cookies = {'sessionid' : request.session.session_key}
	requests.get('http://localhost:8000/restapi/file/'+path, cookies=cookies)
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type='multipart/form-data' )
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
	raise Http404

@login_required
def file_view(request, path):
	cookies = {'sessionid' : request.session.session_key}
	requests.get('http://localhost:8000/restapi/file/'+path, cookies=cookies)
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type='text/plain' )
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
	raise Http404

@login_required
def file_copy(request, old_path, new_path):
	cookies = {'sessionid' : request.session.session_key}
	cookies['csrftoken'] = csrf.get_token(request)
	headers = {'X-CSRFToken': cookies['csrftoken']}
	files = requests.post('http://localhost:8000/restapi/file-mod/'+old_path+'&'+new_path, data={'method': 'cp'}, headers=headers, cookies=cookies)
	print(files.json())
	new_path = "/".join(new_path.split("/")[:-1])
	if new_path != '':
		new_path = new_path+'/'
	return redirect('file_list', path=new_path)
	
@login_required
def file_move(request, old_path, new_path):
	cookies = {'sessionid' : request.session.session_key}
	cookies['csrftoken'] = csrf.get_token(request)
	headers = {'X-CSRFToken': cookies['csrftoken']}
	files = requests.post('http://localhost:8000/restapi/file-mod/'+old_path+'&'+new_path, data={'method': 'mv'}, headers=headers, cookies=cookies)
	print(files.json())
	new_path = "/".join(new_path.split("/")[:-1])
	if new_path != '':
		new_path = new_path+'/'
	return redirect('file_list', path=new_path)
	