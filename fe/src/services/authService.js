/**
 * 🎓 SERVICIO DE AUTENTICACIÓN - GUÍA EDUCATIVA REACT
 *
 * Este archivo centraliza todas las peticiones HTTP relacionadas con autenticación.
 * Usar un servicio separado tiene varias ventajas:
 *
 * 1. SEPARACIÓN DE RESPONSABILIDADES:
 *    - Los componentes se enfocan en la UI
 *    - La lógica de API está centralizada
 *    - Fácil mantenimiento y testing
 *
 * 2. REUTILIZACIÓN:
 *    - Múltiples componentes pueden usar las mismas funciones
 *    - Evita duplicación de código
 *
 * 3. CONFIGURACIÓN CENTRALIZADA:
 *    - URLs base, headers, interceptors en un solo lugar
 *    - Manejo consistente de errores
 *
 * DIFERENCIAS CON EXPRESS.JS BACKEND:
 * - Cliente HTTP (axios) vs servidor HTTP (Flask)
 * - Variables de entorno con VITE_ prefix
 * - Interceptors para agregar tokens automáticamente
 * - Redirección automática en errores 401
 */

import axios from 'axios';

// 🌐 CONFIGURACIÓN DE LA API
// VITE_API_URL se define en .env y apunta al backend Flask
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// 🔧 CREAR INSTANCIA DE AXIOS CONFIGURADA
// Esto nos permite tener configuración base para todas las peticiones
const api = axios.create({
  baseURL: API_URL, // URL base para todas las peticiones
  headers: {
    'Content-Type': 'application/json', // Todas las peticiones envían JSON
  },
});

// 🔐 INTERCEPTOR DE REQUEST - AGREGAR TOKEN AUTOMÁTICAMENTE
// Este interceptor se ejecuta ANTES de cada petición HTTP
api.interceptors.request.use(
  (config) => {
    // 🎫 OBTENER TOKEN DEL LOCALSTORAGE
    const token = localStorage.getItem('token');
    if (token) {
      // 📋 AGREGAR HEADER DE AUTORIZACIÓN
      // Formato: "Authorization: Bearer <jwt-token>"
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // ❌ MANEJAR ERRORES DE CONFIGURACIÓN
    return Promise.reject(error);
  }
);

// 🔄 INTERCEPTOR DE RESPONSE - MANEJAR ERRORES GLOBALMENTE
// Este interceptor se ejecuta DESPUÉS de cada respuesta HTTP
api.interceptors.response.use(
  (response) => response, // ✅ Si la respuesta es exitosa, la devuelve tal como está
  (error) => {
    // 🚫 MANEJAR ERROR 401 (Token inválido/expirado)
    if (error.response?.status === 401) {
      // 🧹 LIMPIAR TOKEN INVÁLIDO
      localStorage.removeItem('token');
      // 🔄 REDIRECCIONAR AL LOGIN
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 📝 OBJETO SERVICIO DE AUTENTICACIÓN
// Agrupa todas las funciones relacionadas con autenticación
const authService = {
  /**
   * 🔐 LOGIN DE USUARIO
   *
   * Autentica un usuario con email y contraseña.
   *
   * @param {string} email - Email del usuario
   * @param {string} password - Contraseña del usuario
   * @returns {Promise} Promesa con los datos del usuario y token
   */
  async login(email, password) {
    try {
      // 📡 PETICIÓN POST AL ENDPOINT DE LOGIN
      const response = await api.post('/auth/login', { email, password });
      return response.data; // Retorna: { user, token, message }
    } catch (error) {
      // 🚫 PROPAGAR ERROR PARA MANEJO EN COMPONENTE
      throw error;
    }
  },

  /**
   * 📝 REGISTRO DE USUARIO
   *
   * Crea una nueva cuenta de usuario.
   *
   * @param {Object} userData - Datos del nuevo usuario
   * @param {string} userData.username - Nombre de usuario
   * @param {string} userData.email - Email del usuario
   * @param {string} userData.password - Contraseña del usuario
   * @returns {Promise} Promesa con los datos del usuario registrado
   */
  async register(userData) {
    try {
      // 📡 PETICIÓN POST AL ENDPOINT DE REGISTRO
      const response = await api.post('/auth/register', userData);
      return response.data; // Retorna: { user, token, message }
    } catch (error) {
      throw error;
    }
  },

  /**
   * 👤 OBTENER PERFIL DEL USUARIO
   *
   * Obtiene los datos del usuario autenticado.
   * Requiere token JWT en el header (agregado automáticamente por interceptor).
   *
   * @returns {Promise} Promesa con los datos del usuario
   */
  async getProfile() {
    try {
      // 📡 PETICIÓN GET AL ENDPOINT DE PERFIL (PROTEGIDO)
      const response = await api.get('/auth/profile');
      return response.data.user; // Retorna solo los datos del usuario
    } catch (error) {
      throw error;
    }
  },

  /**
   * 🚪 LOGOUT DE USUARIO
   *
   * En Flask con JWT no necesitamos endpoint específico de logout
   * ya que los tokens son stateless (no se almacenan en el servidor).
   * El logout se maneja completamente en el frontend.
   *
   * @returns {Promise} Promesa resuelta (no hace petición HTTP)
   */
  async logout() {
    // 🧹 LOGOUT LOCAL - NO REQUIERE PETICIÓN AL SERVIDOR
    // Con JWT stateless, simplemente eliminamos el token del cliente
    return Promise.resolve();
  },
};

export default authService;
