export interface Review {
  id: number;
  text: string | null;
  created_at_origin: string | null;
  fetched_at: string;
  establishment_id: number;
  external_id: string;
  author_name: string | null;
  rating: number | null;
  sentiment: 'positive' | 'neutral' | 'negative' | null;
  status: 'new' | 'acknowledged' | 'resolved';
  topics: string | null;
}

export interface Establishment {
  id: number;
  name: string;
  address: string | null;
  platform_url: string;
  platform_type: string;
  external_id: string | null;
  owner_id: number;
  is_archived: boolean;
  created_at: string;
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
