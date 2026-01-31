import React from 'react';
import './Tabs.css';

function Tabs({ activeTab, onTabChange }) {
    const tabs = [
        { id: 'tasks', label: 'Tareas' },
        { id: 'projects', label: 'Proyectos' },
        { id: 'comments', label: 'Comentarios' },
        { id: 'history', label: 'Historial' },
        { id: 'notifications', label: 'Notificaciones' },
        { id: 'search', label: 'Búsqueda' },
        { id: 'reports', label: 'Reportes' },
    ];

    return (
        <div className="tabs-container">
            <div className="tabs">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        className={`tab ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => onTabChange(tab.id)}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>
        </div>
    );
}

export default Tabs;
