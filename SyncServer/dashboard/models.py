from django.db import models
class SyncRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    agent_id = models.CharField(max_length=128)
    agent_hostname = models.CharField(max_length=128)

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)

    status = models.CharField(
        max_length=32,
        choices=[
            ("running", "Running"),
            ("success", "Success"),
            ("failed", "Failed"),
        ],
    )

    push_bytes = models.BigIntegerField(default=0)
    pull_bytes = models.BigIntegerField(default=0)

    error_code = models.CharField(max_length=64, null=True)
    error_message = models.TextField(null=True)

    idempotency_key = models.CharField(max_length=128, unique=True)
