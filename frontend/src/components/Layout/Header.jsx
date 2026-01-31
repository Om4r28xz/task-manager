import React from 'react';
import './Header.css';

function Header({ user, onLogout }) {
    return (
        <header className="app-header">
            <div className="header-content">
                <div className="header-title">
                    <h1>Task Manager</h1>
                </div>

                <div className="header-user">
                    <span className="user-info">
                        <span className="user-label">Usuario:</span>
                        <span className="user-name">{user.username}</span>
                    </span>
                    <button onClick={onLogout} className="btn-logout">
                        Salir
                    </button>
                </div>
            </div>
        </header>
    );
}

export default Header;
