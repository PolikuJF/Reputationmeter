import { apiClient } from './client';
import { Establishment } from '../types';

export const establishmentsApi = {
  getList: async (activeOnly: boolean = true): Promise<Establishment[]> => {
<<<<<<< HEAD
    const response = await apiClient.get('/establishments', {
      params: { active_only: activeOnly },
    });
    return response.data;
  },

  createByUrl: async (url: string): Promise<Establishment> => {
    const response = await apiClient.post('/establishments', { url });
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
=======
    const response = await apiClient.get('/establishments', { params: { active_only: activeOnly } });
    return response.data;
  },
};
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
