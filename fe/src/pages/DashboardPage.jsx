import React from 'react';
import { useAuth } from '../context/AuthContext';

const DashboardPage = () => {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Sistema de Autenticación - Flask
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">
                Bienvenido, {user?.username}
              </span>
              <button
                onClick={handleLogout}
                className="btn-secondary">
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Información del Usuario */}
            <div className="card">
              <h2 className="text-lg font-medium text-gray-900 mb-4">
                Información del Usuario
              </h2>
              <div className="space-y-3">
                <div>
                  <span className="text-sm font-medium text-gray-500">ID:</span>
                  <p className="text-gray-900">{user?.id}</p>
                </div>
                <div>
                  <span className="text-sm font-medium text-gray-500">
                    Nombre de Usuario:
                  </span>
                  <p className="text-gray-900">{user?.username}</p>
                </div>
                <div>
                  <span className="text-sm font-medium text-gray-500">
                    Email:
                  </span>
                  <p className="text-gray-900">{user?.email}</p>
                </div>
                <div>
                  <span className="text-sm font-medium text-gray-500">
                    Fecha de Registro:
                  </span>
                  <p className="text-gray-900">
                    {user?.created_at
                      ? new Date(user.created_at).toLocaleDateString('es-ES')
                      : 'N/A'}
                  </p>
                </div>
              </div>
            </div>

            {/* Información del Sistema */}
            <div className="card">
              <h2 className="text-lg font-medium text-gray-900 mb-4">
                Estado del Sistema
              </h2>
              <div className="space-y-3">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                  <span className="text-gray-900">
                    Backend Flask: Conectado
                  </span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                  <span className="text-gray-900">Base de Datos: SQLite</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                  <span className="text-gray-900">Autenticación: JWT</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                  <span className="text-gray-900">Frontend: React + Vite</span>
                </div>
              </div>
            </div>

            {/* Funcionalidades */}
            <div className="card md:col-span-2">
              <h2 className="text-lg font-medium text-gray-900 mb-4">
                Funcionalidades Implementadas
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <h3 className="font-medium text-gray-700">Backend (Flask)</h3>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>✅ Registro de usuarios</li>
                    <li>✅ Autenticación con JWT</li>
                    <li>✅ Validación de datos</li>
                    <li>✅ Middleware de autenticación</li>
                    <li>✅ Base de datos SQLite</li>
                    <li>✅ Encriptación de contraseñas</li>
                    <li>✅ CORS configurado</li>
                  </ul>
                </div>
                <div className="space-y-2">
                  <h3 className="font-medium text-gray-700">
                    Frontend (React)
                  </h3>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>✅ Interfaz responsive</li>
                    <li>✅ Rutas protegidas</li>
                    <li>✅ Manejo de estado global</li>
                    <li>✅ Validación de formularios</li>
                    <li>✅ Persistencia de sesión</li>
                    <li>✅ Diseño con Tailwind CSS</li>
                    <li>✅ Componentes reutilizables</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;
