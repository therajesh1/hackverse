from django.shortcuts import render

# Create your views here.
# from django.shortcuts import  render,redirect,HttpResponse
# from datetime import datetime
# from home.models import Contact,Mhtcetregister,Slotbook
# from django.contrib.auth import authenticate,logout,login
# from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from myapp.middlewares import guest , auth



# Create your views here.\
# @login_required(login_url='loginuser')
from django.shortcuts import render
from .models import CustomUser  # or wherever your student model is defined

# def index(request):
#     student = CustomUser.objects.get(id=request.user.id)  # Replace this with how you fetch your student
#     return render(request, 'index.html', {'student': student})
from django.shortcuts import render
from myapp.models import CustomUser



# def index(request):
#     if request.user.is_authenticated:
#         student_id = request.user.id
#         performance_url = reverse('student_performance', kwargs={'student_id': student_id})
#     else:
#         # Redirect to login page if not authenticated
#         return redirect('student_login')
    
#     return render(request, 'index.html', {'performance_url': performance_url})

def index(request):
   # Fetch by the logged-in user's username
    return render(request, 'index.html')

    # return render(request, 'index.html'), {'student': student})

def accreditation(request):
    return render(request,'accreditation.html')

def syllabus(request):
    return render(request,'syllabus.html')

def rubrics(request):
    return render(request,'rubrics.html')

def questionpaper(request):
    return render(request,'questionpaper.html')

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback
import json

def feedback_form(request):
    """Render the feedback form page"""
    return render(request, 'feedback/feedback_form.html')

# views.py
def thank_you(request):
    return render(request, 'thank_you.html')


# views.py
from django.shortcuts import render, redirect
from .models import Feedback

def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the feedback to the database
        feedback = Feedback(name=name, email=email, message=message)
        feedback.save()

        # Redirect to a 'thank you' page or show a success message
        return redirect('thank_you')  # Redirect to a 'Thank You' page or show a success message

    return render(request, 'feedback_form.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

def student_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        pass1=request.POST.get('pass1')
        user = authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request,'index.html')
    return render(request, 'student_login.html', {'user': request.user})


from django.shortcuts import render, get_object_or_404
from .models import CourseOutcome, ProgramOutcome, COPOMap, Assessment, POProgress
from django.db.models import Avg

def outcome_tracking_dashboard(request):
    """ Dashboard to track CO and PO progress """
    pos = ProgramOutcome.objects.all()
    tracking_data = []

    for po in pos:
        mappings = COPOMap.objects.filter(po=po)
        total_weightage = 0
        student_progress = {}

        for mapping in mappings:
            co = mapping.co
            assessments = Assessment.objects.filter(co=co)

            if assessments.exists():
                avg_score = assessments.aggregate(Avg('marks_obtained'))['marks_obtained__avg']
                progress = (avg_score / 100) * 100  # Assuming 100 is the full mark scale
                total_weightage += progress

        average_progress = total_weightage / mappings.count() if mappings.exists() else 0

        tracking_data.append({
            "name": po.name,
            "description": po.description,
            "progress": round(average_progress, 2),
        })

    return render(request, "tracking_dashboard.html", {"tracking_data": tracking_data})
# def outcome_tracking_dashboard(request):
#     """ Dashboard to track CO and PO progress """
#     pos = ProgramOutcome.objects.all()
#     tracking_data = []

#     for po in pos:
#         mappings = COPOMap.objects.filter(po=po)
#         total_weightage = 0

#         for mapping in mappings:
#             co = mapping.co
#             assessments = Assessment.objects.filter(co=co)

#             if assessments.exists():
#                 avg_score = assessments.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
#                 progress = (avg_score / 100) * 100  # Assuming 100 is the full mark scale
#                 total_weightage += progress

#         average_progress = total_weightage / mappings.count() if mappings.exists() else 0

#         tracking_data.append({
#             "po_name": po.name,
#             "description": po.description,
#             "progress": round(average_progress, 2),
#         })

#     # Debug print to check data
#     print("Tracking Data:", tracking_data)

#     return render(request, "tracking_dashboard.html", {"tracking_data": tracking_data})
# from django.contrib.auth import get_user_model  # Import this
# User = get_user_model()  # Get the custom user model

# def student_performance(request, student_id):
#     """ Show CO and PO progress for a specific student """
#     student = get_object_or_404(CustomUser, id=student_id)
#     assessments = Assessment.objects.filter(student=student)
    
#     progress_data = []
#     for assessment in assessments:
#         co = assessment.co
#         co_maps = COPOMap.objects.filter(co=co)

