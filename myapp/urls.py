from django.contrib import admin
from django.urls import path
from myapp import views
from django.urls import path
from .views import outcome_tracking_dashboard, student_performance,generate_question_paper


urlpatterns = [
    path('',views.index,name='index'),
    path('student_login',views.student_login,name='student_login'),
        path('co_po_mapping',views.co_po_mapping,name='co_po_mapping'),
          path("tracking/", outcome_tracking_dashboard, name="tracking_dashboard"),
    path('student/<str:username>/performance/', student_performance, name='student_performance'),
        #   path("questionpaper/", views.questionpaper, name="questionpaper"),
              path('generate_question_paper/', generate_question_paper, name='generate_question_paper'),

    path('question-paper-generator/', views.question_paper_generator, name='question_paper_generator'),
    path('accreditation/', views.accreditation, name='accreditation'),
        path('syllabus/', views.syllabus, name='syllabus'),
                path('rubrics/', views.rubrics, name='rubrics'),
                  
 path('feedback/', views.feedback, name='feedback'),
    path('thank_you/', views.thank_you, name='thank_you'),  # Optional, for thank you page
path('logout/', views.logout_view, name='logout'),


    path('accreditation_checker', views.accreditation_checker, name='accreditation_checker'),

]


