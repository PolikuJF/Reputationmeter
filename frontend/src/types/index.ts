export interface Review {
  id: number;
<<<<<<< HEAD
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
=======
  text: string;
  date: string;
  establishment_id: number;
  sentiment: 'positive' | 'neutral' | 'negative' | null;
  status: 'new' | 'acknowledged' | 'resolved';
  topics: string[] | null;
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
}

export interface Establishment {
  id: number;
  name: string;
<<<<<<< HEAD
  address: string | null;
  platform_url: string;
  platform_type: string;
  external_id: string | null;
  owner_id: number;
  is_archived: boolean;
  created_at: string;
=======
  url: string;
  is_archived: boolean;
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
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
<<<<<<< HEAD
}
=======
}
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
