"use client";

import { useEffect, useState } from "react";

import { getProjects, getTemplates, getVaults } from "@/lib/api";
import { Project } from "@/lib/types";

import { SearchPanel } from "@/components/search-panel";
import { StatCard } from "@/components/stat-card";

type LoadState = {
  vaultCount: number;
  projectCount: number;
  templateCount: number;
  recentProjects: Project[];
};

export function Dashboard() {
  const [data, setData] = useState<LoadState>({
    vaultCount: 0,
    projectCount: 0,
    templateCount: 0,
    recentProjects: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);

      try {
        const [vaults, projects, templates] = await Promise.all([
          getVaults(),
          getProjects(),
          getTemplates()
        ]);

        setData({
          vaultCount: vaults.length,
          projectCount: projects.length,
          templateCount: templates.length,
          recentProjects: projects.slice(0, 6)
        });
      } catch (loadError) {
        const message =
          loadError instanceof Error
            ? loadError.message
            : "Unable to load dashboard data from API.";
        setError(message);
      } finally {
        setLoading(false);
      }
    };

    void load();
  }, []);

  return (
    <main className="container">
      <header>
        <p className="eyebrow">Arkora</p>
        <h1 className="hero-title">Knowledge Platform Console</h1>
        <p className="hero-description">
          A Next.js frontend for vaults, projects, templates, and semantic discovery powered by your
          Arkora backend.
        </p>
      </header>

      {error ? <p className="alert-error">{error}</p> : null}

      <section className="stats-grid">
        <StatCard
          title="Vaults"
          value={data.vaultCount}
          description={loading ? "Loading..." : "Private and team workspaces"}
        />
        <StatCard
          title="Projects"
          value={data.projectCount}
          description={loading ? "Loading..." : "Structured knowledge domains"}
        />
        <StatCard
          title="Templates"
          value={data.templateCount}
          description={loading ? "Loading..." : "Reusable custom content schemas"}
        />
      </section>

      <section className="content-grid">
        <SearchPanel />

        <article className="card">
          <h2 className="section-title">Recent Projects</h2>
          <ul className="stack-list">
            {data.recentProjects.map((project) => (
              <li key={project.id} className="list-item">
                <p className="list-item__title">{project.name}</p>
                <p className="mini-muted">/{project.slug}</p>
                <p className="mini-muted">
                  status: <span className="strong">{project.status}</span>
                  {project.category ? ` · category: ${project.category}` : ""}
                </p>
              </li>
            ))}
            {!loading && data.recentProjects.length === 0 ? (
              <li className="list-item list-item--placeholder">
                No projects yet. Create one through the backend API.
              </li>
            ) : null}
          </ul>
        </article>
      </section>
    </main>
  );
}
