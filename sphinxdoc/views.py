# encoding: utf-8

import datetime
import json
import os.path

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.views.static import serve

from sphinxdoc.models import Project, Document


BUILDDIR = os.path.join('_build', 'json')


@cache_page(60 * 5)
def documentation(request, slug, path):
    project = get_object_or_404(Project, slug=slug)
    path = path.rstrip('/')
    
    try:
        index = 'index' if path == '' else '%s/index' % path
        doc = Document.objects.get(project=project, path=index)
    except ObjectDoesNotExist:
        doc = get_object_or_404(Document, project=project, path=path)

    templates = (
        'sphinxdoc/%s.html' % os.path.basename(path),
        'sphinxdoc/documentation.html',
    )
    
    data = {
        'project': project,
        'doc': json.loads(doc.content),
        'env': json.load(open(
                os.path.join(project.path, BUILDDIR, 
                'globalcontext.json'), 'rb')),
        'update_date':  datetime.datetime.fromtimestamp(
                os.path.getmtime(os.path.join(project.path, BUILDDIR,
                'last_build'))),
    }
        
    return render_to_response(templates, data,
            context_instance=RequestContext(request))

def search(request, slug):
    from django.http import HttpResponse
    return HttpResponse('Not yet implemented.')

@cache_page(60 * 5)
def objects_inventory(request, slug):
    project = get_object_or_404(Project, slug=slug)
    response = serve(
        request, 
        document_root = project.path,
        path = "objects.inv",
    )
    response['Content-Type'] = "text/plain"
    return response

@cache_page(60 * 5)
def images(request, slug, path):
    project = get_object_or_404(Project, slug=slug)
    return serve(
        request, 
        document_root = os.path.join(project.path, '_images'),
        path = path,
    )
    
@cache_page(60 * 5)
def source(request, slug, path):
    project = get_object_or_404(Project, slug=slug)
    return serve(
        request,
        document_root = os.path.join(project.path, '_sources'),
        path = path,
    )
