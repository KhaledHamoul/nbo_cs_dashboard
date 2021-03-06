from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.template.response import TemplateResponse
from pprint import pprint
from logging import warning
from app.models import Dataset, Record, Attribute
from api.models import Result, ExecutionLog
from django.db.models import Count
from django.views.decorators.clickjacking import xframe_options_exempt
import json


@login_required(login_url="/login/")
def index(request):
    datasets = Dataset.objects.count()
    records = Record.objects.count()
    attributes = Attribute.objects.count()
    results = Result.objects.count()
    
    logs = ExecutionLog.objects.order_by('-created_at').all()[0:20]

    params = {
        'datasets': datasets,
        'records': records,
        'attributes': attributes,
        'results': results,
        'logs': logs
    }

    return render(request, "index.html", params)


@login_required(login_url="/login/")
@xframe_options_exempt
def pages(request):
    context = {}
    try:
        load_template = request.path[1:]
        html_template = loader.get_template(load_template + '.html')
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        try:
            load_template = request.path.split('/')[-1]
            html_template = loader.get_template(load_template)
            return HttpResponse(html_template.render(context, request))

        except template.TemplateDoesNotExist:
            html_template = loader.get_template('errors/error-404.html')
            return HttpResponse(html_template.render(context, request))

        except:

            html_template = loader.get_template('errors/error-500.html')
            return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('errors/error-500.html')
        return HttpResponse(html_template.render(context, request))

# index


@login_required(login_url="/login/")
def data_index(request):
    datasets = Dataset.objects.annotate(
        records_count=Count("records")).filter(deleted=False)
    return render(request, "data/index.html", {'datasets': datasets})

# view


@login_required(login_url="/login/")
def data_view(request, id):
    try:
        dataset = Dataset.objects.get(id=id)
        records = dataset.records.all()[0:40]
        return render(request, "data/view.html", {'dataset': dataset, 'records': records})
    except Dataset.DoesNotExist:
        print('Dataset #{id} does not exist !')
        return redirect('data_index')

# update


@login_required(login_url="/login/")
def data_update(request, id):
    try:
        dataset = Dataset.objects.get(id=id)
        return render(request, "data/update.html", {'dataset': dataset, 'fields': ['name', 'label', 'description', 'attribute_type']})
    except Dataset.DoesNotExist:
        print('Dataset #{id} does not exist !')
        return redirect('data_index')

# delete


@login_required(login_url="/login/")
def data_delete(request, id):
    try:
        dataset = Dataset.objects.get(id=id)
        # dataset.attributes.all().delete()
        dataset.records.all().delete()
        dataset.delete()
        # dataset.deleted = True
        # dataset.save()
    except Dataset.DoesNotExist:
        print('Dataset #{id} does not exist !')

    return redirect('data_index')

@login_required(login_url="/login/")
def data_clone(request, id):
    try:
        dataset = Dataset.objects.get(id=id)
        return render(request, "data/clone.html", {'dataset': dataset, 'fields': ['name', 'label', 'description', 'attribute_type']})
    except Dataset.DoesNotExist:
        print('Dataset #{id} does not exist !')
        return redirect('data_index')


@login_required(login_url="/login/")
def optimum_clusters_number(request):
    datasets = Dataset.objects.annotate(
        records_count=Count("records")).filter(deleted=False)
    algorithms = [
        {
            "label": 'Elbow',
            "method": 'elbow'
        },
        {
            "label": 'Silhouette',
            "method": 'silhouette'
        },
        {
            "label": 'Gap Statistic',
            "method": 'gap_statistic'
        }
    ]
    
    return render(request, "analysis/optimum_clusters_number.html", {'datasets': datasets, 'algorithms': algorithms})


@login_required(login_url="/login/")
def clustering(request):
    from django.template.loader import render_to_string

    datasets = Dataset.objects.annotate(
        records_count=Count("records")).filter(deleted=False)
    algorithms = [
        {
            "label": 'K-Means',
            "method": 'kmeans',
            "info": render_to_string('methods_info/kmeans.html')
        },
        {
            "label": 'MiniBatch K-Means',
            "method": 'mini_batch_kmeans',
            "info": render_to_string('methods_info/mini_batch_kmeans.html')
        },
        {
            "label": 'Birch',
            "method": 'birch',
            "info": render_to_string('methods_info/birch.html')
        },
        {
            "label": 'Hierarchical',
            "method": 'hierarchical',
            "info": render_to_string('methods_info/hierarchical.html')
        },
        {
            "label": 'Spectral',
            "method": 'spectral',
            "info": render_to_string('methods_info/spectral.html')
        },
        {
            "label": 'MeanShift',
            "method": 'mean_shift',
            "info": render_to_string('methods_info/mean_shift.html')
        },
        {
            "label": 'DBSCAN',
            "method": 'dbscan',
            "info": render_to_string('methods_info/dbscan.html')
        },
        {
            "label": 'OPTICS',
            "method": 'optics',
            "info": render_to_string('methods_info/optics.html')
        }
    ]

    linkageMethods = [
        {
            "label": 'Ward',
            "method": 'ward'
        },
        {
            "label": 'Single',
            "method": 'single'
        },
        {
            "label": 'Complete',
            "method": 'complete'
        },
        {
            "label": 'Average',
            "method": 'average'
        }
    ]

    return render(request, "analysis/clustering.html", {'datasets': datasets, 'algorithms': algorithms, "linkageMethods": linkageMethods})


@login_required(login_url="/login/")
def results_index(request):
    results = Result.objects.all()
    return render(request, "analysis/results/index.html", {'results': results})


# view
@login_required(login_url="/login/")
def results_view(request, id):
    try:
        result = Result.objects.get(id=id)
        indexes = json.loads(result.indexes)

        return render(request, "analysis/results/view.html", {'result': result, 'indexes': indexes})
    except Result.DoesNotExist:
        print('Result #{id} does not exist !')

        return redirect('results_index')

# delete


@login_required(login_url="/login/")
def results_delete(request, id):
    try:
        result = Result.objects.get(id=id)
        result.delete()
    except Result.DoesNotExist:
        print('Result #{id} does not exist !')

    return redirect('results_index')
