import { Tag } from 'antd';

const statusColors = {
  new: 'blue',
  acknowledged: 'orange',
  resolved: 'green',
};

export const ReviewStatusBadge = ({ status }: { status: string }) => {
  return <Tag color={statusColors[status as keyof typeof statusColors]}>{status.toUpperCase()}</Tag>;
};