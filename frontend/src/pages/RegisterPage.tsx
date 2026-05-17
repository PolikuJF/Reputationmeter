import { Form, Input, Button, Card, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';

export const RegisterPage = () => {
  const navigate = useNavigate();

  const onFinish = async (values: { email: string; password: string; full_name: string }) => {
    try {
      await apiClient.post('/auth/register', values);
      message.success('Регистрация успешна, теперь войдите');
      navigate('/login');
    } catch (error) {
      message.error('Ошибка регистрации');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <Card title="Регистрация" style={{ width: 400 }}>
        <Form onFinish={onFinish}>
          <Form.Item name="email" rules={[{ required: true, type: 'email' }]}>
            <Input placeholder="Email" />
          </Form.Item>
          <Form.Item name="full_name">
            <Input placeholder="Полное имя" />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true }]}>
            <Input.Password placeholder="Пароль" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>Зарегистрироваться</Button>
          </Form.Item>
          <Form.Item>
            <Button type="link" onClick={() => navigate('/login')}>Уже есть аккаунт? Войти</Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};