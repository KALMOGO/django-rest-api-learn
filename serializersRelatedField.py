# FOR GETTING access to the related field model value between two related model
# For example and quatations: best method

from rest_framework import serializers
# from todos.serializers import ActivitySerializer circular importation 
# serializer for getting access to a User data inside a related modal
# the Serialization is possible because the fields name included 
# within the serializer exist in the model

class ActivityInlineSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    id   = serializers.IntegerField(read_only=True)

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    activities_user = serializers.SerializerMethodField(read_only=True)
    
    def get_activities_user(self, obj):
        user = obj
        # easy way to get foreign key data like obj.objects.all()
        # can juste retrieve some line of the data with : user.activity_set.all()[:5] 
        activies_qs = user.activity_set.all() 
        # need to serialize the data before retrieve them
            #data = ActivitySerializer(activies_qs, many=True).data : No due to a circular import error
        data = ActivityInlineSerializer(activies_qs, many=True).data
        
        return data
    