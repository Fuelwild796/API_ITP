const API_BASE_URL = 'http://localhost:8000';

export async function fetchData<T>(endpoint: string): Promise<T | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/${endpoint}`);
    if (!response.ok) {
      console.error(`HTTP Error: ${response.status} fetching ${endpoint}`);
      return null;
    }
    return await response.json();
  } catch (error) {
    console.error(`Failed to fetch data from ${endpoint}:`, error);
    return null;
  }
}