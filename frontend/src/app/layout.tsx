import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Arkora Console",
  description: "Frontend console for Arkora knowledge platform"
};

type RootLayoutProps = Readonly<{ children: React.ReactNode }>;

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
