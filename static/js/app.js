class TaskManager {
    constructor() {
        this.apiBase = '/tasks'; // Используем префикс из роутера
        this.init();
    }

    async init() {
        this.bindEvents();
        await this.loadTasks();
    }

    bindEvents() {
        document.getElementById('taskForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTask();
        });
    }

    async addTask() {
        const name = document.getElementById('taskName').value;
        const description = document.getElementById('taskDescription').value;

        try {
            const response = await fetch('${this.apiBase}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, description })
            });

            if (response.ok) {
                const result = await response.json();
                // В вашем API POST возвращает {"ok": true, "task_id": id}
                if (result.ok) {
                    document.getElementById('taskName').value = '';
            document.getElementById('taskDescription').value = '';
            await this.loadTasks(); // Загружаем полный список задач
                } else {
                    alert('Ошибка при добавлении задачи');
                }
            } else {
                const errorData = await response.json();
                alert(`Ошибка при добавлении задачи: ${errorData.detail || 'Неизвестная ошибка'}`);
            }
        } catch (error) {
            console.error('Error adding task:', error);
            alert('Ошибка сети при добавлении задачи');
        }
    }

    async loadTasks() {
        try {
            const response = await fetch(this.apiBase);
            if (!response.ok) throw new Error('Network response was not ok');
            const tasks = await response.json();
            this.renderTasks(tasks);
        } catch (error) {
            console.error('Error loading tasks:', error);
            document.getElementById('tasksContainer').innerHTML =
                '<p>Ошибка загрузки задач</p>';
        }
    }

    renderTasks(tasks) {
        const container = document.getElementById('tasksContainer');
        container.innerHTML = '';

        if (tasks.length === 0) {
            container.innerHTML = '<p>Задач пока нет</p>';
            return;
        }

        tasks.forEach(task => {
            const taskElement = this.createTaskElement(task);
            container.appendChild(taskElement);
        });
    }

    createTaskElement(task) {
        const div = document.createElement('div');
        div.className = `task-item ${task.is_completed ? 'completed' : ''}`;

        div.innerHTML = `
            <div class="task-content">
                <div class="task-name">${task.name}</div>
                ${task.description ? `<div class="task-description">${task.description}</div>` : ''}
            </div>
            <div class="task-actions">
                ${!task.is_completed ?
                    `<button onclick="taskManager.completeTask(${task.id})">Завершить</button>` :
                    ''}
                <button onclick="taskManager.deleteTask(${task.id})">Удалить</button>
            </div>
        `;

        return div;
    }

    // Метод завершения задачи
    async completeTask(taskId) {
        try {
            const response = await fetch(`${this.apiBase}/${taskId}/complete`, {
                method: 'PUT'
            });

            if (response.ok) {
                await this.loadTasks(); // Обновляем список задач
            } else if (response.status === 404) {
                alert('Задача не найдена');
            } else {
                const errorData = await response.json();
                alert(`Ошибка при завершении задачи: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error completing task:', error);
            alert('Ошибка сети при завершении задачи');
        }
    }

    // Метод удаления задачи
    async deleteTask(taskId) {
        try {
            // Поскольку в вашем API нет DELETE, используем GET для получения задачи
            // и затем удаляем её через отдельный эндпоинт (если есть)
            // Либо имитируем удаление локально после подтверждения
            const confirmDelete = confirm('Вы уверены, что хотите удалить эту задачу?');
            if (!confirmDelete) return;

            // В текущей реализации API нет эндпоинта DELETE — нужно добавить его в роутер
            alert('Функция удаления пока не реализована в API');
            // Здесь можно добавить запрос к новому эндпоинту DELETE /tasks/{id}
        } catch (error) {
            console.error('Error deleting task:', error);
            alert('Ошибка сети при удалении задачи');
        }
    }
}

// Инициализация приложения после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('taskForm');
    const tasksContainer = document.getElementById('tasksContainer');

    taskForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const taskName = document.getElementById('taskName').value;
        const taskDescription = document.getElementById('taskDescription').value;

        try {
            const response = await fetch('/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: taskName,
            description: taskDescription || null
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Задача создана:', result);

            // Обновляем список задач
            loadTasks();

            // Очищаем форму
            taskForm.reset();
        } catch (error) {
            console.error('Ошибка при добавлении задачи:', error);
            alert('Ошибка при добавлении задачи');
        }
    });

    async function loadTasks() {
        try {
            const response = await fetch('/tasks');
            console.log(response)
            const data = await response.json();
            console.log(data)

            //tasksContainer.innerHTML = '';
            data.forEach(task => {
                const taskElement = document.createElement('div');
                taskElement.className = 'task-item';
                taskElement.innerHTML = `
                    <h3>${task.name}</h3>
                    ${task.description ? `<p>${task.description}</p>` : ''}
            `;
                tasksContainer.appendChild(taskElement);
            });
        } catch (error) {
            console.error('Ошибка загрузки задач:', error);
        }
    }

    // Загружаем задачи при загрузке страницы
    loadTasks();
});