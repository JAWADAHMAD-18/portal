from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specification=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='teacher_pics/', blank=True, null=True)





class Career(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    STREAM_CHOICES = [
        ('Science', 'Science'),
        ('Commerce', 'Commerce'),
        ('Humanities', 'Humanities'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    
    stream = models.CharField(max_length=20, choices=STREAM_CHOICES)

    subject1_name = models.CharField(max_length=100, blank=True, null=True)
    subject1_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    subject2_name = models.CharField(max_length=100, blank=True, null=True)
    subject2_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    subject3_name = models.CharField(max_length=100, blank=True, null=True)
    subject3_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    subject4_name = models.CharField(max_length=100, blank=True, null=True)
    subject4_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    subject5_name = models.CharField(max_length=100, blank=True, null=True)
    subject5_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    intrest = models.TextField()
    guidance = models.TextField(blank=True, null=True)




class Appointment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True,null=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.student.name} -> {self.teacher.user.first_name} on {self.date} at {self.time}"


class Feedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} → {self.teacher.name} (Rating: {self.rating})"