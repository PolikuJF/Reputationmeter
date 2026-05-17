import { Card, Spin, Alert } from 'antd';
import ReactWordcloud from 'react-wordcloud';
import { useDashboardOverview } from '../../hooks/useDashboard';

// Подготовка данных для облака слов
const prepareWordCloudData = (topTopics: string[]) => {
  // Для MVP просто показываем темы с одинаковым весом, либо на основе частоты
  return topTopics.map((topic) => ({ text: topic, value: 10 }));
};

export const TopicsCloud = () => {
  const { data, isLoading, error } = useDashboardOverview();

  if (isLoading) return <Spin />;
  if (error) return <Alert message="Ошибка" type="error" />;
  if (!data || !data.top_topics.length) return <Alert message="Нет данных по темам" type="info" />;

  const words = prepareWordCloudData(data.top_topics);

  return (
    <Card title="Облако тем">
      <div style={{ height: 300, width: '100%' }}>
        <ReactWordcloud words={words} options={{ rotations: 2, fontSizes: [16, 48] }} />
      </div>
    </Card>
  );
};