export interface Review {
  id: number;
  text: string;
  date: string;
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
  last_parsed_at?: string | null;
}

export interface ReviewsFilters {
  establishment_id?: number;
  sentiment?: string;
  status?: string;
  limit?: number;
  offset?: number;
  from_date?: string;
  to_date?: string;
}

export interface ReviewsResponse {
  items: Review[];
  total: number;
}