#         for mapping in co_maps:
#             po = mapping.po
#             progress, created = POProgress.objects.get_or_create(student=student, po=po)
#             progress.progress_percentage = (assessment.marks_obtained / assessment.total_marks) * 100
#             progress.save()

#             progress_data.append({
#                 "name": co.name,
#                 # "po_name": po.name,
#                 "marks": assessment.marks_obtained,
#                 "total_marks": assessment.total_marks,
#                 "progress": round(progress.progress_percentage, 2),
#             })

#     return render(request, "student_performance.html", {"progress_data": progress_data, "student": student})
from django.shortcuts import get_object_or_404, render
from myapp.models import CustomUser, Assessment, COPOMap, POProgress

def student_performance(request, username):
    """ Show CO and PO progress for a specific student based on username """
    student = get_object_or_404(CustomUser, username=username)  # Fetch by username
    assessments = Assessment.objects.filter(student=student)
    
    progress_data = []
    for assessment in assessments:
        co = assessment.co
        co_maps = COPOMap.objects.filter(co=co)

        for mapping in co_maps:
            po = mapping.po
            progress, created = POProgress.objects.get_or_create(student=student, po=po)
            progress.progress_percentage = (assessment.marks_obtained / assessment.total_marks) * 100
            progress.save()

            progress_data.append({
                "name": co.name,
                "marks": assessment.marks_obtained,
                "total_marks": assessment.total_marks,
                "progress": round(progress.progress_percentage, 2),
            })

    return render(request, "student_performance.html", {"progress_data": progress_data, "student": student})


import google.generativeai as genai
from django.shortcuts import render
from .models import ProgramOutcome
import json
import re

# Configure the Gemini API
genai.configure(api_key="AIzaSyArYroSmf7e1ZMLi9CY-ALNaAcg0igXEQs")

def co_po_mapping(request):
    if request.method == "POST":
        co_text = request.POST.get("co_text", "").strip()

        if not co_text:
            return render(request, "mapping_form.html", {
                "error": "Please enter a Course Outcome description."
            })

        # Fetch all Program Outcomes (names + descriptions)
        po_list = list(ProgramOutcome.objects.values("name", "description"))

        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Construct the mapping prompt
        mapping_prompt = f"""
        Course Outcome: '{co_text}'

        Perform a systematic mapping of this Course Outcome to the following Program Outcomes:
        {json.dumps(po_list, indent=2)}

        Respond strictly in the following JSON format:

        {{
            "mapped_pos": [
                {{
                    "name": "Exact Program Outcome Name from DB",
                    "alignment_level": "Strong/Moderate",
                    "rationale": "Brief explanation of alignment"
                }}
            ]
        }}

        Instructions:
        - Select only relevant Program Outcomes from the provided list.
        - Use exact names from the database.
        - Ensure proper justification for alignment.
        - If no mapping exists, return an empty "mapped_pos" list.
        """

        try:
            # Generate mapping response
            response = model.generate_content(mapping_prompt)
            response_text = response.text.strip()

            # Extract valid JSON
            response_text = re.sub(r"```json\n?|```", "", response_text).strip()
            mapping_json = json.loads(response_text)

            # Validate and filter mapped POs
            mapped_pos = []
            for mapping in mapping_json.get("mapped_pos", []):
                po = ProgramOutcome.objects.filter(name=mapping["name"]).first()
                if po:
                    mapped_pos.append({
                        "po_name": po.name,
                        "po_description": po.description,  # Show full PO description
                        "alignment_level": mapping["alignment_level"],
                        "rationale": mapping["rationale"]
                    })
                else:
                    print(f"Warning: Program Outcome '{mapping['name']}' not found in DB.")

            # Generate justification **only if there are mapped POs**
            justification_text = ""
            if mapped_pos:
                justification_prompt = f"""
                Provide a **concise yet structured** academic justification for mapping:
                - **Course Outcome:** '{co_text}'
                - **Mapped Program Outcomes:** {', '.join([m['po_name'] for m in mapped_pos])}

                Guidelines:
                - Keep it **brief (5-7 sentences)** but informative.
                - Explain how the **CO aligns with the PO(s)**.
                - Justify the **alignment level** (Strong/Moderate).
                - Highlight **key knowledge/skills transferred**.

                Format the response **clearly** using bullet points.
                """

                justification_response = model.generate_content(justification_prompt)
                justification_text = justification_response.text.strip()

                # Improve formatting
                justification_text = re.sub(r"\n-", "\n•", justification_text)  # Convert `-` to `•`
                justification_text = re.sub(r"\n{2,}", "\n\n", justification_text)  # Fix spacing

            return render(request, "mapping_result.html", {
                "mapped_pos": mapped_pos,
                "justification": justification_text if mapped_pos else "No justification needed as no mapping was found.",
                "co_text": co_text
            })

        except (json.JSONDecodeError, KeyError):
            return render(request, "mapping_form.html", {
                "error": "Invalid response format received from AI. Try again."
            })

        except Exception as e:
            return render(request, "mapping_form.html", {
                "error": f"An error occurred: {str(e)}"
            })

    return render(request, "mapping_form.html")



