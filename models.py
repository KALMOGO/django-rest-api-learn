from django.db import models
import django.db.models.constraints as _
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError
# Create your models here.


class Activity(models.Model):
    id_subactivity = models.ForeignKey("self", on_delete=models.CASCADE, null=True,  blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    creating_date = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        ordering = ['name', '-creating_date'] # ordonner les activites par ordre alp et par date le plus recent

    def __str__(self):
        return self.name
    


class Task(models.Model):
    name = models.CharField(max_length=250, unique=True)
    state = models.BooleanField(default=False)
    starting_date = models.DateTimeField()
    creating_date = models.DateTimeField(auto_now_add=True)

    activity = models.ForeignKey(
            Activity, 
            verbose_name=("activite"),
            related_name="tasks",
            on_delete=models.CASCADE
        )

    ending_date = models.DateTimeField()

    class Meta:
        ordering = ['name','creating_date']
        constraints = [
            _.UniqueConstraint(fields=['id', 'activity'], name='unique_id_activity'),
            
            _.CheckConstraint(
                check = models.Q(starting_date__gte=datetime.now()) ,
                name='ck_starting_date'
                )
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if(self.starting_date <= self.ending_date):
            super(Task, self).save(*args, **kwargs )

        else:
            message = " Erreur de chronologie"
            raise ValidationError(message)

    @property
    def rest_of_day(self):
        return (self.ending_date - self.creating_date).days

    @property
    def rest_of_month(self):
        return (self.ending_date.month - self.creating_date.month)


### making a search ------------------------------->

class QuoteQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
    
    def search(self, query, user=None):
        lookup = models.Q(author__icontains=query) | models.Q(quotation__icontains=query)
        qs = self.is_public().filter(lookup) # insure that data that we are searching is public

        if user is not None :
            qs = qs.filter(user=user)
        return qs
    
class QuoteManager(models.Manager):
    """
        class for implementing search operations
    """
    
    def get_queryset(self, *args, **kwargs):
        
        print(self._db)
        return QuoteQuerySet(self.model, using=self._db)
    
    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)
    

# --------------------------------------------------->
class quotations(models.Model): 

    quotation = models.TextField(unique=True, null=True, blank=True)
    author = models.CharField(max_length=250, null=True)
    creating_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        User, verbose_name=("user"),
        related_name='quotations' ,
        on_delete=models.CASCADE
        )
    public = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-creating_date']
    
