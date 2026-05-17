import { apiClient } from './client';

export interface SentimentTimelinePoint {
  date: string;
  positive: number;
  neutral: number;
  negative: number;
}

export interface DashboardOverview {
  total_reviews: number;
  positive_percent: number;
  neutral_percent: number;
  negative_percent: number;
  sentiment_timeline: SentimentTimelinePoint[];
  top_topics: string[];
}

export const dashboardApi = {
  getOverview: async (establishmentId?: number, fromDate?: string, toDate?: string): Promise<DashboardOverview> => {
    const params = new URLSearchParams();
    if (establishmentId) params.append('establishment_id', String(establishmentId));
    if (fromDate) params.append('from_date', fromDate);
    if (toDate) params.append('to_date', toDate);
    const response = await apiClient.get(`/dashboard/overview?${params.toString()}`);
    return response.data;
  },
};