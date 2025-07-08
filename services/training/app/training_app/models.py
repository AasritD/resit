from django.db import models

class ExperimentRun(models.Model):
    run_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    metrics = models.JSONField()
    params = models.JSONField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.run_id} ({self.status})"
