import { Card, Spin, Alert, Select, DatePicker } from 'antd';
import { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useDashboardOverview } from '../../hooks/useDashboard';
import { useEstablishments } from '../../hooks/useEstablishments';
import type { Dayjs } from 'dayjs';

const { RangePicker } = DatePicker;
const { Option } = Select;

export const SentimentChart = () => {
  const [establishmentId, setEstablishmentId] = useState<number | undefined>(undefined);
  const [dateRange, setDateRange] = useState<[Dayjs, Dayjs] | null>(null);
  const { data: establishments } = useEstablishments();

  const fromDate = dateRange?.[0]?.format('YYYY-MM-DD');
  const toDate = dateRange?.[1]?.format('YYYY-MM-DD');

  const { data, isLoading, error } = useDashboardOverview(establishmentId, fromDate, toDate);

  if (isLoading) return <Spin tip="Загрузка графика..." />;
  if (error) return <Alert message="Ошибка загрузки данных" type="error" showIcon />;
  if (!data || !data.sentiment_timeline.length) return <Alert message="Нет данных за выбранный период" type="info" />;

  return (
    <Card
      title="Динамика тональности отзывов"
      extra={
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <Select
            placeholder="Все заведения"
            style={{ width: 180 }}
            allowClear
            value={establishmentId}
            onChange={setEstablishmentId}
          >
            {establishments?.map((est) => (
              <Option key={est.id} value={est.id}>{est.name}</Option>
            ))}
          </Select>
          <RangePicker
            value={dateRange}
            onChange={(dates) => setDateRange(dates as [Dayjs, Dayjs] | null)}
          />
        </div>
      }
    >
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data.sentiment_timeline}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" tick={{ fontSize: 12 }} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="positive" stroke="#52c41a" name="Позитивные" strokeWidth={2} />
          <Line type="monotone" dataKey="neutral" stroke="#faad14" name="Нейтральные" strokeWidth={2} />
          <Line type="monotone" dataKey="negative" stroke="#ff4d4f" name="Негативные" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
};