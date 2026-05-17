import { useQuery } from '@tanstack/react-query';
import { dashboardApi, DashboardOverview } from '../api/dashboardApi';

export const useDashboardOverview = (establishmentId?: number, fromDate?: string, toDate?: string) => {
  return useQuery<DashboardOverview>({
    queryKey: ['dashboardOverview', establishmentId, fromDate, toDate],
    queryFn: () => dashboardApi.getOverview(establishmentId, fromDate, toDate),
    staleTime: 5 * 60 * 1000,
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 10000),
  });
};