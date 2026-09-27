import type { Metadata } from "next";
import "./globals.css";
import { Header } from "../components/layout/Header";

export const metadata: Metadata = {
  title: "ImpeccableOS | Adaptive AI Engineering Trainer & Execution Engine",
  description:
    "Enterprise-grade adaptive training platform for AI engineers featuring deterministic DAG roadmaps, hybrid RRF retrieval, and evidence-calibrated confidence scoring.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-slate-100 min-h-screen flex flex-col">
        <Header />
        <main className="flex-1 flex">{children}</main>
      </body>
    </html>
  );
}
