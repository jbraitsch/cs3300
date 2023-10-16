from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Student, Portfolio

# Create your views here.
def index(request):
    student_active_portfolios = Student.objects.select_related('portfolio').all().filter(portfolio__is_active=True)
   # student_active_portfolios = student_active_portfolios.filter(is)
    print("active portfolio query set", student_active_portfolios)
    return render( request, 'portfolio_app/index.html', {'student_active_portfolios':student_active_portfolios})



class StudentListView(generic.ListView):
    model = Student
class StudentDetailView(generic.DetailView):
    model = Student
class PortfolioDetailView(generic.DetailView):
    model = Portfolio