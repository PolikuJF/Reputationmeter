import { Row, Col } from 'antd';
import { SentimentChart } from '../components/dashboard/SentimentChart';
import { TopicsCloud } from '../components/dashboard/TopicsCloud';
import { ReviewFilterBar } from '../components/reviews/ReviewFilterBar';
import { ReviewTable } from '../components/reviews/ReviewTable';
import { useReviews } from '../hooks/useReviews';
import { useState } from 'react';

export const DashboardPage = () => {
  const [establishmentId, setEstablishmentId] = useState<number | undefined>(undefined);
  const [sentiment, setSentiment] = useState<string | undefined>(undefined);

  const { data, isLoading } = useReviews({
    establishment_id: establishmentId,
    sentiment: sentiment,
    limit: 100,
  });

  return (
    <div style={{ padding: '24px' }}>
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={16}>
          <SentimentChart />
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