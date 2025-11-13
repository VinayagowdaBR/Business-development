import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Login from './components/Login';
import Register from './components/Register';
import MainLayout from './components/layout/MainLayout';
import DashboardPage from './pages/DashboardPage';
import RoleManagement from './pages/RoleManagement';
import OrganizationDashboard from './components/OrganizationDashboard';
import ProtectedRoute from './components/ProtectedRoute';
import MembersList from './pages/MembersList'; 

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected Routes with Layout */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <DashboardPage />
                </MainLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/users"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <OrganizationDashboard />
                </MainLayout>
              </ProtectedRoute>
            }
          />
          {/* ADD THIS ROUTE FOR /users/roles */}
          <Route
            path="/users/roles"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <RoleManagement />
                </MainLayout>
              </ProtectedRoute>
            }
          />

           <Route
            path="/members"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <MembersList />
                </MainLayout>
              </ProtectedRoute>
            }
          />



          <Route
            path="/roles"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <RoleManagement />
                </MainLayout>
              </ProtectedRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
