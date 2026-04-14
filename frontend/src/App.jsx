import React, { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { Analytics } from '@vercel/analytics/react';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import ResumeBuilder from './pages/ResumeBuilder';
import ResumeView from './pages/ResumeView';
import Templates from './pages/Templates';
import Pricing from './pages/Pricing';
import Profile from './pages/Profile';
import PublicShareView from './pages/PublicShareView';

// Components
import Sidebar from './components/Sidebar';
import Spinner from './components/Spinner';

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function App() {
  const { user, loading } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Public routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <Login />} />
        <Route path="/signup" element={user ? <Navigate to="/dashboard" /> : <Signup />} />
        <Route path="/templates" element={<Templates />} />
        <Route path="/share/:shareCode" element={<PublicShareView />} />

        {/* Protected routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <div className="flex">
                <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
                <div className="flex-1 lg:ml-64 min-h-screen">
                  <Dashboard />
                </div>
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/create"
          element={
            <ProtectedRoute>
              <div className="flex">
                <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
                <div className="flex-1 lg:ml-64 min-h-screen">
                  <ResumeBuilder />
                </div>
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/resume/:id/edit"
          element={
            <ProtectedRoute>
              <div className="flex">
                <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
                <div className="flex-1 lg:ml-64 min-h-screen">
                  <ResumeBuilder />
                </div>
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/resume/:id"
          element={
            <ProtectedRoute>
              <div className="flex">
                <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
                <div className="flex-1 lg:ml-64 min-h-screen">
                  <ResumeView />
                </div>
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/pricing"
          element={
            <ProtectedRoute>
              <div className="flex">
                <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
                <div className="flex-1 lg:ml-64 min-h-screen">
                  <Pricing />
                </div>
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <div className="flex">
                <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
                <div className="flex-1 lg:ml-64 min-h-screen">
                  <Profile />
                </div>
              </div>
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
      <Analytics />
    </div>
  );
}

export default App;