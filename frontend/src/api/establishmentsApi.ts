import { apiClient } from './client';
import { Establishment } from '../types';

export const establishmentsApi = {
  getList: async (activeOnly: boolean = true): Promise<Establishment[]> => {
    const response = await apiClient.get('/establishments', {
      params: { active_only: activeOnly },
    });
    return response.data;
  },

  create: async (data: { name: string; address: string; url: string }): Promise<Establishment> => {
    const response = await apiClient.post('/establishments', data);
    return response.data;
  },

  archive: async (id: number): Promise<void> => {
    await apiClient.delete(`/establishments/${id}`);
  },

  runParsing: async (id: number) => {
    const response = await apiClient.post(`/parsing/establishments/${id}/run`);
    return response.data;
  },
};