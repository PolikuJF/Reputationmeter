import { useState } from 'react';
<<<<<<< HEAD
import { Card, List, Button, Input, Form, message, Modal, Popconfirm, Space, Typography } from 'antd';
import { PlusOutlined, DeleteOutlined, PlayCircleOutlined } from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { establishmentsApi } from '../api/establishmentsApi';

const { Text } = Typography;
=======
import { Card, List, Button, Input, Form, message, Modal, Popconfirm } from 'antd';
import { PlusOutlined, DeleteOutlined } from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { establishmentsApi } from '../api/establishmentsApi';
import { apiClient } from '../api/client';

// Расширим establishmentsApi для добавления и архивации
const addEstablishment = async (url: string) => {
  const response = await apiClient.post('/establishments', { url });
  return response.data;
};

const archiveEstablishment = async (id: number) => {
  const response = await apiClient.delete(`/establishments/${id}`);
  return response.data;
};
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1

export const EstablishmentsPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();
  const queryClient = useQueryClient();

  const { data: establishments, isLoading } = useQuery({
<<<<<<< HEAD
    queryKey: ['establishments', false],
=======
    queryKey: ['establishments', false], // false = все, включая архивные
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    queryFn: () => establishmentsApi.getList(false),
  });

  const addMutation = useMutation({
<<<<<<< HEAD
    mutationFn: (url: string) => establishmentsApi.createByUrl(url),
=======
    mutationFn: (url: string) => addEstablishment(url),
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    onSuccess: () => {
      message.success('Заведение добавлено');
      queryClient.invalidateQueries({ queryKey: ['establishments'] });
      setIsModalOpen(false);
      form.resetFields();
    },
<<<<<<< HEAD
    onError: () => message.error('Ошибка добавления заведения'),
  });

  const archiveMutation = useMutation({
    mutationFn: (id: number) => establishmentsApi.archive(id),
=======
    onError: () => message.error('Ошибка добавления'),
  });

  const archiveMutation = useMutation({
    mutationFn: (id: number) => archiveEstablishment(id),
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    onSuccess: () => {
      message.success('Заведение архивировано');
      queryClient.invalidateQueries({ queryKey: ['establishments'] });
    },
    onError: () => message.error('Ошибка архивации'),
  });

<<<<<<< HEAD
  const parsingMutation = useMutation({
    mutationFn: (id: number) => establishmentsApi.runParsing(id),
    onSuccess: (data) => {
      message.success(`Парсинг завершён. Новых отзывов: ${data.saved_reviews}`);
      queryClient.invalidateQueries({ queryKey: ['establishments'] });
      queryClient.invalidateQueries({ queryKey: ['reviews'] });
      queryClient.invalidateQueries({ queryKey: ['dashboardOverview'] });
    },
    onError: () => message.error('Ошибка запуска парсера'),
  });

=======
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
  const handleSubmit = (values: { url: string }) => {
    addMutation.mutate(values.url);
  };

  return (
<<<<<<< HEAD
    <Card
      title="Управление заведениями"
      extra={<Button icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>Добавить</Button>}
    >
=======
    <Card title="Управление заведениями" extra={<Button icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>Добавить</Button>}>
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
      <List
        loading={isLoading}
        dataSource={establishments}
        renderItem={(item) => (
          <List.Item
            actions={[
              !item.is_archived && (
<<<<<<< HEAD
                <Button
                  icon={<PlayCircleOutlined />}
                  loading={parsingMutation.isPending}
                  onClick={() => parsingMutation.mutate(item.id)}
                >
                  Запустить парсер
                </Button>
              ),
              !item.is_archived && (
=======
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
                <Popconfirm
                  title="Архивировать заведение?"
                  onConfirm={() => archiveMutation.mutate(item.id)}
                  okText="Да"
                  cancelText="Нет"
                >
                  <Button icon={<DeleteOutlined />} danger>Архивировать</Button>
                </Popconfirm>
              ),
            ]}
          >
            <List.Item.Meta
              title={item.name}
<<<<<<< HEAD
              description={
                <Space direction="vertical" size={2}>
                  <Text>{item.address || 'Адрес не указан'}</Text>
                  <Text type="secondary">{item.platform_url}</Text>
                  <Text type="secondary">
                    Последний сбор:{' '}
                    {item.last_parsed_at ? new Date(item.last_parsed_at).toLocaleString('ru-RU') : 'ещё не запускался'}
                  </Text>
                </Space>
              }
            />
            {item.is_archived && <Text type="danger">Архивировано</Text>}
          </List.Item>
        )}
      />

      <Modal title="Добавить заведение" open={isModalOpen} onCancel={() => setIsModalOpen(false)} footer={null}>
        <Form form={form} onFinish={handleSubmit} layout="vertical">
          <Form.Item
            name="url"
            label="Ссылка на заведение"
            rules={[{ required: true, message: 'Введите ссылку' }, { type: 'url', message: 'Введите корректный URL' }]}
          >
            <Input placeholder="https://yandex.ru/maps/..." />
=======
              description={item.url}
            />
            {item.is_archived && <span style={{ color: 'red' }}>Архивировано</span>}
          </List.Item>
        )}
      />
      <Modal title="Добавить заведение" open={isModalOpen} onCancel={() => setIsModalOpen(false)} footer={null}>
        <Form form={form} onFinish={handleSubmit} layout="vertical">
          <Form.Item name="url" label="Ссылка на заведение (URL)" rules={[{ required: true, type: 'url' }]}>
            <Input placeholder="https://..." />
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={addMutation.isPending}>Добавить</Button>
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
<<<<<<< HEAD
};
=======
};
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
