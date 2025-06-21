// static/dashboard.js
document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar on mobile
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Task completion toggle
    const taskCheckboxes = document.querySelectorAll('.task-checkbox input');
    taskCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskTitle = this.closest('.task-item').querySelector('.task-title');
            if (this.checked) {
                taskTitle.classList.add('completed');
                // TODO: Mettre à jour la tâche dans Supabase
                // fetch('/api/tasks/update', { method: 'POST', body: JSON.stringify({ id: taskId, completed: true }) })
            } else {
                taskTitle.classList.remove('completed');
                // TODO: Mettre à jour la tâche dans Supabase
            }
        });
    });

    // Add new task
    const addTaskInput = document.querySelector('.add-task input');
    const addTaskBtn = document.querySelector('.btn-add-task');
    
    if (addTaskInput && addTaskBtn) {
        addTaskBtn.addEventListener('click', function() {
            const taskText = addTaskInput.value.trim();
            if (taskText) {
                const taskList = document.querySelector('.task-list');
                const newTask = document.createElement('div');
                newTask.className = 'task-item';
                newTask.innerHTML = `
                    <label class="task-checkbox">
                        <input type="checkbox">
                        <span class="checkmark"></span>
                    </label>
                    <div class="task-content">
                        <div class="task-title">${taskText}</div>
                        <div class="task-meta">
                            <span class="task-due">Aujourd'hui</span>
                            <span class="task-priority medium">Moyenne priorité</span>
                        </div>
                    </div>
                    <button class="task-menu"><i class="fas fa-ellipsis-v"></i></button>
                `;
                taskList.appendChild(newTask);
                addTaskInput.value = '';
                // TODO: Enregistrer la tâche dans Supabase
                // fetch('/api/tasks/add', { method: 'POST', body: JSON.stringify({ title: taskText, due_date: new Date().toISOString().split('T')[0], priority: 'medium' }) })
            }
        });

        addTaskInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addTaskBtn.click();
            }
        });
    }
});