import React, { useState } from 'react';
import './login.css';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Aquí iría la lógica de autenticación
        console.log('Email:', email);
        console.log('Password:', password);
    };

    return (
        <div className="login-container">
            <h1>Iniciar Sesión</h1>
            <p>Para comenzar, inicia sesión desde aquí.</p>

            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    id="email"
                    placeholder="ejemplo@gmail.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                
                <label htmlFor="password">Contraseña</label>
                <input
                    type="password"
                    id="password"
                    placeholder="**********"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <a href="resert_password.html" className="forgot-password">Olvidaste tu contraseña?</a>

                <button type="submit">Iniciar sesión</button>
            </form>

            <p>No tienes una cuenta? <a href="register.html" className="create-account">Crea una cuenta</a></p>
        </div>
    );
};

export default Login;
