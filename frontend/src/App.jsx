import React, { useState, useEffect } from 'react';
import Login from './components/Auth/Login';
import Header from './components/Layout/Header';
import Tabs from './components/Layout/Tabs';
import StatsPanel from './components/Stats/StatsPanel';
import { authAPI, tasksAPI, projectsAPI, reportsAPI, notificationsAPI, historyAPI, commentsAPI } from './services/api';
import './styles/App.css';
import { format } from 'date-fns';

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

    const markAllNotificationsRead = async () => {
        try {
            await notificationsAPI.markAllAsRead();
            await loadNotifications();
        } catch (error) {
            console.error('Error marking notifications as read:', error);
        }
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

                            <div className="section-card">
                                <h2>Lista de Tareas</h2>
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
                                <h2>Reportes del Sistema</h2>
                                <p className="note-text">
                                    Las tablas de tareas incluyen funcionalidad de exportación a PDF, CSV y Excel usando DataTables.
                                    Regresa a la pestaña "Tareas" para usar los botones de exportación.
                                </p>
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default App;
