import os, joblib, shap
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ModelArtifact, InferenceLog
from .serializers import ModelArtifactSerializer, InferenceLogSerializer
from .forms import UploadForm

class ModelArtifactViewSet(viewsets.ModelViewSet):
    queryset = ModelArtifact.objects.all().order_by('-uploaded_at')
    serializer_class = ModelArtifactSerializer

class InferenceViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def predict(self, request):
        f = request.FILES['file']
        artifact = ModelArtifact.objects.order_by('-uploaded_at').first()
        model = joblib.load(artifact.file.path)
        # load preprocessor
        pre = joblib.load(os.path.join(os.path.dirname(artifact.file.path),'..','models','preprocessor.joblib'))
        X = pre.transform([f.read().decode().split(',')])  # adapt for CSV/text
        pred = model.predict(X)[0]
        explainer = shap.Explainer(model, X)
        shap_vals = explainer(X).values.tolist()
        log = InferenceLog.objects.create(
            user=request.user, model=artifact,
            input_file=f, prediction=str(pred),
            shap_values=shap_vals
        )
        return Response(InferenceLogSerializer(log).data, status=status.HTTP_201_CREATED)

@login_required
def upload_ui(request):
    pred=None; shap_vals=None
    if request.method=='POST':
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            resp = InferenceViewSet().predict(request)
            data = resp.data
            pred = data['prediction']; shap_vals = data['shap_values']
            form = UploadForm()
    else:
        form=UploadForm()
    return render(request,'inference/upload.html',{'form':form,'prediction':pred,'shap':shap_vals})

@login_required
def dashboard(request):
    """
    Simple inference dashboard view.
    URL: /inference/dashboard/
    """
    return render(request, 'inference/dashboard.html')
