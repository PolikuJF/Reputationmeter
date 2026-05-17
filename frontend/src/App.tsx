import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DashboardPage } from './pages/DashboardPage';
import { LoginPage } from './pages/LoginPage';
import { Layout } from './components/common/Layout';
import { EstablishmentsPage } from './pages/EstablishmentsPage';
import { RegisterPage } from './pages/RegisterPage';

const queryClient = new QueryClient();

function App() {
  // Простейшая проверка авторизации (для демо)
  const isAuthenticated = !!localStorage.getItem('access_token');

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/dashboard"
            element={
              isAuthenticated ? (
                <Layout>
                  <DashboardPage />
                </Layout>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route path="/" element={<Navigate to="/dashboard" />} />
          <Route path="/establishments" element={<Layout><EstablishmentsPage /></Layout>} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;