import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { reviewsApi } from '../api/reviewsApi';
import { ReviewsFilters } from '../types';

export const useReviews = (filters: ReviewsFilters) => {
  return useQuery({
    queryKey: ['reviews', filters],
    queryFn: () => reviewsApi.getList(filters),
    staleTime: 2 * 60 * 1000,
  });
};

export const useUpdateReviewStatus = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ reviewId, status }: { reviewId: number; status: string }) =>
      reviewsApi.updateStatus(reviewId, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews'] });
    },
  });
};