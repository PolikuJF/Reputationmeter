import { useQuery } from '@tanstack/react-query';
import { establishmentsApi } from '../api/establishmentsApi';

export const useEstablishments = () => {
  return useQuery({
    queryKey: ['establishments'],
    queryFn: () => establishmentsApi.getList(true),
    staleTime: 10 * 60 * 1000,
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 10000),
  });
};