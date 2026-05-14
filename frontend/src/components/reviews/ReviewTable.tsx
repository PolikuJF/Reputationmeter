import { Table, Select, Space, message, Typography } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Review } from '../../types';
import { ReviewStatusBadge } from './ReviewStatusBadge';
import { useUpdateReviewStatus } from '../../hooks/useReviews';
import dayjs from 'dayjs'; // установить dayjs

const { Text } = Typography;

interface ReviewTableProps {
  reviews: Review[];
  loading: boolean;
}

export const ReviewTable = ({ reviews, loading }: ReviewTableProps) => {
  const { mutate: updateStatus } = useUpdateReviewStatus();

  const handleStatusChange = (reviewId: number, newStatus: string) => {
    updateStatus({ reviewId, status: newStatus }, {
      onSuccess: () => message.success('Статус обновлён'),
      onError: () => message.error('Ошибка обновления'),
    });
  };

  const columns: ColumnsType<Review> = [
    {
      title: 'Текст отзыва',
      dataIndex: 'text',
      key: 'text',
      ellipsis: true,
      width: '40%',
      render: (text: string) => <Text ellipsis={{ tooltip: true }}>{text}</Text>,
    },
    {
      title: 'Дата',
      dataIndex: 'date',
      key: 'date',
      width: 120,
      render: (date: string) => dayjs(date).format('DD.MM.YYYY'),
    },
    {
      title: 'Тональность',
      dataIndex: 'sentiment',
      key: 'sentiment',
      width: 120,
      render: (sent: string) => {
        if (!sent) return <Text type="secondary">—</Text>;
        const color = sent === 'positive' ? 'green' : sent === 'negative' ? 'red' : 'gold';
        return <Text style={{ color }}>{sent === 'positive' ? 'Позитив' : sent === 'negative' ? 'Негатив' : 'Нейтральный'}</Text>;
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
      width: 150,
      render: (topics: string[] | null) => topics?.join(', ') || '—',
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={reviews}
      loading={loading}
      rowKey="id"
      pagination={{ pageSize: 10, showSizeChanger: true, showTotal: (total) => `Всего ${total} отзывов` }}
      scroll={{ x: 800 }}
      responsive
    />
  );
};