from django.shortcuts import render
from django.http import HttpResponse
from .models import student, subjects
from .cor import generate_cor
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime

allstudents = student.objects.all()
number_of_students_enrolled = student.objects.all().count()

def admin_profile(request):
    return render(request, "admin_dashboard/profile.html",{})
def admin_masterlist(request):
    return render(request, "admin_dashboard/masterlist.html",{'allstudents':allstudents})
def admin_schedule(request):
    return render(request, "admin_dashboard/schedule.html",{})
def admin_enrollment(request):
    return render(request, "admin_dashboard/student-enrollment.html",{})
def admin_checklist(request):
    return render(request, "admin_dashboard/checklist.html",{})

def new_or_old_enrollee_view(request):
    return render(request, "admin_dashboard/new_or_old_enrollee.html",{})

def new_enrollee_view(request):
    return render(request, "admin_dashboard/new_student_enrollment.html",{})

def old_enrollee_view(request):
    return render(request, "admin_dashboard/old_student_enrollment.html",{})


def enroll_new_student(request):

    if request.method == 'POST':
        
        allstudents = student.objects.all().count()
        intyear = datetime.date.today().year
        year = str(intyear)
        result = int(allstudents)

        student_number = "{:05d}".format(result)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        Dateofbirth = request.POST.get('dob')
        Gender = request.POST.get('gender')
        contact_info = request.POST.get('contactNumber')
        email = request.POST.get('email')
        address = request.POST.get('Address')
        Sectionyear = request.POST.get('year_standing')

        match(Sectionyear):
            case "1":
                studentyear = '1st Year'
            case "2":
                studentyear = '2nd Year'
            case "3":
                studentyear = '3rd Year'
            case "4":
                studentyear = '4th Year'
            case _:
                return HttpResponse("Please enter 1 to 4 in year standing")

        Section = request.POST.get('section')
        Course = request.POST.get('course')
        Major = request.POST.get('major')
        Suffix = request.POST.get('suffix')
        Status = request.POST.get('status')
        studenttype = 'New'

        
        student_info = student(

            studentnumber = year + student_number,
            firstname = first_name, 
            lastname = last_name,
            middlename = middle_name,
            dateofbirth = Dateofbirth,
            gender = Gender,
            suffix = Suffix,
            contact = contact_info,
            email = email,
            address = address,
            year = studentyear,
            sectionyear = Sectionyear,
            section = Section,
            course = Course,
            major = Major,
            status = Status,
            new_or_old = studenttype 
            )
        student_info.save()

        return HttpResponse("Enrolled Successfully!")
    else:
        return HttpResponse("Invalid request method.")
    

def enroll_old_student(request):

    if request.method == 'POST':

        student_number = request.POST.get('studentnumber')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        Dateofbirth = request.POST.get('dob')
        Gender = request.POST.get('gender')
        contact_info = request.POST.get('contactNumber')
        email = request.POST.get('email')
        address = request.POST.get('Address')
        Sectionyear = request.POST.get('year_standing')

        match(Sectionyear):
            case "1":
                studentyear = '1st Year'
            case "2":
                studentyear = '2nd Year'
            case "3":
                studentyear = '3rd Year'
            case "4":
                studentyear = '4th Year'
            case _:
                return HttpResponse("Please enter 1 to 4 in year standing")

        Section = request.POST.get('section')
        Course = request.POST.get('course')
        Major = request.POST.get('major')
        Suffix = request.POST.get('suffix')
        Status = request.POST.get('status')
        studenttype = 'Old'

        
        student_info = student(

            studentnumber = student_number,
            firstname = first_name, 
            lastname = last_name,
            middlename = middle_name,
            dateofbirth = Dateofbirth,
            gender = Gender,
            suffix = Suffix,
            contact = contact_info,
            email = email,
            address = address,
            year = studentyear,
            sectionyear = Sectionyear,
            section = Section,
            course = Course,
            major = Major,
            status = Status,
            new_or_old = studenttype 
            )
        student_info.save()

        return HttpResponse("Enrolled Successfully!")
    else:
        return HttpResponse("Invalid request method.")

def search_students(request):

    if request.method == 'POST':

        search_year = request.POST.get('year_filter')
        search_course = request.POST.get('course_filter')
        search_student_id = request.POST.get('search_student_number')

        template = get_template('admin_dashboard/search_results.html')

        search_results = student.objects.filter(year=search_year).values() | student.objects.filter(course=search_course).values() | student.objects.filter(studentnumber=search_student_id).values()
        
        context = {
        'allstudents': allstudents,
        'search_results': search_results
        }

        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("Not Found")

