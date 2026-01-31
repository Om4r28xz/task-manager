import React from 'react';
import './StatsPanel.css';

function StatsPanel({ stats }) {
    if (!stats) return null;

    const statItems = [
        { label: 'Total', value: stats.total, color: '#667eea' },
        { label: 'Completadas', value: stats.completed, color: '#48bb78' },
        { label: 'Pendientes', value: stats.pending, color: '#ed8936' },
        { label: 'En Progreso', value: stats.in_progress, color: '#4299e1' },
        { label: 'Alta Prioridad', value: stats.high_priority, color: '#f56565' },
        { label: 'Vencidas', value: stats.overdue, color: '#e53e3e' },
    ];

    return (
        <div className="stats-panel">
            <h3>Estadísticas</h3>
            <div className="stats-grid">
                {statItems.map((item, index) => (
                    <div key={index} className="stat-card" style={{ borderColor: item.color }}>
                        <div className="stat-value" style={{ color: item.color }}>
                            {item.value}
                        </div>
                        <div className="stat-label">{item.label}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default StatsPanel;
