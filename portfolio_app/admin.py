from django.contrib import admin
from .models import Student, Portfolio, Project#, ProjectsInPortfolio
# Register your models here.
admin.site.register(Student)
#admin.site.register(ProjectsInPortfolio)
admin.site.register(Project)
admin.site.register(Portfolio)