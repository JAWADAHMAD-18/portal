from django.shortcuts import render,get_object_or_404, redirect
from .models import Career,Teacher,Appointment,Feedback
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User



# Create your views here.
def wow(request):
    return render(request,'base.html')
def home(request):
    return render(request,'home.html')

def dashboard(request):
    return render(request,'dashboard.html')

'''def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(email=email)
            if student.password == password:
                request.session['student_id'] = student.id  
                return redirect('ass_index')  
            else:
                messages.error(request, "Incorrect password")
        except Student.DoesNotExist:
            messages.error(request, "Student not found with this email")

    return render(request, 'login.html')

def signup(request):
    if request.method=='POST':
        name=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        Student.objects.create(name=name, email=email, password=password)
        return redirect('login')
    
    return render(request,'signup.html')'''
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Signup successful. Please log in.")
            return redirect('login')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

@login_required
def career(request):
    if request.method == 'POST':
        if Career.objects.filter(student=request.user).exists():
            messages.warning(request, "You have already submitted your career report.")
            return redirect('ass_index')
        student=request.user
        name = request.POST.get('name')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        stream = request.POST.get('stream')

        subject1_name = request.POST.get('subject1_name')
        subject1_marks = request.POST.get('subject1_marks')
        subject2_name = request.POST.get('subject2_name')
        subject2_marks = request.POST.get('subject2_marks')
        subject3_name = request.POST.get('subject3_name')
        subject3_marks = request.POST.get('subject3_marks')
        subject4_name = request.POST.get('subject4_name')
        subject4_marks = request.POST.get('subject4_marks')
        subject5_name = request.POST.get('subject5_name')
        subject5_marks = request.POST.get('subject5_marks')

        intrest = request.POST.get('intrest')
        guidance = request.POST.get('guidance')

        try:
            Career.objects.create(
                student=student,
                name=name,
                age=age,
                sex=sex,
                stream=stream,
                subject1_name=subject1_name,
                subject1_marks=subject1_marks,
                subject2_name=subject2_name,
                subject2_marks=subject2_marks,
                subject3_name=subject3_name,
                subject3_marks=subject3_marks,
                subject4_name=subject4_name,
                subject4_marks=subject4_marks,
                subject5_name=subject5_name,
                subject5_marks=subject5_marks,
                intrest=intrest,
                guidance=guidance,
            )
            messages.success(request, "Form submitted successfully!")
            return redirect('teacher_list')  
        except Exception as e:
            messages.error(request, f"Error saving form: {e}")

    return render(request, 'assessment_index.html')  

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')
    
def teacher_list(request):
    teachers = User.objects.filter(is_staff=True)
    teachers = Teacher.objects.all()
    context={'teachers': teachers}
    return render(request, 'teachers.html', context)

def appointment(request,teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method=='POST':
        date=request.POST.get('date')
        time=request.POST.get('time')
        message=request.POST.get('message')
        new_appointment =Appointment.objects.create(student=request.user,teacher=teacher,time=time,date=date,message=message,status='pending')
        return redirect('appointment_confirmation', appointment_id=new_appointment.id)
    context={'teacher': teacher}
    return render(request, 'appointment.html',context)



@login_required
def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, student=request.user)
    return render(request, 'appointment_confirmation.html', {'appointment': appointment})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Appointment, Teacher

@login_required
def teacher_appointments(request):
    
    teacher = get_object_or_404(Teacher, user=request.user)
    appointments = Appointment.objects.filter(teacher=teacher).order_by('-date', '-time')
    return render(request, 'teacher_appointments.html', {'appointments': appointments})


@login_required
def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Debug print to confirm request.user and appointment.teacher
    print(f"Current user: {request.user}")
    print(f"Appointment teacher: {appointment.teacher.user}")

    if appointment.teacher.user == request.user:
        appointment.status = 'accepted'
        appointment.save()
        print("Appointment accepted successfully!")  # <-- Key debug line
    else:
        print("Unauthorized attempt to accept appointment!")

    return redirect('teacher_appointments')


  


@login_required
def student_dashboard(request):
    accepted_appointments = Appointment.objects.filter(student=request.user, status='accepted')
    context = {
        'accepted_appointments': accepted_appointments,
    }
    return render(request, 'dashboard.html', context)






def is_teacher_or_superuser(user):
    return user.is_superuser or hasattr(user, 'teacher')




@login_required
@user_passes_test(is_teacher_or_superuser)
def career_report_list(request):
    reports = Career.objects.all()
    return render(request, 'career_report_list.html', {'reports': reports})





@login_required
@user_passes_test(is_teacher_or_superuser)
def review_career_report(request, report_id):
    report = get_object_or_404(Career, id=report_id)
    if request.method == 'POST':
       guidance = request.POST.get('guidance')
       report.guidance = guidance
       report.save()

    subject_data = []
    for i in range(1, 6):
        subject_name = getattr(report, f'subject{i}_name')
        subject_marks = getattr(report, f'subject{i}_marks')
        subject_data.append((subject_name, subject_marks))

    if request.method == 'POST':
        guidance = request.POST.get('guidance')
        report.guidance = guidance
        report.save()
        messages.success(request, 'Guidance submitted successfully.')
        return redirect('career_report_list')

    return render(request, 'review_career.html', {
        'report': report,
        'subject_data': subject_data
    })

#for student to vieww feedback bhai
@login_required
def view_my_career_report(request):
    report = Career.objects.filter(student=request.user).first()
    context={'report': report}
    return render(request, 'student_view_report.html', context)


@login_required
def give_feedback(request,teacher_id):
    teacher=get_object_or_404(Teacher,id=teacher_id)
    if Feedback.objects.filter(student=request.user, teacher=teacher).exists():
        messages.warning(request, "You have already submitted feedback for this teacher.")
        return render(request, 'feedback.html', {'teacher': teacher})

    if request.method=='POST':
        rating=request.POST.get('rating')
        comments=request.POST.get('comments')
        Feedback.objects.create(student=request.user,rating=rating,teacher=teacher,comments=comments)
        messages.success(request,'your FeedBack has submitted Successfully Thankyou for your response')
        return redirect('dashboard')
    context={'teacher':teacher}
    return render(request,'feedback.html',context)

@login_required
@user_passes_test(is_teacher_or_superuser)
def view_feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})