def process_cor(request, student_number):

    template = get_template('admin_dashboard/process_cor.html')
    enrolled_student = student.objects.get(studentnumber=student_number)
    subject_code = subjects.objects.order_by('course_code')
    current_school_year = datetime.date.today().year
    previous_school_year = datetime.date.today().year - 1
    next_school_year = datetime.date.today().year + 1

    context = {
        'enrolled_student': enrolled_student,
        'subject_codes':subject_code,
        'current_SY':current_school_year,
        'previous_SY':previous_school_year,
        'next_SY':next_school_year,
    }

    return HttpResponse(template.render(context, request))


def edit_info(request, student_number):

    template = get_template('admin_dashboard/edit_student_info.html')
    enrolled_student = student.objects.get(studentnumber=student_number)
    context = {
        'enrolled_student':enrolled_student
    }
    return HttpResponse(template.render(context, request))


def update_info(request, student_number):

    template = get_template("admin_dashboard/masterlist.html")

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    middle_name = request.POST['middle_name']
    Gender = request.POST['gender']
    contact_info = request.POST['contactNumber']
    email = request.POST['email']
    address = request.POST['Address']
    Sectionyear = request.POST['year_standing']

    match(Sectionyear):
            case "1":
                studentyear = '1st Year'
            case "2":
                studentyear = '2nd Year'
            case "3":
                studentyear = '3rd Year'
            case "4":
                studentyear = '4th Year'
            case _:
                return HttpResponse("Please enter 1 to 4 in year standing")
        
    Section = request.POST['section']
    Course = request.POST['course']
    Major = request.POST['major']
    Suffix = request.POST['suffix']
    Status = request.POST['status']
    studenttype = request.POST['studentType']

    student.objects.filter(studentnumber=student_number).update(
        firstname = first_name, 
        lastname = last_name,
        middlename = middle_name,
        gender = Gender,
        suffix = Suffix,
        contact = contact_info,
        email = email,
        address = address,
        year = studentyear,
        sectionyear = Sectionyear,
        section = Section,
        course = Course,
        major = Major,
        status = Status,
        new_or_old = studenttype
        
    )
    context = {}

    return HttpResponse(template.render(context, request))

def print_cor(request, student_number):
        
        if request.method == 'POST':
        
            enrolled_student = student.objects.filter(studentnumber = student_number)
            semester = request.POST.get('semester')
            yearstanding = request.POST.get('yearstanding')
            section = request.POST.get('section')
            yearlevel = request.POST.get('yearlevel')
            old_new = request.POST.get('old/new')
            status = request.POST.get('status')
            date_enrolled = datetime.date.today()

            subject1 = request.POST.get('subject1')
            subject2 = request.POST.get('subject2')
            subject3 = request.POST.get('subject3')
            subject4 = request.POST.get('subject4')
            subject5 = request.POST.get('subject5')
            subject6 = request.POST.get('subject6')
            subject7 = request.POST.get('subject7')
            subject8 = request.POST.get('subject8')
            subject9 = request.POST.get('subject9')
            subject10 = request.POST.get('subject10')

            context = {
                'enrolled_student': enrolled_student,
                'semester': semester,
                'yearstanding': yearstanding,
                'section': section,
                'yearlevel': yearlevel,
                'old_new': old_new,
                'status': status,
                'date_enrolled': date_enrolled,

                'subject1': subjects.objects.filter(course_code=subject1).values(),
                'subject2': subjects.objects.filter(course_code=subject2).values(),
                'subject3': subjects.objects.filter(course_code=subject3).values(),
                'subject4': subjects.objects.filter(course_code=subject4).values(),
                'subject5': subjects.objects.filter(course_code=subject5).values(),
                'subject6': subjects.objects.filter(course_code=subject6).values(),
                'subject7': subjects.objects.filter(course_code=subject7).values(),
                'subject8': subjects.objects.filter(course_code=subject8).values(),
                'subject9': subjects.objects.filter(course_code=subject9).values(),
                'subject10': subjects.objects.filter(course_code=subject10).values(),

                'allsubjects': ['subject1', 'subject2', 'subject3', 'subject4', 'subject5', 'subject6', 'subject7', 'subject8', 'subject9', 'subject10']

            }

            cor = generate_cor('admin_dashboard/cor_template.html', context)

            return HttpResponse(cor, content_type='application/pdf')

