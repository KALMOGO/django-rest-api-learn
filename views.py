from django.shortcuts import render
from rest_framework.response import Response
from todos.serializers import QuotationSerializer, ActivitySerializer, TaskSerializer
from todos.models import quotations, Activity, Task
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import rest_framework.status as status
from rest_framework import generics, permissions, authentication

from .permissions import IsStaffUserPermission

from todosApp.authentication import TokenAuthentication

            ##################################

            # CRUD genericAPI, mixins        #

            ##################################

# ----------------------- Operations CRUD For Quotation --------------
class QuotationsDetailAPIView(generics.RetrieveAPIView):
    queryset = quotations.objects.all()
    serializer_class = QuotationSerializer

quotations_Detail_APIView = QuotationsDetailAPIView.as_view()

            
class ListCreateQuotations(generics.ListCreateAPIView):
    queryset= quotations.objects.all()
    serializer_class = QuotationSerializer
    permission_classes=[permissions.IsAdminUser, IsStaffUserPermission ] # order the permissions as you wanted to be checked
    
    #authentication system declare outside the setting file
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     TokenAuthentication
    #     ]
    
    def perform_create(self, serializer): # personalise the create obj method
        serializer.save(user=self.request.user) # add the required user for creating a quotation
        
list_create_quotationsAPIView = ListCreateQuotations.as_view()

        # Retrieve ,Update, Delete 
class QuotationsRetrUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = quotations.objects.all()
    serializer_class = QuotationSerializer
    lookup_field ='pk'
    
Quotations_Retr_Update_Delete = QuotationsRetrUpdateDeleteAPIView.as_view()

# ----------------------- Operations CRUD For Task --------------
class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    
Task_List_Create_APIView = TaskListCreateAPIView.as_view()

            # Retrieve ,Update, Delete 
class TaskRetrUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field ='pk'

Task_Retr_Update_Delete_APIView = TaskRetrUpdateDeleteAPIView.as_view()

# ----------------------- Operations CRUD For Task --------------
class ActivityListCreateAPIView(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    # copy the method from the ListCreateAPIView class to re-define them
    # the best way is to create your own Mixins View : more clear
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
    def get(self, request,*args, **kwargs): 
        return self.list(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        # personalize the return value as I want

        for value in serializer.data :
            value.pop("tasks")
        
        return Response(serializer.data)
    
    
Activity_List_Create_APIView = ActivityListCreateAPIView.as_view()

            # Retrieve ,Update, Delete 
class ActivityRetrUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    lookup_field ='pk'

    # copy the method from the RetrieveUpdateDestroyAPIView class to redefine them
    # the best way is to create your own Mixins View : more clear
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # personalize the return value as I want
        data = serializer.data
        data.pop("tasks")

        return Response(data)
    
Activity_Retr_Update_Destroy_APIView =ActivityRetrUpdateDestroyAPIView.as_view()


            ##################################
            # CRUD @api_view METHOD          #
            ##################################

@api_view(["GET", "POST", "DELETE", "PUT", "PATCH"])
def home(request, pk=None, *args, **kwargs):
    # sourcery skip: instance-method-first-arg-name
    """
        quotations:
            Supported Methods 
                GET     --> recuperation des objects de la bd
                POST    --> Creation des objects
                PUT     --> Mettre à jours tout l' object 
                PATCH   --> mise à jour de quelque attribut de l'objects
                DELETE  --> Suppression d'un object;
    """
    
    if request.method == 'GET':
        if pk is not None :
            qs= get_object_or_404(quotations, pk=pk)
            serialize = QuotationSerializer(qs, many=False)
            return Response(serialize.data, status=status.HTTP_200_0k)
        
        instance = quotations.objects.all()    
        data = QuotationSerializer(instance, many=True).data
        return Response(data, status=status.HTTP_200_OK)
        
    elif request.method == 'POST':

        serializer = QuotationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        data = get_object_or_404(quotations.objects.all(), pk=pk)
        data.delete()
        return Response({"delete sucessful !!"}, status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == "PUT":
        data = get_object_or_404(quotations.objects.all(), pk=pk)
        serializer = QuotationSerializer(data, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method=="PATCH":
        data = get_object_or_404(quotations.objects.all(), pk=pk)
        serializer = QuotationSerializer(data, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response({"invalid method"}, status=status.HTTP_BAD_REQUEST)

@api_view(["GET", "POST"])
def tasks_view(request, pk=None ,*args, **kwargs):
    """
        Task 
            Supported Methods 
                GET     --> recuperation des objects de la bd
                POST    --> Creation des objects
    """
    
    if request.method == 'GET' :
        if pk is not None :
            qs = get_object_or_404(Task, pk=pk)
            data = TaskSerializer(qs , many=False).data
            return Response(data, status=status.HTTP_200_OK)
        
        data = Task.objects.all()
        result = TaskSerializer(data, many=True).data
        return Response(result , status=status.HTTP_200_OK)
        
    if request.method == 'POST' :
        serialize = TaskSerializer(data=request.data)

        if serialize.is_valid(raise_exception=True) :
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        
    return Response(serialize.error, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
def activity_view(request, pk=None ,*args, **kwargs):
    """
        Activty
            Supported Methods
                GET     --> recuperation des objects de la bd
                POST    --> Creation des objects
                DELETE  --> Suppression d'un object;
    """
    if request.method == 'GET' :
        if pk is not None :
            instance = get_object_or_404(Activity,  pk=pk)
            serializer = ActivitySerializer(instance, many=False)
            data = serializer.data
            data.pop("tasks")
                
            return Response(data, status=status.HTTP_200_OK)
        
        data = Activity.objects.all()
        serialize = ActivitySerializer(data, many=True)
        for value in serialize.data :
            value.pop("tasks")
        return Response(serialize.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serialize = ActivitySerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            serialize.save(user=request.user)
            # data = serialize.data.pop("tasks")
            return Response({"sucessful now!!"}, status=status.HTTP_200_OK)
        
    elif request.method == "DELETE":
        data = get_object_or_404(Activity, pk=pk)
        data.delete()
        return Response({"sucessfuly !!! "}, status=status.HTTP_200_OK)
            
    return Response({"invalid method "}, status=status.HTTP_400_BAD_REQUEST)

