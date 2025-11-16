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
import AreaLegionPage from './pages/AreaLegionPage';
import MembershipFeesPage from './pages/MembershipFeesPage';
import MemberTypesPage from './pages/MemberTypesPage';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Dashboard */}
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

          {/* Areas & Legions */}
          <Route
            path="/areas-legions"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <AreaLegionPage />
                </MainLayout>
              </ProtectedRoute>
            }
          />

          {/* Membership Fees - FIXED: Only one route */}
          <Route
            path="/membership-fees"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <MembershipFeesPage />
                </MainLayout>
              </ProtectedRoute>
            }
          />

          {/* Users */}
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

          {/* Roles Management */}
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

          {/* Members */}
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
            path="/member-types"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <MemberTypesPage />
                </MainLayout>
              </ProtectedRoute>
            }
          />







          {/* Legacy Roles Route */}
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
