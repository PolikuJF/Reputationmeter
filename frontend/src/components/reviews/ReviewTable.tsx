import { formatInGmt5 } from '../../utils/dateUtils';
import { Table, Select, message, Typography } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Review } from '../../types';
import { useUpdateReviewStatus } from '../../hooks/useReviews';

const { Text } = Typography;

const sortByString = (a: string | null, b: string | null) => {
  const aStr = a?.toLowerCase() ?? '';
  const bStr = b?.toLowerCase() ?? '';
  return aStr.localeCompare(bStr);
};

const sortByDate = (a: string | null, b: string | null) => {
  const aTime = a ? new Date(a).getTime() : 0;
  const bTime = b ? new Date(b).getTime() : 0;
  return aTime - bTime;
};

const sortBySentiment = (a: string | null, b: string | null) => {
  const order = { positive: 1, neutral: 2, negative: 3 };
  const aVal = a ? order[a as keyof typeof order] ?? 4 : 4;
  const bVal = b ? order[b as keyof typeof order] ?? 4 : 4;
  return aVal - bVal;
};

const sortByStatus = (a: string | null, b: string | null) => {
  const order = { new: 1, acknowledged: 2, resolved: 3 };
  const aVal = a ? order[a as keyof typeof order] ?? 4 : 4;
  const bVal = b ? order[b as keyof typeof order] ?? 4 : 4;
  return aVal - bVal;
};

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
      sorter: (a, b) => sortByString(a.author_name, b.author_name),
      sortDirections: ['ascend', 'descend'],
      render: (author: string | null) => author || '—',
    },
    {
      title: 'Дата',
      dataIndex: 'created_at_origin',
      key: 'created_at_origin',
      width: 120,
      sorter: (a, b) => sortByDate(a.created_at_origin, b.created_at_origin),
      sortDirections: ['ascend', 'descend'],
      render: (date: string | null) => (date ? formatInGmt5(date, { dateStyle: 'short', timeStyle: 'short' }) : '—'),
    },
    {
      title: 'Тональность',
      dataIndex: 'sentiment',
      key: 'sentiment',
      width: 130,
      sorter: (a, b) => sortBySentiment(a.sentiment, b.sentiment),
      sortDirections: ['ascend', 'descend'],
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
      sorter: (a, b) => sortByStatus(a.status, b.status),
      sortDirections: ['ascend', 'descend'],
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
      sorter: (a, b) => sortByString(a.topics, b.topics),
      sortDirections: ['ascend', 'descend'],
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