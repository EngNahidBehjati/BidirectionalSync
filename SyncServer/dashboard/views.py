import json

from django.shortcuts import render
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import SyncRun


@require_POST
def register_run(request):
    payload = json.loads(request.body)

    with transaction.atomic():
        run, created = SyncRun.objects.get_or_create(
            idempotency_key=payload["idempotency_key"],
            defaults={
                "agent_id": payload["agent_id"],
                "agent_hostname": payload["hostname"],
                "status": "running",
            },
        )

    return JsonResponse(
        {
            "run_id": str(run.id),
            "status": run.status,
        }
    )
