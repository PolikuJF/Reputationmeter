import { Form, Input, Button, Card, message } from 'antd';
import { useNavigate } from 'react-router-dom';

export const LoginPage = () => {
  const navigate = useNavigate();

  const onFinish = () => {
    localStorage.setItem('access_token', 'demo-token');
    message.success('Вход выполнен');
    navigate('/dashboard');
    setTimeout(() => {
      if (window.location.pathname !== '/dashboard') {
        window.location.href = '/dashboard';
      }
    }, 100);
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <Card title="Вход в систему" style={{ width: 400 }}>
        <Form onFinish={onFinish}>
          <Form.Item name="username" rules={[{ required: true }]}>
            <Input placeholder="Логин" />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true }]}>
            <Input.Password placeholder="Пароль" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>Войти</Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};