import openai
import fitz  # PyMuPDF for PDF extraction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

openai.api_key = "AIzaSyArYroSmf7e1ZMLi9CY-ALNaAcg0igXEQs"  # Add your API key

def extract_syllabus(pdf_path):
    """Extracts text from syllabus PDF."""
    doc = fitz.open(pdf_path)
    syllabus_text = ""
    for page in doc:
        syllabus_text += page.get_text()
    return syllabus_text


from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('student_login')  # Redirect to login page after logout

def generate_questions(subject, difficulty, syllabus):
    """Generates AI-based questions using OpenAI API."""
    prompt = f"""
    Generate {5 if difficulty == 'easy' else 3 if difficulty == 'medium' else 2} questions for {subject}
    based on the following syllabus:

    {syllabus}

    Ensure questions align with Course Outcomes (CO) and are of {difficulty} difficulty.
    Provide structured questions with marks.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os
from django.core.files.storage import default_storage

from django.shortcuts import render

def question_paper_generator(request):
    return render(request, 'question_paper_form.html')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

@csrf_exempt
def generate_question_paper(request):
    if request.method == "POST":
        # Instead of getting the file from the user, use the file path directly
        syllabus_pdf_path = "/static/syllabus.pdf"  # Path to the PDF on your server

        subject = request.POST.get("subject")
        difficulty = request.POST.get("difficulty")

        if not syllabus_pdf_path:
            return JsonResponse({"error": "No PDF file found on server"}, status=400)

        # Simulate AI-based question generation (Replace this with actual logic)
        generated_questions = [
            f"Sample question 1 for {subject} ({difficulty})",
            f"Sample question 2 for {subject} ({difficulty})",
            f"Sample question 3 for {subject} ({difficulty})"
        ]

        return JsonResponse({"questions": generated_questions})

    return JsonResponse({"message": "Welcome to the Question Paper Generator API. Please use a POST request to generate questions."}, status=200)








import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods

# Configure Gemini
import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

def accreditation_checker(request):
    # Configure the API key securely (avoid hardcoding)
    genai.configure(api_key="AIzaSyArYroSmf7e1ZMLi9CY-ALNaAcg0igXEQs")  # Replace with environment variable

    if request.method == "POST":
        # Retrieve form data
        outcome_text = request.POST.get("outcome_text", "").strip()
        outcome_type = request.POST.get("outcome_type", "CO")
        standard_type = request.POST.get("standard_type", "NBA")

        # Validate input
        if not outcome_text:
            return JsonResponse({"error": "Please enter an outcome"}, status=400)

        try:
            # Initialize the generative model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Create a comprehensive prompt
            prompt = f"""
            Comprehensive Accreditation Alignment Analysis

            Objective: Evaluate {outcome_type} against {standard_type} Accreditation Standards

            Outcome Text: "{outcome_text}"

            Analysis Requirements:
            A. Alignment Assessment
            - Determine precise alignment level (Strong/Moderate/Weak/None)
            - Identify specific {standard_type} accreditation criteria matches
            - Provide detailed rationale for alignment evaluation

            B. Detailed Evaluation
            - Break down how each component of the outcome relates to standard criteria
            - Highlight potential strengths and weaknesses
            - Offer constructive improvement recommendations

            C. Comprehensive Insights
            - Provide actionable feedback
            - Suggest specific modifications to enhance accreditation potential
            - Maintain a professional, objective tone
            """

            # Generate content with error handling
            response = model.generate_content(prompt)
            
            # Return JSON response with analysis
            return JsonResponse({
                "status": "success",
                "analysis": response.text,
                "standard": standard_type,
                "outcome_type": outcome_type
            })

        except Exception as e:
            # Comprehensive error handling
            return JsonResponse({
                "error": f"Analysis generation failed: {str(e)}",
                "details": "Please check API configuration and input"
            }, status=500)

    # Render the template for GET requests
    return render(request, "simple_checker.html")