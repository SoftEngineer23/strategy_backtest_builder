import axios from 'axios';
import type { GenerateResponse, BacktestResponse, BacktestConfig } from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface GenerateOptions {
  useAgent?: boolean;
}

export async function generateStrategy(
  description: string,
  options: GenerateOptions = {}
): Promise<GenerateResponse> {
  try {
    const response = await api.post('/generate', {
      description,
      use_agent: options.useAgent ?? false,
    });
    return response.data;
  } catch (error: unknown) {
    const err = error as { response?: { data?: { error?: string } }; message?: string };
    return {
      success: false,
      code: null,
      error: err.response?.data?.error || err.message || 'Unknown error',
    };
  }
}

export async function runBacktest(
  code: string,
  config: BacktestConfig
): Promise<BacktestResponse> {
  try {
    const response = await api.post('/backtest', {
      code,
      ...config,
    });
    return response.data;
  } catch (error: unknown) {
    const err = error as { response?: { data?: { error?: string } }; message?: string };
    return {
      success: false,
      metrics: null,
      equity_curve: null,
      error: err.response?.data?.error || err.message || 'Unknown error',
    };
  }
}
