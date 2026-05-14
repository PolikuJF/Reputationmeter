import { useState } from 'react';
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

export const EstablishmentsPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();
  const queryClient = useQueryClient();

  const { data: establishments, isLoading } = useQuery({
    queryKey: ['establishments', false], // false = все, включая архивные
    queryFn: () => establishmentsApi.getList(false),
  });

  const addMutation = useMutation({
    mutationFn: (url: string) => addEstablishment(url),
    onSuccess: () => {
      message.success('Заведение добавлено');
      queryClient.invalidateQueries({ queryKey: ['establishments'] });
      setIsModalOpen(false);
      form.resetFields();
    },
    onError: () => message.error('Ошибка добавления'),
  });

  const archiveMutation = useMutation({
    mutationFn: (id: number) => archiveEstablishment(id),
    onSuccess: () => {
      message.success('Заведение архивировано');
      queryClient.invalidateQueries({ queryKey: ['establishments'] });
    },
    onError: () => message.error('Ошибка архивации'),
  });

  const handleSubmit = (values: { url: string }) => {
    addMutation.mutate(values.url);
  };

  return (
    <Card title="Управление заведениями" extra={<Button icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>Добавить</Button>}>
      <List
        loading={isLoading}
        dataSource={establishments}
        renderItem={(item) => (
          <List.Item
            actions={[
              !item.is_archived && (
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
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={addMutation.isPending}>Добавить</Button>
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};