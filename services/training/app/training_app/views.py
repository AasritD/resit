import os
import subprocess
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from mlflow.tracking import MlflowClient
from .models import ExperimentRun
from .serializers import ExperimentRunSerializer
from django.utils.dateparse import parse_datetime

class ExperimentRunViewSet(viewsets.ModelViewSet):
    """
    CRUD for ExperimentRun records.
    """
    queryset = ExperimentRun.objects.all().order_by('-start_time')
    serializer_class = ExperimentRunSerializer

class TrainingViewSet(viewsets.ViewSet):
    """
    Custom endpoints to trigger training and list MLflow runs.
    """
    @action(detail=False, methods=['post'])
    def retrain(self, request):
        # Runs the training script synchronously
        script = os.path.join(
            os.path.dirname(__file__), 'scripts', 'train.py'
        )
        proc = subprocess.run(
            ['python', script],
            capture_output=True, text=True
        )
        if proc.returncode != 0:
            return Response(
                {'error': proc.stderr},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {'output': proc.stdout},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def runs(self, request):
        # Fetch MLflow runs and optionally mirror to Django DB
        uri = os.getenv('MLFLOW_TRACKING_URI', 'http://mlflow:5000')
        client = MlflowClient(tracking_uri=uri)
        exp = client.get_experiment_by_name('mlaas_experiment')
        if not exp:
            return Response([], status=status.HTTP_200_OK)

        mlflow_runs = client.search_runs(
            [exp.experiment_id],
            order_by=['attributes.start_time DESC']
        )
        resp = []
        for r in mlflow_runs:
            start = parse_datetime(r.info.start_time.isoformat()) \
                if hasattr(r.info, 'start_time') else None
            end = parse_datetime(r.info.end_time.isoformat()) \
                if hasattr(r.info, 'end_time') else None
            data = {
                'run_id': r.info.run_id,
                'status': r.info.status,
                'metrics': r.data.metrics,
                'params': r.data.params,
                'start_time': start,
                'end_time': end
            }
            resp.append(data)
            # Optionally: sync to Django DB
            ExperimentRun.objects.update_or_create(
                run_id=r.info.run_id,
                defaults={
                    'status': r.info.status,
                    'metrics': r.data.metrics,
                    'params': r.data.params,
                    'start_time': start,
                    'end_time': end
                }
            )
        return Response(resp, status=status.HTTP_200_OK)
