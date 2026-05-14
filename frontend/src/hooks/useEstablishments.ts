import { useQuery } from '@tanstack/react-query';
import { establishmentsApi } from '../api/establishmentsApi';

export const useEstablishments = () => {
  return useQuery({
    queryKey: ['establishments'],
    queryFn: () => establishmentsApi.getList(true),
    staleTime: 10 * 60 * 1000,
  });
};