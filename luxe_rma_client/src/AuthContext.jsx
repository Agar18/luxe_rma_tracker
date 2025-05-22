import React, { createContext, useEffect, useState } from 'react';
import { jwtDecode } from 'jwt-decode';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState({
    token: null,
    userId: null,
    role: null,
    isLoggedIn: false
  });

  // On load, check localStorage
  useEffect(() => {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');

    if (token) {
      try {
        const decoded = jwtDecode(token);
        setAuth({
          token,
          userId,
          role: decoded.role,
          isLoggedIn: true
        });
      } catch (err) {
        localStorage.clear();
      }
    }
  }, []);

  const login = (token, userId) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user_id', userId);
    const decoded = jwtDecode(token);

    setAuth({
      token,
      userId,
      role: decoded.role,
      isLoggedIn: true
    });
  };

  const logout = () => {
    localStorage.clear();
    setAuth({
      token: null,
      userId: null,
      role: null,
      isLoggedIn: false
    });
  };

  return (
    <AuthContext.Provider value={{ ...auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
