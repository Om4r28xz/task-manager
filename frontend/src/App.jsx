import React, { useState, useEffect, useRef } from 'react';
import Login from './components/Auth/Login';
import Header from './components/Layout/Header';
import Tabs from './components/Layout/Tabs';
import StatsPanel from './components/Stats/StatsPanel';
import { authAPI, tasksAPI, projectsAPI, reportsAPI, notificationsAPI, historyAPI, commentsAPI } from './services/api';
import './styles/App.css';
import { format } from 'date-fns';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [currentUser, setCurrentUser] = useState(null);
    const [activeTab, setActiveTab] = useState('tasks');
    const [tasks, setTasks] = useState([]);
    const [projects, setProjects] = useState([]);
    const [users, setUsers] = useState([]);
    const [stats, setStats] = useState(null);
    const [notifications, setNotifications] = useState([]);
    const [history, setHistory] = useState([]);
    const [comments, setComments] = useState([]);
    const [selectedTaskId, setSelectedTaskId] = useState(null);
    const [loading, setLoading] = useState(false);
    const [commentText, setCommentText] = useState('');

    // Task form state
    const [taskForm, setTaskForm] = useState({
        title: '',
        description: '',
        status: 'Pendiente',
        priority: 'Media',
        project_id: '',
        assigned_to: '',
        due_date: '',
        estimated_hours: '',
    });

    // Project form state
    const [projectForm, setProjectForm] = useState({
        name: '',
        description: '',
    });

    // Search filters
    const [searchFilters, setSearchFilters] = useState({
        text: '',
        status: '',
        priority: '',
        project_id: '',
    });

    // Check for existing authentication
    useEffect(() => {
        const token = localStorage.getItem('token');
        const user = localStorage.getItem('user');

        if (token && user) {
            setCurrentUser(JSON.parse(user));
            setIsAuthenticated(true);
        }
    }, []);

    // Load initial data when authenticated
    useEffect(() => {
        if (isAuthenticated) {
            loadInitialData();
        }
    }, [isAuthenticated]);

    const loadInitialData = async () => {
        await Promise.all([
            loadTasks(),
            loadProjects(),
            loadUsers(),
            loadStats(),
            loadNotifications(),
        ]);
    };

    const loadTasks = async () => {
        try {
            const data = await tasksAPI.getAll();
            setTasks(data);
        } catch (error) {
            console.error('Error loading tasks:', error);
        }
    };

    const loadProjects = async () => {
        try {
            const data = await projectsAPI.getAll();
            setProjects(data);
        } catch (error) {
            console.error('Error loading projects:', error);
        }
    };

    const loadUsers = async () => {
        try {
            const data = await reportsAPI.getUsers();
            setUsers(data);
        } catch (error) {
            console.error('Error loading users:', error);
        }
    };

    const loadStats = async () => {
        try {
            const data = await reportsAPI.getStats();
            setStats(data);
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    };

    const loadNotifications = async () => {
        try {
            const data = await notificationsAPI.getAll(true);
            setNotifications(data);
        } catch (error) {
            console.error('Error loading notifications:', error);
        }
    };

    const loadHistory = async (limit = 100) => {
        try {
            const data = await historyAPI.getAll(limit);
            setHistory(data);
        } catch (error) {
            console.error('Error loading history:', error);
        }
    };

    const loadComments = async (taskId) => {
        try {
            const data = await commentsAPI.getByTask(taskId);
            setComments(data);
        } catch (error) {
            console.error('Error loading comments:', error);
            setComments([]);
        }
    };

    const handleLogin = (user) => {
        setCurrentUser(user);
        setIsAuthenticated(true);
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setCurrentUser(null);
        setIsAuthenticated(false);
        setActiveTab('tasks');
    };

    const handleTaskFormChange = (field, value) => {
        setTaskForm({ ...taskForm, [field]: value });
    };

    const handleTaskSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const taskData = {
                ...taskForm,
                project_id: taskForm.project_id || null,
                assigned_to: taskForm.assigned_to || null,
                due_date: taskForm.due_date ? new Date(taskForm.due_date).toISOString() : null,
                estimated_hours: taskForm.estimated_hours ? parseFloat(taskForm.estimated_hours) : null,
            };

            if (selectedTaskId) {
                await tasksAPI.update(selectedTaskId, taskData);
            } else {
                await tasksAPI.create(taskData);
            }

            await loadTasks();
            await loadStats();
            clearTaskForm();
            alert(selectedTaskId ? 'Tarea actualizada exitosamente' : 'Tarea creada exitosamente');
        } catch (error) {
            alert('Error al guardar la tarea: ' + (error.response?.data?.detail || error.message));
        } finally {
            setLoading(false);
        }
    };

    const handleTaskDelete = async (taskId) => {
        if (!window.confirm('¿Está seguro de eliminar esta tarea?')) return;

        try {
            await tasksAPI.delete(taskId);
            await loadTasks();
            await loadStats();
            alert('Tarea eliminada exitosamente');
        } catch (error) {
            alert('Error al eliminar la tarea');
        }
    };

    const selectTask = (task) => {
        setTaskForm({
            title: task.title,
            description: task.description || '',
            status: task.status,
            priority: task.priority,
            project_id: task.project_id || '',
            assigned_to: task.assigned_to || '',
            due_date: task.due_date ? task.due_date.split('T')[0] : '',
            estimated_hours: task.estimated_hours || '',
        });
        setSelectedTaskId(task._id);
        loadComments(task._id);
    };

    const clearTaskForm = () => {
        setTaskForm({
            title: '',
            description: '',
            status: 'Pendiente',
            priority: 'Media',
            project_id: '',
            assigned_to: '',
            due_date: '',
            estimated_hours: '',
        });
        setSelectedTaskId(null);
        setComments([]);
        setCommentText('');
    };

    const handleProjectSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            await projectsAPI.create(projectForm);
            await loadProjects();
            setProjectForm({ name: '', description: '' });
            alert('Proyecto creado exitosamente');
        } catch (error) {
            alert('Error al crear el proyecto: ' + (error.response?.data?.detail || error.message));
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async () => {
        try {
            const data = await tasksAPI.search(searchFilters);
            setTasks(data);
        } catch (error) {
            console.error('Error searching tasks:', error);
        }
    };

    const clearSearchFilters = async () => {
        setSearchFilters({
            text: '',
            status: '',
            priority: '',
            project_id: '',
        });
        await loadTasks();
    };

    const handleAddComment = async (e) => {
        e.preventDefault();
        if (!commentText.trim() || !selectedTaskId) return;

        try {
            await commentsAPI.create({
                task_id: selectedTaskId,
                comment: commentText,
            });
            setCommentText('');
            await loadComments(selectedTaskId);
        } catch (error) {
            alert('Error al agregar comentario: ' + (error.response?.data?.detail || error.message));
        }
    };

    const markAllNotificationsRead = async () => {
        try {
            await notificationsAPI.markAllAsRead();
            await loadNotifications();
        } catch (error) {
            console.error('Error marking notifications as read:', error);
        }
    };

    // CSV Export function
    const exportToCSV = () => {
        if (tasks.length === 0) {
            alert('No hay tareas para exportar');
            return;
        }

        // Define CSV headers
        const headers = ['ID', 'Título', 'Estado', 'Prioridad', 'Proyecto', 'Asignado', 'Vencimiento', 'Horas Estimadas'];

        // Convert tasks to CSV rows
        const rows = tasks.map((task, index) => [
            index + 1,
            `"${task.title.replace(/"/g, '""')}"`,
            task.status,
            task.priority,
            task.project_name || '-',
            task.assigned_to_name || '-',
            task.due_date ? format(new Date(task.due_date), 'dd/MM/yyyy') : '-',
            task.estimated_hours || '-'
        ]);

        // Combine headers and rows
        const csvContent = [
            headers.join(','),
            ...rows.map(row => row.join(','))
        ].join('\n');

        // Create blob and download
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `tareas_${format(new Date(), 'yyyy-MM-dd')}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    // PDF Export function for reports
    const exportReportToPDF = () => {
        if (!stats) {
            alert('No hay datos de estadísticas para exportar');
            return;
        }

        const doc = new jsPDF();

        // Title
        doc.setFontSize(20);
        doc.text('Reporte del Sistema de Tareas', 14, 20);

        // Date
        doc.setFontSize(10);
        doc.text(`Generado: ${format(new Date(), 'dd/MM/yyyy HH:mm')}`, 14, 28);

        // Summary statistics
        doc.setFontSize(14);
        doc.text('Resumen de Estadísticas', 14, 40);

        doc.setFontSize(11);
        const summaryData = [
            ['Total de Tareas', stats.total_tasks || 0],
            ['Tareas Pendientes', stats.pending_tasks || 0],
            ['Tareas en Progreso', stats.in_progress_tasks || 0],
            ['Tareas Completadas', stats.completed_tasks || 0],
            ['Total de Proyectos', stats.total_projects || 0],
            ['Total de Usuarios', stats.total_users || 0]
        ];

        doc.autoTable({
            startY: 45,
            head: [['Métrica', 'Valor']],
            body: summaryData,
            theme: 'grid',
            headStyles: { fillColor: [102, 126, 234] }
        });

        // Tasks by priority
        if (stats.tasks_by_priority && stats.tasks_by_priority.length > 0) {
            doc.setFontSize(14);
            doc.text('Tareas por Prioridad', 14, doc.lastAutoTable.finalY + 15);

            const priorityData = stats.tasks_by_priority.map(item => [
                item._id || 'Sin definir',
                item.count
            ]);

            doc.autoTable({
                startY: doc.lastAutoTable.finalY + 20,
                head: [['Prioridad', 'Cantidad']],
                body: priorityData,
                theme: 'grid',
                headStyles: { fillColor: [102, 126, 234] }
            });
        }

        // Tasks by status
        if (stats.tasks_by_status && stats.tasks_by_status.length > 0) {
            doc.setFontSize(14);
            doc.text('Tareas por Estado', 14, doc.lastAutoTable.finalY + 15);

            const statusData = stats.tasks_by_status.map(item => [
                item._id || 'Sin definir',
                item.count
            ]);

            doc.autoTable({
                startY: doc.lastAutoTable.finalY + 20,
                head: [['Estado', 'Cantidad']],
                body: statusData,
                theme: 'grid',
                headStyles: { fillColor: [102, 126, 234] }
            });
        }

        // Save the PDF
        doc.save(`reporte_sistema_${format(new Date(), 'yyyy-MM-dd')}.pdf`);
    };

    // CSV Export function for reports
    const exportReportToCSV = () => {
        if (!stats) {
            alert('No hay datos de estadísticas para exportar');
            return;
        }

        const headers = ['Métrica', 'Valor'];
        const rows = [
            ['Total de Tareas', stats.total_tasks || 0],
            ['Tareas Pendientes', stats.pending_tasks || 0],
            ['Tareas en Progreso', stats.in_progress_tasks || 0],
            ['Tareas Completadas', stats.completed_tasks || 0],
            ['Total de Proyectos', stats.total_projects || 0],
            ['Total de Usuarios', stats.total_users || 0],
            ['', ''], // Empty row
            ['Prioridad', 'Cantidad']
        ];

        // Add priority data
        if (stats.tasks_by_priority && stats.tasks_by_priority.length > 0) {
            stats.tasks_by_priority.forEach(item => {
                rows.push([item._id || 'Sin definir', item.count]);
            });
        }

        rows.push(['', ''], ['Estado', 'Cantidad']);

        // Add status data
        if (stats.tasks_by_status && stats.tasks_by_status.length > 0) {
            stats.tasks_by_status.forEach(item => {
                rows.push([item._id || 'Sin definir', item.count]);
            });
        }

        const csvContent = [
            headers.join(','),
            ...rows.map(row => row.join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `reporte_sistema_${format(new Date(), 'yyyy-MM-dd')}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    if (!isAuthenticated) {
        return <Login onLoginSuccess={handleLogin} />;
    }

    return (
        <div className="app">
            <Header user={currentUser} onLogout={handleLogout} />
            <Tabs activeTab={activeTab} onTabChange={setActiveTab} />

            <main className="main-content">
                <div className="container">
                    {activeTab === 'tasks' && (
                        <div className="tab-content">
                            <StatsPanel stats={stats} />

                            <div className="section-card">
                                <h2>{selectedTaskId ? 'Editar Tarea' : 'Nueva Tarea'}</h2>
                                <form onSubmit={handleTaskSubmit} className="task-form">
                                    <div className="form-row">
                                        <div className="form-group">
                                            <label htmlFor="title">Título *</label>
                                            <input
                                                id="title"
                                                type="text"
                                                value={taskForm.title}
                                                onChange={(e) => handleTaskFormChange('title', e.target.value)}
                                                required
                                            />
                                        </div>
                                    </div>

                                    <div className="form-row">
                                        <div className="form-group">
                                            <label htmlFor="description">Descripción</label>
                                            <textarea
                                                id="description"
                                                value={taskForm.description}
                                                onChange={(e) => handleTaskFormChange('description', e.target.value)}
                                                rows="3"
                                            />
                                        </div>
                                    </div>

                                    <div className="form-row">
                                        <div className="form-group">
                                            <label htmlFor="status">Estado</label>
                                            <select
                                                id="status"
                                                value={taskForm.status}
                                                onChange={(e) => handleTaskFormChange('status', e.target.value)}
                                            >
                                                <option value="Pendiente">Pendiente</option>
                                                <option value="En Progreso">En Progreso</option>
                                                <option value="Completada">Completada</option>
                                            </select>
                                        </div>

                                        <div className="form-group">
                                            <label htmlFor="priority">Prioridad</label>
                                            <select
                                                id="priority"
                                                value={taskForm.priority}
                                                onChange={(e) => handleTaskFormChange('priority', e.target.value)}
                                            >
                                                <option value="Baja">Baja</option>
                                                <option value="Media">Media</option>
                                                <option value="Alta">Alta</option>
                                                <option value="Crítica">Crítica</option>
                                            </select>
                                        </div>
                                    </div>

                                    <div className="form-row">
                                        <div className="form-group">
                                            <label htmlFor="project">Proyecto</label>
                                            <select
                                                id="project"
                                                value={taskForm.project_id}
                                                onChange={(e) => handleTaskFormChange('project_id', e.target.value)}
                                            >
                                                <option value="">Sin asignar</option>
                                                {projects.map((p) => (
                                                    <option key={p._id} value={p._id}>{p.name}</option>
                                                ))}
                                            </select>
                                        </div>

                                        <div className="form-group">
                                            <label htmlFor="assigned">Asignado a</label>
                                            <select
                                                id="assigned"
                                                value={taskForm.assigned_to}
                                                onChange={(e) => handleTaskFormChange('assigned_to', e.target.value)}
                                            >
                                                <option value="">Sin asignar</option>
                                                {users.map((u) => (
                                                    <option key={u.id} value={u.id}>{u.username}</option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>

                                    <div className="form-row">
                                        <div className="form-group">
                                            <label htmlFor="due_date">Fecha de vencimiento</label>
                                            <input
                                                id="due_date"
                                                type="date"
                                                value={taskForm.due_date}
                                                onChange={(e) => handleTaskFormChange('due_date', e.target.value)}
                                            />
                                        </div>

                                        <div className="form-group">
                                            <label htmlFor="hours">Horas estimadas</label>
                                            <input
                                                id="hours"
                                                type="number"
                                                step="0.5"
                                                value={taskForm.estimated_hours}
                                                onChange={(e) => handleTaskFormChange('estimated_hours', e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="form-actions">
                                        <button type="submit" className="btn btn-primary" disabled={loading}>
                                            {selectedTaskId ? 'Actualizar' : 'Agregar'}
                                        </button>
                                        <button type="button" className="btn btn-secondary" onClick={clearTaskForm}>
                                            Limpiar
                                        </button>
                                    </div>
                                </form>
                            </div>

                            {selectedTaskId && (
                                <div className="section-card">
                                    <h2>Comentarios</h2>
                                    <div className="comments-section">
                                        <div className="comments-list">
                                            {comments.length === 0 ? (
                                                <p className="empty-message" style={{ padding: '20px' }}>No hay comentarios aún</p>
                                            ) : (
                                                comments.map((comment) => (
                                                    <div key={comment._id} className="comment-item">
                                                        <div className="comment-header">
                                                            <strong>{comment.username}</strong>
                                                            <span className="comment-time">
                                                                {format(new Date(comment.created_at), 'dd/MM/yyyy HH:mm')}
                                                            </span>
                                                        </div>
                                                        <div className="comment-text">{comment.comment}</div>
                                                    </div>
                                                ))
                                            )}
                                        </div>
                                        <form onSubmit={handleAddComment} className="comment-form">
                                            <textarea
                                                value={commentText}
                                                onChange={(e) => setCommentText(e.target.value)}
                                                placeholder="Escribe un comentario..."
                                                rows="3"
                                                style={{ width: '100%' }}
                                            />
                                            <button type="submit" className="btn btn-primary" style={{ marginTop: '10px' }}>
                                                Agregar Comentario
                                            </button>
                                        </form>
                                    </div>
                                </div>
                            )}

                            <div className="section-card">
                                <h2>Búsqueda de Tareas</h2>
                                <div className="search-filters">
                                    <div className="form-row">
                                        <div className="form-group">
                                            <label htmlFor="searchText">Buscar por texto</label>
                                            <input
                                                id="searchText"
                                                type="text"
                                                value={searchFilters.text}
                                                onChange={(e) => setSearchFilters({ ...searchFilters, text: e.target.value })}
                                                placeholder="Título o descripción..."
                                            />
                                        </div>
                                        <div className="form-group">
                                            <label htmlFor="searchStatus">Estado</label>
                                            <select
                                                id="searchStatus"
                                                value={searchFilters.status}
                                                onChange={(e) => setSearchFilters({ ...searchFilters, status: e.target.value })}
                                            >
                                                <option value="">Todos</option>
                                                <option value="Pendiente">Pendiente</option>
                                                <option value="En Progreso">En Progreso</option>
                                                <option value="Completada">Completada</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div className="form-row">
                                        <div className="form-group">
                                            <label htmlFor="searchPriority">Prioridad</label>
                                            <select
                                                id="searchPriority"
                                                value={searchFilters.priority}
                                                onChange={(e) => setSearchFilters({ ...searchFilters, priority: e.target.value })}
                                            >
                                                <option value="">Todas</option>
                                                <option value="Baja">Baja</option>
                                                <option value="Media">Media</option>
                                                <option value="Alta">Alta</option>
                                                <option value="Crítica">Crítica</option>
                                            </select>
                                        </div>
                                        <div className="form-group">
                                            <label htmlFor="searchProject">Proyecto</label>
                                            <select
                                                id="searchProject"
                                                value={searchFilters.project_id}
                                                onChange={(e) => setSearchFilters({ ...searchFilters, project_id: e.target.value })}
                                            >
                                                <option value="">Todos</option>
                                                {projects.map((p) => (
                                                    <option key={p._id} value={p._id}>{p.name}</option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>
                                    <div className="form-actions">
                                        <button type="button" className="btn btn-primary" onClick={handleSearch}>
                                            🔍 Buscar
                                        </button>
                                        <button type="button" className="btn btn-secondary" onClick={clearSearchFilters}>
                                            ✖ Limpiar Filtros
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div className="section-card">
                                <div className="section-header">
                                    <h2>Lista de Tareas</h2>
                                    <button className="btn btn-secondary" onClick={exportToCSV}>
                                        📊 Exportar CSV
                                    </button>
                                </div>
                                <div className="table-container">
                                    <table className="data-table" id="tasksTable">
                                        <thead>
                                            <tr>
                                                <th>ID</th>
                                                <th>Título</th>
                                                <th>Estado</th>
                                                <th>Prioridad</th>
                                                <th>Proyecto</th>
                                                <th>Asignado</th>
                                                <th>Vencimiento</th>
                                                <th>Acciones</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {tasks.map((task, index) => (
                                                <tr key={task._id}> <td>{index + 1}</td>
                                                    <td>{task.title}</td>
                                                    <td><span className={`badge badge-${task.status.toLowerCase().replace(' ', '-')}`}>{task.status}</span></td>
                                                    <td><span className={`badge badge-${task.priority.toLowerCase()}`}>{task.priority}</span></td>
                                                    <td>{task.project_name || '-'}</td>
                                                    <td>{task.assigned_to_name || '-'}</td>
                                                    <td>{task.due_date ? format(new Date(task.due_date), 'dd/MM/yyyy') : '-'}</td>
                                                    <td>
                                                        <button className="btn-icon" onClick={() => selectTask(task)} title="Editar">✏️</button>
                                                        <button className="btn-icon" onClick={() => handleTaskDelete(task._id)} title="Eliminar">🗑️</button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'projects' && (
                        <div className="tab-content">
                            <div className="section-card">
                                <h2>Nuevo Proyecto</h2>
                                <form onSubmit={handleProjectSubmit} className="project-form">
                                    <div className="form-group">
                                        <label htmlFor="projectName">Nombre *</label>
                                        <input
                                            id="projectName"
                                            type="text"
                                            value={projectForm.name}
                                            onChange={(e) => setProjectForm({ ...projectForm, name: e.target.value })}
                                            required
                                        />
                                    </div>

                                    <div className="form-group">
                                        <label htmlFor="projectDesc">Descripción</label>
                                        <textarea
                                            id="projectDesc"
                                            value={projectForm.description}
                                            onChange={(e) => setProjectForm({ ...projectForm, description: e.target.value })}
                                            rows="3"
                                        />
                                    </div>

                                    <button type="submit" className="btn btn-primary" disabled={loading}>
                                        Crear Proyecto
                                    </button>
                                </form>
                            </div>

                            <div className="section-card">
                                <h2>Lista de Proyectos</h2>
                                <div className="projects-grid">
                                    {projects.map((project) => (
                                        <div key={project._id} className="project-card">
                                            <h3>{project.name}</h3>
                                            <p>{project.description || 'Sin descripción'}</p>
                                            <small>Creado: {format(new Date(project.created_at), 'dd/MM/yyyy')}</small>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'notifications' && (
                        <div className="tab-content">
                            <div className="section-card">
                                <div className="section-header">
                                    <h2>Notificaciones ({notifications.length})</h2>
                                    {notifications.length > 0 && (
                                        <button className="btn btn-secondary" onClick={markAllNotificationsRead}>
                                            Marcar todas como leídas
                                        </button>
                                    )}
                                </div>

                                <div className="notifications-list">
                                    {notifications.length === 0 ? (
                                        <p className="empty-message">No tienes notificaciones nuevas</p>
                                    ) : (
                                        notifications.map((notif) => (
                                            <div key={notif._id} className="notification-item">
                                                <div className="notification-content">{notif.message}</div>
                                                <div className="notification-time">
                                                    {format(new Date(notif.created_at), 'dd/MM/yyyy HH:mm')}
                                                </div>
                                            </div>
                                        ))
                                    )}
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'history' && (
                        <div className="tab-content">
                            <div className="section-card">
                                <h2>Historial de Cambios</h2>
                                <button className="btn btn-secondary" onClick={() => loadHistory()} style={{ marginBottom: '20px' }}>
                                    Cargar Historial
                                </button>

                                <div className="history-list">
                                    {history.map((entry) => (
                                        <div key={entry._id} className="history-entry">
                                            <div className="history-action">
                                                <span className={`badge badge-${entry.action.toLowerCase()}`}>{entry.action}</span>
                                            </div>
                                            <div className="history-details">
                                                <strong>{entry.username}</strong>
                                                {entry.old_value && entry.new_value && (
                                                    <span> cambió de "{entry.old_value}" a "{entry.new_value}"</span>
                                                )}
                                                {entry.new_value && !entry.old_value && (
                                                    <span>: {entry.new_value}</span>
                                                )}
                                            </div>
                                            <div className="history-time">
                                                {format(new Date(entry.timestamp), 'dd/MM/yyyy HH:mm')}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'reports' && (
                        <div className="tab-content">
                            <StatsPanel stats={stats} />
                            <div className="section-card">
                                <div className="section-header">
                                    <h2>Exportar Reportes</h2>
                                </div>
                                <p className="note-text">
                                    Exporta las estadísticas del sistema en formato PDF o CSV para análisis externo.
                                </p>
                                <div className="form-actions" style={{ marginTop: '20px' }}>
                                    <button className="btn btn-primary" onClick={exportReportToPDF}>
                                        📄 Exportar a PDF
                                    </button>
                                    <button className="btn btn-secondary" onClick={exportReportToCSV}>
                                        📊 Exportar a CSV
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default App;
