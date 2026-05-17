import { useState } from 'react';
import { Card, List, Button, Input, Form, message, Modal, Popconfirm, Space, Typography } from 'antd';
import { PlusOutlined, DeleteOutlined, PlayCircleOutlined } from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { establishmentsApi } from '../api/establishmentsApi';

const { Text } = Typography;

export const EstablishmentsPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();
  const queryClient = useQueryClient();

  const { data: establishments, isLoading } = useQuery({
    queryKey: ['establishments', false],
    queryFn: () => establishmentsApi.getList(false),
  });

  const addMutation = useMutation({
    mutationFn: (url: string) => establishmentsApi.createByUrl(url),
    onSuccess: () => {
      message.success('Заведение добавлено');
      queryClient.invalidateQueries({ queryKey: ['establishments'] });
      setIsModalOpen(false);
      form.resetFields();
    },
    onError: () => message.error('Ошибка добавления заведения'),
  });

  const archiveMutation = useMutation({
    mutationFn: (id: number) => establishmentsApi.archive(id),
    onSuccess: () => {
      message.success('Заведение архивировано');
      queryClient.invalidateQueries({ queryKey: ['establishments'] });
    },
    onError: () => message.error('Ошибка архивации'),
  });

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

  const handleSubmit = (values: { url: string }) => {
    addMutation.mutate(values.url);
  };

  return (
    <Card
      title="Управление заведениями"
      extra={<Button icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>Добавить</Button>}
    >
      <List
        loading={isLoading}
        dataSource={establishments}
        renderItem={(item) => (
          <List.Item
            actions={[
              !item.is_archived && (
                <Button
                  icon={<PlayCircleOutlined />}
                  loading={parsingMutation.isPending}
                  onClick={() => parsingMutation.mutate(item.id)}
                >
                  Запустить парсер
                </Button>
              ),
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
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={addMutation.isPending}>Добавить</Button>
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};
