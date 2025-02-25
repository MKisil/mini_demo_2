from django.core.files.storage import default_storage
from django.shortcuts import render
import markdown
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from google import genai

from config import settings
from demo.forms import CallsUploadForm
from demo.models import CallsAnalysis

@csrf_exempt
def calls_analyze_view(request):
    if request.method == "POST":
        form = CallsUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instruction = form.cleaned_data['instruction']
            uploaded_file = request.FILES.get('file')

            file_name = default_storage.save(f"tmp/{uploaded_file.name}", uploaded_file)
            file_path = default_storage.path(file_name)

            client = genai.Client(api_key=settings.GEMINI_API_KEY)

            gemini_file = client.files.upload(file=file_path)

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[instruction, gemini_file]
            )

            response_text = response.text

            call_analysis = CallsAnalysis.objects.create(
                audio_file=file_name,
                analysis_result=response_text
            )

            return render(request, "call_analyzed.html", {"obj": call_analysis, "response_text": response_text})
    else:
        form = CallsUploadForm()

    return render(request, "call_upload.html", {"form": form})
