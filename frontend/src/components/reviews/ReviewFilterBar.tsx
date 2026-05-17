import { Select, Row, Col, Button } from 'antd';
import { useEstablishments } from '../../hooks/useEstablishments';

const { Option } = Select;

interface FilterBarProps {
  selectedEstablishment: number | undefined;
  setSelectedEstablishment: (id: number | undefined) => void;
  selectedSentiment: string | undefined;
  setSelectedSentiment: (sent: string | undefined) => void;
}

export const ReviewFilterBar = ({
  selectedEstablishment,
  setSelectedEstablishment,
  selectedSentiment,
  setSelectedSentiment,
}: FilterBarProps) => {
  const { data: establishments, isLoading: estLoading } = useEstablishments();

  const handleReset = () => {
    setSelectedEstablishment(undefined);
    setSelectedSentiment(undefined);
  };

  return (
    <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
      <Col xs={24} sm={12} md={8}>
        <Select
          placeholder="Все заведения"
          style={{ width: '100%' }}
          allowClear
          loading={estLoading}
          value={selectedEstablishment}
          onChange={(val) => setSelectedEstablishment(val ?? undefined)}
        >
          {establishments?.map((est) => (
            <Option key={est.id} value={est.id}>{est.name}</Option>
          ))}
        </Select>
      </Col>
      <Col xs={24} sm={12} md={8}>
        <Select
          placeholder="Любая тональность"
          style={{ width: '100%' }}
          allowClear
          value={selectedSentiment}
          onChange={(val) => setSelectedSentiment(val ?? undefined)}
        >
          <Option value="positive">Позитивный</Option>
          <Option value="neutral">Нейтральный</Option>
          <Option value="negative">Негативный</Option>
        </Select>
      </Col>
      <Col xs={24} sm={12} md={8}>
        <Button onClick={handleReset}>Сбросить фильтры</Button>
      </Col>
    </Row>
  );
};