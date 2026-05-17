import { Table, Select, message, Typography } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Review } from '../../types';
import { useUpdateReviewStatus } from '../../hooks/useReviews';
import dayjs from 'dayjs';

const { Text } = Typography;

interface ReviewTableProps {
  reviews: Review[];
  loading: boolean;
}

export const ReviewTable = ({ reviews, loading }: ReviewTableProps) => {
  const { mutate: updateStatus } = useUpdateReviewStatus();

  const handleStatusChange = (reviewId: number, newStatus: string) => {
<<<<<<< HEAD
    updateStatus(
      { reviewId, status: newStatus },
      {
        onSuccess: () => message.success('Статус обновлён'),
        onError: () => message.error('Ошибка обновления'),
      }
    );
=======
    updateStatus({ reviewId, status: newStatus }, {
      onSuccess: () => message.success('Статус обновлён'),
      onError: () => message.error('Ошибка обновления'),
    });
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
  };

  const columns: ColumnsType<Review> = [
    {
      title: 'Текст отзыва',
      dataIndex: 'text',
      key: 'text',
      ellipsis: true,
<<<<<<< HEAD
      width: '45%',
      render: (text: string | null) => <Text ellipsis={{ tooltip: true }}>{text || '—'}</Text>,
    },
    {
      title: 'Автор',
      dataIndex: 'author_name',
      key: 'author_name',
      width: 160,
      render: (author: string | null) => author || '—',
    },
    {
      title: 'Дата',
      dataIndex: 'created_at_origin',
      key: 'created_at_origin',
      width: 120,
      render: (date: string | null) => (date ? dayjs(date).format('DD.MM.YYYY') : '—'),
=======
      width: '40%',
      render: (text: string) => <Text ellipsis={{ tooltip: true }}>{text}</Text>,
    },
    {
      title: 'Дата',
      dataIndex: 'date',
      key: 'date',
      width: 120,
      render: (date: string) => dayjs(date).format('DD.MM.YYYY'),
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    },
    {
      title: 'Тональность',
      dataIndex: 'sentiment',
      key: 'sentiment',
<<<<<<< HEAD
      width: 130,
      render: (sent: string | null) => {
        if (!sent) return <Text type="secondary">—</Text>;

        const color = sent === 'positive' ? 'green' : sent === 'negative' ? 'red' : 'gold';

        return (
          <Text style={{ color }}>
            {sent === 'positive' ? 'Позитив' : sent === 'negative' ? 'Негатив' : 'Нейтральный'}
          </Text>
        );
=======
      width: 120,
      render: (sent: string) => {
        if (!sent) return <Text type="secondary">—</Text>;
        const color = sent === 'positive' ? 'green' : sent === 'negative' ? 'red' : 'gold';
        return <Text style={{ color }}>{sent === 'positive' ? 'Позитив' : sent === 'negative' ? 'Негатив' : 'Нейтральный'}</Text>;
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
      },
    },
    {
      title: 'Статус',
      dataIndex: 'status',
      key: 'status',
      width: 150,
      render: (status: string, record: Review) => (
        <Select
          value={status}
          style={{ width: 120 }}
          onChange={(val) => handleStatusChange(record.id, val)}
          options={[
            { value: 'new', label: 'Новый' },
            { value: 'acknowledged', label: 'В работе' },
            { value: 'resolved', label: 'Решён' },
          ]}
        />
      ),
    },
    {
      title: 'Темы',
      dataIndex: 'topics',
      key: 'topics',
<<<<<<< HEAD
      width: 180,
      render: (topics: string | null) => topics || '—',
=======
      width: 150,
      render: (topics: string[] | null) => topics?.join(', ') || '—',
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={reviews}
      loading={loading}
      rowKey="id"
<<<<<<< HEAD
      pagination={{
        pageSize: 10,
        showSizeChanger: true,
        showTotal: (total) => `Всего ${total} отзывов`,
      }}
      scroll={{ x: 1000 }}
=======
      pagination={{ pageSize: 10, showSizeChanger: true, showTotal: (total) => `Всего ${total} отзывов` }}
      scroll={{ x: 800 }}
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    />
  );
};