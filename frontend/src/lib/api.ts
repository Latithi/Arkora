import { ContentTemplate, Project, SearchResponse, Vault } from "@/lib/types";

const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? DEFAULT_API_BASE_URL;

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Request failed (${response.status}): ${response.statusText}`);
  }

  return (await response.json()) as T;
}

export async function getVaults(): Promise<Vault[]> {
  return request<Vault[]>("/vaults");
}

export async function getProjects(): Promise<Project[]> {
  return request<Project[]>("/projects");
}

export async function getTemplates(): Promise<ContentTemplate[]> {
  return request<ContentTemplate[]>("/templates");
}

export async function searchKnowledge(query: string): Promise<SearchResponse> {
  const encodedQuery = encodeURIComponent(query);
  return request<SearchResponse>(`/search?q=${encodedQuery}&limit=5`);
}
