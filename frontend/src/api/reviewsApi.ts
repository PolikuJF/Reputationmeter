import { apiClient } from './client';
import { Review, ReviewsFilters, ReviewsResponse } from '../types';

export const reviewsApi = {
  getList: async (filters: ReviewsFilters): Promise<ReviewsResponse> => {
    const params = new URLSearchParams();
    if (filters.establishment_id) params.append('establishment_id', String(filters.establishment_id));
    if (filters.sentiment) params.append('sentiment', filters.sentiment);
    if (filters.status) params.append('status', filters.status);
    if (filters.limit) params.append('limit', String(filters.limit));
    if (filters.offset) params.append('offset', String(filters.offset));
    if (filters.from_date) params.append('from_date', filters.from_date);
    if (filters.to_date) params.append('to_date', filters.to_date);
    const response = await apiClient.get(`/reviews?${params.toString()}`);
    return response.data;
  },
  updateStatus: async (reviewId: number, status: string): Promise<Review> => {
    const response = await apiClient.patch(`/reviews/${reviewId}/status`, { status });
    return response.data;
  },
};