type StatCardProps = {
  title: string;
  value: number;
  description: string;
};

export function StatCard({ title, value, description }: StatCardProps) {
  return (
    <article className="card stat-card">
      <p className="stat-card__title">{title}</p>
      <p className="stat-card__value">{value}</p>
      <p className="stat-card__description">{description}</p>
    </article>
  );
}
