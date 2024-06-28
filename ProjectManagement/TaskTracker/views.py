from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm, TaskForm

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('projects:project_detail')
    else:
        form = ProjectForm()
    return render(request, 'project_create.html', {'form': form})

@login_required(login_url='/login/')
def project_detail(request):
    projects = Project.objects.all()
    project_tasks = {project: Task.objects.filter(project=project) for project in projects}


    return render(request, 'project_detail.html', {'project': projects,'task':project_tasks})

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects:project_detail')
    return render(request, 'project_update.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST': 
        project.delete()
        return redirect('projects:project_detail')
    return render(request, 'project_confirm_delete.html', {'project': project})

@login_required
def task_list(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=project.id)
    members = project.members.all()

    return render(request, 'task_list.html', {'tasks': tasks, 'project': project,'members':members})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_detail.html', {'task': task})

@login_required
def create_task(request, project_id):
    header = 'Create New Task'
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project  # Associate task with the project
            task.save()
            return redirect('projects:task_list', id=project.id)
    else:
        form = TaskForm(project=project)
    
    context = {
        'form': form,
        'project': project,
        'header': header
    }
    return render(request, 'task_form.html', context)


@login_required
def update_task(request, pk):
    header = 'Update Task'
    task = get_object_or_404(Task, pk=pk)
    project = task.project  # Get the project associated with the task

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task, project=project)
        if form.is_valid():
            form.save()
            return redirect('projects:task_detail', pk=pk)
    else:
        form = TaskForm(instance=task, project=project)  
    
    context = {
        'form': form,
        'task': task,
        'header': header
    }
    return render(request, 'task_form.html', context)


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        project_id = task.project.id  
        task.delete()
        return redirect('projects:task_list', id=project_id)
    return render(request, 'task_confirm_delete.html', {'task': task})



