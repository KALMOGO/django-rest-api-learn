# validators could to : model, serializers ...

# serializer: it can be write inside the serializer himself
#               
from rest_framework import serializers
from rest_framework import validators # model that contain several vailidors that can be immediatly use
                                    # UniqueValidators, UniqueTogtherValidators ....
from .models import Activity

# check if the activity name is unique
def validate_name(value): # utilisation:  name = TypeField(validators=[validate_name]) dans le serilaizer
    qs = Activity.objects.filter(name__iexact=value)
    if qs.exists() :
        raise serializers.ValidationError(f"{value} is already an activity name")
    return value

# check if the activity name is unique with classes inside the validors model
unique_activity_name = validators.UniqueValidator(Activity.objects.all())