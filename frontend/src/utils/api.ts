// Define the type for the API response
import {getUserId} from "../store/session.ts";

interface ApiResponse<T> {
  data: T | null;
  error: string | null;
}

// Define a generic function to make API calls
async function fetchData<T>(url: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
      return {
        data: null,
        error: data.message || 'An error occurred while fetching data'
      };
    }

    return {
      data: data as T,
      error: null
    };
  } catch (error) {
    return {
      data: null,
      error: (error as Error).message
    };
  }
}

interface User {
  user_id: string;
}

interface Book {
  title: string;
}

const api_basepath = "https://eg9x85kiwd.execute-api.us-east-1.amazonaws.com/Prod";

export async function createUser(): Promise<ApiResponse<User>> {
  return fetchData<User>(api_basepath + '/user/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
  });
}

export async function getBook(bookId: string): Promise<ApiResponse<Book>> {
  return fetchData<Book>(`${api_basepath}/book/${bookId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      // 'X-User-Id': getUserId(),
      'Authorization': getUserId()
    },
  });
}

export async function listBooks(): Promise<ApiResponse<any>> {
  return fetchData<any>(`${api_basepath}/books`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      // 'X-User-Id': getUserId(),
      'Authorization': getUserId()
    },
  });
}
