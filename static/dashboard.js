// dashboard.js (version mise à jour)
document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.querySelector('.sidebar').classList.toggle('collapsed');
        });
    }

    // Gestion des tâches
    const taskList = document.querySelector('.task-list');
    const addTaskInput = document.querySelector('.add-task input');
    const addTaskBtn = document.querySelector('.btn-add-task');

    // Ajouter une tâche
    if (addTaskBtn && addTaskInput) {
        addTaskBtn.addEventListener('click', addTask);
        addTaskInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') addTask();
        });
    }

    async function addTask() {
        const title = addTaskInput.value.trim();
        if (!title) return;

        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title })
            });
            
            if (response.ok) {
                const task = await response.json();
                renderTask(task);
                addTaskInput.value = '';
            }
        } catch (error) {
            console.error('Erreur:', error);
        }
    }

    function renderTask(task) {
        const taskItem = document.createElement('div');
        taskItem.className = 'task-item';
        taskItem.dataset.id = task.id;
        taskItem.innerHTML = `
            <label class="task-checkbox">
                <input type="checkbox" ${task.completed ? 'checked' : ''}>
                <span class="checkmark"></span>
            </label>
            <div class="task-content">
                <div class="task-title ${task.completed ? 'completed' : ''}">${task.title}</div>
                <div class="task-meta">
                    <span class="task-due">${task.due_date}</span>
                    <span class="task-priority ${task.priority}">${task.priority} priorité</span>
                </div>
            </div>
            <button class="task-menu"><i class="fas fa-ellipsis-v"></i></button>
        `;
        
        if (taskList) {
            taskList.appendChild(taskItem);
            taskItem.querySelector('input').addEventListener('change', toggleTask);
        }
    }

    async function toggleTask(e) {
        const taskId = e.target.closest('.task-item').dataset.id;
        const completed = e.target.checked;
        
        try {
            await fetch(`/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ completed })
            });
            
            e.target.closest('.task-item').querySelector('.task-title').classList.toggle('completed');
        } catch (error) {
            console.error('Erreur:', error);
        }
    }
});