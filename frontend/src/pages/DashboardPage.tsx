import { useState } from 'react';
import { Row, Col } from 'antd';
import { SentimentChart } from '../components/dashboard/SentimentChart';
import { TopicsCloud } from '../components/dashboard/TopicsCloud';
import { ReviewFilterBar } from '../components/reviews/ReviewFilterBar';
import { ReviewTable } from '../components/reviews/ReviewTable';
import { useReviews } from '../hooks/useReviews';
import type { Dayjs } from 'dayjs';

export const DashboardPage = () => {
  const [establishmentId, setEstablishmentId] = useState<number | undefined>(undefined);
  const [sentiment, setSentiment] = useState<string | undefined>(undefined);
  const [dateRange, setDateRange] = useState<[Dayjs, Dayjs] | null>(null);

  const fromDate = dateRange?.[0]?.format('YYYY-MM-DD');
  const toDate = dateRange?.[1]?.format('YYYY-MM-DD');

  const { data, isLoading } = useReviews({
    establishment_id: establishmentId,
    sentiment: sentiment,
    from_date: fromDate,
    to_date: toDate,
    limit: 100,
  });

  return (
    <div style={{ padding: '24px' }}>
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={16}>
          <SentimentChart
            establishmentId={establishmentId}
            onEstablishmentChange={setEstablishmentId}
            dateRange={dateRange}
            onDateRangeChange={setDateRange}
          />
        </Col>
        <Col xs={24} lg={8}>
          <TopicsCloud />
        </Col>
        <Col xs={24}>
          <ReviewFilterBar
            selectedEstablishment={establishmentId}
            setSelectedEstablishment={setEstablishmentId}
            selectedSentiment={sentiment}
            setSelectedSentiment={setSentiment}
          />
          <ReviewTable reviews={data?.items || []} loading={isLoading} />
        </Col>
      </Row>
    </div>
  );
};