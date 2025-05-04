from django.shortcuts import render, redirect, get_object_or_404
from .models import Problem, Application,Category
from .forms import ProblemForm, ApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db.models import Q
from django.http import HttpResponseForbidden

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('problem_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def problem_list(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    problems = Problem.objects.filter(is_resolved=False)
    
    if category_id:
        problems = problems.filter(category_id=category_id)
    
    if search_query:
        problems = problems.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    categories = Category.objects.all()
    return render(request, 'problem_list.html', {
        'problems': problems,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'search_query': search_query or ''
    })

@login_required
def my_orders(request):
    my_problems = Problem.objects.filter(user=request.user)    
    my_applications = Application.objects.filter(user=request.user)
    
    return render(request, 'my_orders.html', {
        'my_problems': my_problems,
        'my_applications': my_applications
    })
@login_required
def problem_create(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user = request.user
            problem.save()
            return redirect('problem_list')
    else:
        form = ProblemForm()
    return render(request, 'problem_form.html', {'form': form})

@login_required
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    applications = problem.applications.all()
    form = ApplicationForm()
    return render(request, 'problem_detail.html', {
        'problem': problem,
        'applications': applications,
        'form': form,
        'request': request  
    })
@login_required
def application_create(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.problem = problem
            application.save()
            return redirect('problem_detail', pk=pk)
    return redirect('problem_detail', pk=pk)

@login_required
def application_accept(request, pk, app_id):
    application = get_object_or_404(Application, pk=app_id, problem__pk=pk, problem__user=request.user)
    application.is_accepted = True
    application.problem.is_resolved = True
    application.problem.save()
    application.save()
    return redirect('problem_detail', pk=pk)
@login_required
def problem_edit(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if not problem.can_edit(request.user):
        return HttpResponseForbidden("У вас нет прав на редактирование этой проблемы")
    
    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            return redirect('problem_detail', pk=pk)
    else:
        form = ProblemForm(instance=problem)
    
    return render(request, 'problem_form.html', {'form': form})

@login_required
def problem_delete(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    
    if not (request.user == problem.user and not problem.is_resolved):
        return HttpResponseForbidden("У вас нет прав на удаление этой проблемы")
    
    if request.method == 'POST':
        problem.delete()
        return redirect('problem_list')
    
    return render(request, 'confirm_delete.html', {
        'object': problem,
        'message': 'Вы уверены, что хотите удалить эту проблему?'
    })
@login_required
def application_edit(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    if not application.can_edit(request.user):
        return HttpResponseForbidden("У вас нет прав на редактирование этой заявки")
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('problem_detail', pk=application.problem.pk)
    else:
        form = ApplicationForm(instance=application)
    
    return render(request, 'application_form.html', {'form': form})

@login_required
def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    if not application.can_edit(request.user):
        return HttpResponseForbidden("У вас нет прав на удаление этой заявки")
    
    if request.method == 'POST':
        problem_pk = application.problem.pk
        application.delete()
        return redirect('problem_detail', pk=problem_pk)
    
    return render(request, 'confirm_delete.html', {
        'object': application,
        'message': 'Вы уверены, что хотите удалить эту заявку?'
    })