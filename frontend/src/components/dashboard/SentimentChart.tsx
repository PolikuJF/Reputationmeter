import { Card, Spin, Alert, Select, DatePicker, Row, Col, Statistic, Tooltip as AntTooltip } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
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
import { formatInGmt5 } from '../../utils/dateUtils';
import type { Dayjs } from 'dayjs';

const { RangePicker } = DatePicker;
const { Option } = Select;

interface SentimentChartProps {
  establishmentId?: number;
  onEstablishmentChange: (id: number | undefined) => void;
  dateRange: [Dayjs, Dayjs] | null;
  onDateRangeChange: (range: [Dayjs, Dayjs] | null) => void;
}

export const SentimentChart = ({
  establishmentId,
  onEstablishmentChange,
  dateRange,
  onDateRangeChange,
}: SentimentChartProps) => {
  const { data: establishments } = useEstablishments();

  const fromDate = dateRange?.[0]?.format('YYYY-MM-DD');
  const toDate = dateRange?.[1]?.format('YYYY-MM-DD');

  const { data, isLoading, error } = useDashboardOverview(establishmentId, fromDate, toDate);

  const selectedEstablishment = establishments?.find(est => est.id === establishmentId);
  const lastParsedAt = selectedEstablishment?.last_parsed_at;
  const lastParsedFormatted = lastParsedAt
    ? formatInGmt5(lastParsedAt)
    : establishmentId ? 'Нет данных' : 'Выберите заведение';

  if (isLoading) return <Spin tip="Загрузка графика..." />;
  if (error) return <Alert message="Ошибка загрузки данных" type="error" showIcon />;
  if (!data) return <Alert message="Нет данных" type="info" />;

  const totalReviews = data.total_reviews;
  const positivePercent = data.positive_percent;
  const neutralPercent = data.neutral_percent;
  const negativePercent = data.negative_percent;

  return (
    <>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} md={6}>
          <Card><Statistic title="Всего отзывов" value={totalReviews} /></Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card><Statistic title="Позитивные" value={positivePercent} suffix="%" valueStyle={{ color: '#52c41a' }} /></Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card><Statistic title="Нейтральные" value={neutralPercent} suffix="%" valueStyle={{ color: '#faad14' }} /></Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card><Statistic title="Негативные" value={negativePercent} suffix="%" valueStyle={{ color: '#ff4d4f' }} /></Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title={<span>Последний сбор <AntTooltip title="Дата и время последнего обновления отзывов"><QuestionCircleOutlined style={{ fontSize: 12, color: '#888' }} /></AntTooltip></span>}
              value={lastParsedFormatted}
              valueStyle={{ fontSize: '14px', fontWeight: 'normal' }}
            />
          </Card>
        </Col>
      </Row>

      <Card
        title="Динамика тональности отзывов"
        extra={
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <Select
              placeholder="Все заведения"
              style={{ width: 180 }}
              value={establishmentId}
              onChange={onEstablishmentChange}
            >
              <Option value={undefined}>Все заведения</Option>
              {establishments?.map((est) => (
                <Option key={est.id} value={est.id}>{est.name}</Option>
              ))}
            </Select>
            <RangePicker
              value={dateRange}
              onChange={(dates) => onDateRangeChange(dates as [Dayjs, Dayjs] | null)}
            />
          </div>
        }
      >
        {data.sentiment_timeline.length === 0 ? (
          <Alert message="Нет данных за выбранный период" type="info" />
        ) : (
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
        )}
      </Card>
    </>
  );
};