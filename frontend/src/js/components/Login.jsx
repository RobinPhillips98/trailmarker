import { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext.jsx';

function Login() {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });

    const { login } = useContext(AuthContext);

    function handleChange(e) {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    function handleSubmit(e) {
        e.preventDefault();
        login(formData.username, formData.password);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="username" placeholder="Username" onChange={handleChange} />
            <input type="password" name="password" placeholder="Password" onChange={handleChange} />
            <button type="submit">Login</button>
        </form>
    );
};

export default Login;