"use client";

import { FormEvent, useState } from "react";

import { searchKnowledge } from "@/lib/api";
import { SearchHit } from "@/lib/types";

export function SearchPanel() {
  const [query, setQuery] = useState("oauth token endpoint");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hits, setHits] = useState<SearchHit[]>([]);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!query.trim()) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await searchKnowledge(query);
      setHits(response.hits);
    } catch (submitError) {
      const message =
        submitError instanceof Error
          ? submitError.message
          : "Unable to load search results right now.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2 className="section-title">Semantic Search</h2>
      <p className="muted">Query your knowledge graph using natural language.</p>

      <form className="search-form" onSubmit={onSubmit}>
        <input
          className="text-input"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search for architecture, APIs, incidents..."
        />
        <button type="submit" disabled={loading} className="button">
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {error ? <p className="error-text">{error}</p> : null}

      <ul className="stack-list">
        {hits.map((hit) => (
          <li key={hit.item_id} className="list-item">
            <div className="list-item__header">
              <h3 className="list-item__title">{hit.title}</h3>
              <span className="pill">score {hit.score}</span>
            </div>
            <p className="muted">{hit.snippet || "No snippet available."}</p>
          </li>
        ))}
        {!loading && hits.length === 0 ? (
          <li className="list-item list-item--placeholder">
            No hits yet. Try a search query after adding content in the backend.
          </li>
        ) : null}
      </ul>
    </section>
  );
}
