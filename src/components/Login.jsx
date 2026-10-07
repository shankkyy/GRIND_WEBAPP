import { useState } from 'react';
import { authAPI } from '../api/client';
import { useStore } from '../stores/useStore';
import './Login.css';

const Login = () => {
  const setUser = useStore((state) => state.setUser);
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isRegister = mode === 'register';

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const response = isRegister
        ? await authAPI.register(email, username, password)
        : await authAPI.login(email, password);
      const { access_token, user_id, username: savedUsername } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_id', user_id);
      localStorage.setItem('username', savedUsername);
      setUser({
        id: user_id,
        username: savedUsername,
        email,
        level: 1,
        totalXp: 0,
        emeralds: 0,
        streakDays: 0,
      });
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string') {
        setError(detail);
      } else if (Array.isArray(detail)) {
        setError(detail.map((item) => item.msg).join(' '));
      } else {
        setError('Could not sign in. Check your details and try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="login-screen">
      <form className="login-card" onSubmit={handleSubmit}>
        <h1>GRIND</h1>
        <p>{isRegister ? 'Create an account' : 'Sign in to continue'}</p>

        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />

        {isRegister && (
          <>
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              autoComplete="username"
              minLength={3}
              maxLength={20}
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
            />
          </>
        )}

        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          autoComplete={isRegister ? 'new-password' : 'current-password'}
          minLength={isRegister ? 8 : undefined}
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
        />

        {error && <p className="login-error" role="alert">{error}</p>}

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Please wait' : isRegister ? 'Create account' : 'Log in'}
        </button>

        <button
          type="button"
          className="login-switch"
          onClick={() => {
            setMode(isRegister ? 'login' : 'register');
            setError('');
          }}
        >
          {isRegister ? 'Back to log in' : 'Register'}
        </button>
      </form>
    </main>
  );
};

export default Login;
