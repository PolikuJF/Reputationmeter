import { apiClient } from './client';
import { Establishment } from '../types';

export const establishmentsApi = {
  getList: async (activeOnly: boolean = true): Promise<Establishment[]> => {
    const response = await apiClient.get('/establishments', { params: { active_only: activeOnly } });
    return response.data;
  },
};