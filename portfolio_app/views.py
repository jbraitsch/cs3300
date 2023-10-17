from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Student, Portfolio, Project
from .forms import ProjectForm
from django.contrib import messages

# Create your views here.
def index(request):
    student_active_portfolios = Student.objects.select_related('portfolio').all().filter(portfolio__is_active=True)
    print("active portfolio query set", student_active_portfolios)
    return render( request, 'portfolio_app/index.html', {'student_active_portfolios':student_active_portfolios})



class StudentListView(generic.ListView):
    model = Student
class StudentDetailView(generic.DetailView):
    model = Student
class PortfolioDetailView(generic.DetailView):
    model = Portfolio

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the p
        context["project_list"] = self.object.project_set.all()
        return context
class ProjectDetailView(generic.DetailView):
    model = Project


def createProject(request, portfolio_id):
    form = ProjectForm()
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    
    if request.method == 'POST':
        # Create a new dictionary with form data and portfolio_id
        project_data = request.POST.copy()
        project_data['portfolio_id'] = portfolio_id
        
        form = ProjectForm(project_data)
        if form.is_valid():
            # Save the form without committing to the database
            project = form.save(commit=False)
            # Set the portfolio relationship
            project.portfolio = portfolio
            project.save()

            # Redirect back to the portfolio detail page
            return redirect('portfolio-detail', portfolio_id)

    context = {'form': form}
    return render(request, 'portfolio_app/project_form.html', context)

def deleteProject(request, portfolio_id, project_id):
    project = Project.objects.get(pk=project_id)
    context = {'project': project}
    if request.method == 'GET':
        return render(request, 'portfolio_app/project_delete.html',context)       
    elif request.method == 'POST':
        project.delete()
        return redirect('portfolio-detail', portfolio_id)

def updateProject(request, portfolio_id, project_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    project = Project.objects.get(pk=project_id)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project.save()

            # Redirect back to the portfolio detail page
            return redirect('portfolio-detail', portfolio_id)
    else:
        context = {'form': form}
        return render(request, 'portfolio_app/project_form.html', context)   
