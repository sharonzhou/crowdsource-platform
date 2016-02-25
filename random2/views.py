from __future__ import division
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from random2 import data
import json
from random2.models import WorkerConfig
from crowdsourcing.models import TaskWorker, Task
from crowdsourcing.utils import get_model_or_none
from django.db.models import Count
import numpy as np


@xframe_options_exempt
@csrf_exempt
def random_index(request, *args, **kwargs):
    daemo_id = request.GET.get('daemo_id', False)
    post_url = '/api/done/?daemo_id=' + str(daemo_id)
    data_mappings = {
        "1": data.yelp_photos,
        "2": data.football,
        "3": data.tweets,
        "4": data.facts

    }
    total_tasks = 4
    projects = []
    project_indexes = [1, 2, 3, 4]
    requesters = {
        "1": 0.25,
        "2": 0.25,
        "3": 0.25,
        "4": 0.25
    }

    if not daemo_id:
        return HttpResponse("Missing identifier", status=400)
    try:
        from django.conf import settings
        from copy import deepcopy
        from hashids import Hashids
        identifier_hash = Hashids(salt=settings.SECRET_KEY, min_length=settings.ID_HASH_MIN_LENGTH)
        if len(identifier_hash.decode(daemo_id)) == 0:
            return HttpResponse("Invalid identifier", status=400)
        task_worker_id, task_id, template_item_id = identifier_hash.decode(daemo_id)
        task_worker = TaskWorker.objects.get(id=task_worker_id)
        task = Task.objects.get(id=task_id)
        repetition = task.project.repetition
        config = WorkerConfig.objects.filter(worker_id=task_worker.worker_id)
        worker_config = None
        processed = []
        if not config:
            for index in project_indexes:
                current_data = WorkerConfig.objects.values('requester').filter(project=index) \
                    .annotate(num_workers=Count('requester')).order_by('num_workers')

                conf = None
                if not current_data:
                    conf = np.random.choice(requesters.keys(), p=requesters.values())
                elif current_data.count() < len(requesters):
                    filtered_requesters = deepcopy(requesters)
                    for c in current_data:
                        if str(c['requester']) in filtered_requesters.keys():
                            del filtered_requesters[str(c['requester'])]
                    for c in processed:
                        if c in filtered_requesters.keys():
                            del filtered_requesters[c]
                    for x in filtered_requesters.keys():
                        if str(x) not in processed:
                            filtered_requesters[x] = 1 / (len(filtered_requesters.keys()))
                    conf = np.random.choice(filtered_requesters.keys(), p=filtered_requesters.values())
                else:
                    conf = str(current_data.first()['requester'])
                processed.append(conf)
                requesters[conf] = 0
                for x in requesters.keys():
                    if x != int(conf) and str(x) not in processed:
                        requesters[x] = 1 / (len(requesters.keys()) - len(processed))
                projects.append({
                    "index": index,
                    "requester": int(conf),
                    "tasks": data_mappings[str(index)]
                })
            WorkerConfig.objects.filter(worker_id=task_worker.worker_id).delete()
            for project in projects:
                WorkerConfig.objects.create(requester=project['requester'],
                                            project=project['index'], worker_id=task_worker.worker_id)
        else:
            for conf in config:
                projects.append({
                    "index": conf.project,
                    "requester": conf.requester,
                    "tasks": data_mappings[str(conf.project)]
                })

    except Exception:
        return HttpResponse("Something went wrong, try again!")

    return render(request, 'authorship.html', {'POST_URL': post_url,
                                               'projects': projects})
