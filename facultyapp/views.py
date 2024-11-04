from django.shortcuts import render, redirect
from .forms import AddCourseForm
from django.contrib.auth.decorators import login_required
from .models import AddCourse


@login_required
def FacultyHomePage(request):
    return render(request, 'facultyapp/FacultyHomePage.html')


from django.shortcuts import render, redirect
from .forms import AddCourseForm


def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facultyapp:FacultyHomePage')
    else:
        form = AddCourseForm()

    return render(request, 'facultyapp/add_course.html', {'form': form})


from django.shortcuts import render
from .models import AddCourse
from adminapp.models import StudentList  # Ensure this import is correct

def view_student_list(request):
    course = request.GET.get('course')
    section = request.GET.get('section')

    student_courses = AddCourse.objects.all()
    if course:
        student_courses = student_courses.filter(course=course)
    if section:
        student_courses = student_courses.filter(section=section)

    # Fetch students based on filtered courses
    students = StudentList.objects.filter(id__in=student_courses.values('student_id'))

    context = {
        'students': students,
        'course_choices': AddCourse.COURSE_CHOICES,
        'section_choices': AddCourse.SECTION_CHOICES,
        'selected_course': course,
        'selected_section': section,
    }

    return render(request, 'facultyapp/view_student_list.html', context)


from django.core.mail import send_mail
from django.contrib.auth.models import User  # Assuming User is your custom user model
from .models import StudentList
from .forms import MarksForm


from django.core.mail import send_mail
from django.shortcuts import render
from .forms import MarksForm

def post_marks(request):
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks_instance = form.save(commit=False)
            marks_instance.save()

            # Retrieve the User email based on the student in the form
            student = marks_instance.student
            student_user = getattr(student, 'user', None)  # Get user or None if not available

            if student_user and student_user.email:  # Check if student_user and email exist
                user_email = student_user.email

                subject = 'Marks Entered'
                message = f'Hello, {student_user.first_name}, marks for {marks_instance.course} have been entered. Marks: {marks_instance.marks}'
                from_email = 'ch1.durgarao@gmail.com'
                recipient_list = [user_email]

                send_mail(subject, message, from_email, recipient_list)

            return render(request, 'facultyapp/marks_success.html')
    else:
        form = MarksForm()
    return render(request, 'facultyapp/post_marks.html', {'form': form})
