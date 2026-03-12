export type Vault = {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
};

export type Project = {
  id: number;
  vault_id: number;
  name: string;
  slug: string;
  status: string;
  category: string | null;
  created_at: string;
  updated_at: string;
};

export type ContentTemplate = {
  id: number;
  name: string;
  description: string | null;
  schema: Record<string, unknown>;
  created_at: string;
  updated_at: string;
};

export type SearchHit = {
  item_id: number;
  project_id: number;
  title: string;
  score: number;
  snippet: string;
};

export type SearchResponse = {
  query: string;
  total: number;
  hits: SearchHit[];
};
