import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cyber Rescue - Panel de Control & Ranking",
  description: "Clasificación en tiempo real y estadísticas del simulador educativo de ciberseguridad Cyber Rescue.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>
        <div className="cyber-grid"></div>
        {children}
      </body>
    </html>
  );
}
