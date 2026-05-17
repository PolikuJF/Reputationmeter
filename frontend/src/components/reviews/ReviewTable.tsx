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
    updateStatus(
      { reviewId, status: newStatus },
      {
        onSuccess: () => message.success('Статус обновлён'),
        onError: () => message.error('Ошибка обновления'),
      }
    );
  };

  const columns: ColumnsType<Review> = [
    {
      title: 'Текст отзыва',
      dataIndex: 'text',
      key: 'text',
      ellipsis: true,
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
    },
    {
      title: 'Тональность',
      dataIndex: 'sentiment',
      key: 'sentiment',
      width: 130,
      render: (sent: string | null) => {
        if (!sent) return <Text type="secondary">—</Text>;

        const color = sent === 'positive' ? 'green' : sent === 'negative' ? 'red' : 'gold';

        return (
          <Text style={{ color }}>
            {sent === 'positive' ? 'Позитив' : sent === 'negative' ? 'Негатив' : 'Нейтральный'}
          </Text>
        );
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
      width: 180,
      render: (topics: string | null) => topics || '—',
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={reviews}
      loading={loading}
      rowKey="id"
      pagination={{
        pageSize: 10,
        showSizeChanger: true,
        showTotal: (total) => `Всего ${total} отзывов`,
      }}
      scroll={{ x: 1000 }}
    />
  );
};