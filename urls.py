from django.urls import path
from . import views

urlpatterns = [
    
        #Activity --- url
    path('activities/', views.Activity_List_Create_APIView, name='list_create_activities'),
    path('activities/<int:pk>', views.Activity_Retr_Update_Destroy_APIView, name='activities_pk'),
    
        #quotations --- url
    path('quotations/<int:pk>', views.Quotations_Retr_Update_Delete, name='quotation_pk'),
    path('quotations/', views.list_create_quotationsAPIView, name='list_create_quotation'),
    
        #Tasks --- url
    path('tasks/<int:pk>', views.Task_Retr_Update_Delete_APIView, name='task_pk'),
    path('tasks/', views.Task_List_Create_APIView, name='list_create_tasks'),
    
        #--->@api_view path --
    #path('tasks/', views.tasks_view, name='tasks'),
    #path('quotations/<int:pk>', views.quotations_Detail_APIView, name='detail_quotation'),
    #path('tasks/<int:pk>', views.tasks_view, name='task_detail'),
    #path('activities/<int:pk>', views.activity_view, name='delate'),
    #path('activities/', views.activity_view, name='activities'),
    
]