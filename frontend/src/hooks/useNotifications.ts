import { useEffect, useRef } from 'react';
import { notification } from 'antd';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';

const fetchUnnotifiedNegativeReviews = async () => {
  const response = await apiClient.get('/reviews/unnotified?sentiment=negative');
  return response.data;
};

export const useNotifications = () => {
  const lastNotifiedRef = useRef<number>(0);

  const { data } = useQuery({
    queryKey: ['negativeReviews', 'unnotified'],
    queryFn: fetchUnnotifiedNegativeReviews,
    refetchInterval: 30000, // каждые 30 секунд
  });

  useEffect(() => {
    if (data && data.length) {
      data.forEach((review: any) => {
        if (review.id > lastNotifiedRef.current) {
          notification.warning({
            message: 'Новый негативный отзыв',
            description: review.text.slice(0, 100),
            placement: 'bottomRight',
          });
        }
      });
      if (data.length) lastNotifiedRef.current = data[data.length - 1].id;
    }
  }, [data]);
};