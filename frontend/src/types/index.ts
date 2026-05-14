export interface Review {
  id: number;
  text: string;
  date: string;        // ISO
  establishment_id: number;
  sentiment: 'positive' | 'neutral' | 'negative' | null;
  status: 'new' | 'acknowledged' | 'resolved';
  topics: string[] | null;
}

export interface Establishment {
  id: number;
  name: string;
  url: string;
  is_archived: boolean;
}

export interface ReviewsFilters {
  establishment_id?: number;
  sentiment?: string;
  status?: string;
  limit?: number;
  offset?: number;
}

export interface ReviewsResponse {
  items: Review[];
  total: number;
}