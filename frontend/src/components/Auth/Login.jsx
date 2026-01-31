import React, { useState } from 'react';
import { authAPI } from '../../services/api';
import './Login.css';

function Login({ onLoginSuccess }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const data = await authAPI.login(username, password);

            // Store token and user info
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));

            onLoginSuccess(data.user);
        } catch (err) {
            setError(err.response?.data?.detail || 'Error al iniciar sesión');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h1>Task Manager</h1>
                    <p>Sistema de Gestión de Tareas</p>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    {error && <div className="error-message">{error}</div>}

                    <div className="form-group">
                        <label htmlFor="username">Usuario</label>
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Ingrese su usuario"
                            required
                            autoFocus
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Contraseña</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Ingrese su contraseña"
                            required
                        />
                    </div>

                    <button type="submit" className="btn-login" disabled={loading}>
                        {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
                    </button>
                </form>

                <div className="login-footer">
                    <p className="demo-credentials">
                        <strong>Usuarios demo:</strong><br />
                        admin / admin123 | user1 / user123 | user2 / user123
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Login;
