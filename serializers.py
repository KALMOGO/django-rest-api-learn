from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Activity, Task, quotations

from .validators import validate_name, unique_activity_name

from todosApp.serializersRelatedField import UserPublicSerializer

class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = (
            'id',
            'activity',
            'name',
            'state',
            'starting_date',
            'creating_date',
            'ending_date',
            'rest_of_day',
            'rest_of_month'
        )
        

class ActivitySerializer(serializers.ModelSerializer):
    
    tasks = TaskSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    task_num = serializers.SerializerMethodField()
    name = serializers.CharField(validators=[validate_name])
    class Meta:
        model = Activity
        fields= (
            'id',
            'name',
            'creating_date',
            'user',
            'task_num',
            'tasks',
            'id_subactivity'
            )
        
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.creating_date = validated_data.get('creating_date', instance.creating_date)
        isntance.save()
        
        return instance
    
    def get_task_num(self, obj):
        return 0 if len(obj.tasks.values_list()) == 0 else len(obj.tasks.values_list()) 




class QuotationSerializer(serializers.ModelSerializer):
    # related serializer
        #  data_field_user = serializers.SerializerMethodField(read_only=True)
    # read_only=True as a parameter because all his field will be read_only
    owner = UserPublicSerializer(source="user",read_only=True)

    class Meta:
        model = quotations
        fields=(
            'id',
            'owner',
            'quotation',
            'author',
            #'data_field_user'
        )
        
    # method to get access to the foreign key data: Not the recommended the method: Use a related serializer
    # def get_data_field_user(self, obj):
    #     return {
    #         "username":obj.user.username
    #     }


