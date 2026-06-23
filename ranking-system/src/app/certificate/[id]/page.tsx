'use client';

import React, { useState, use } from 'react';
import { useRouter } from 'next/navigation';

interface PageProps {
  params: Promise<{ id: string }>;
}

interface CertificateData {
  player_name: string;
  score: number;
  time_left: number;
  created_at: string;
}

export default function CertificatePage({ params }: PageProps) {
  const { id } = use(params);
  const router = useRouter();
  
  const [password, setPassword] = useState('');
  const [data, setData] = useState<CertificateData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/scores/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, password })
      });

      const json = await res.json();
      if (!res.ok) {
        throw new Error(json.error || 'Error al verificar las credenciales');
      }

      setData(json);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (secs: number) => {
    const mins = Math.floor(secs / 60);
    const s = secs % 60;
    return `${String(mins).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  };

  const formatDate = (isoString: string) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
      });
    } catch {
      return '';
    }
  };

  // 1. Pantalla de bloqueo: Pedir contraseña
  if (!data) {
    return (
      <div className="verify-container">
        <style>{`
          .verify-container {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
          }
          .verify-card {
            width: 100%;
            max-width: 420px;
            padding: 40px 30px;
            text-align: center;
            border-radius: 4px;
          }
          .verify-title {
            color: var(--primary-color);
            font-size: 1.5rem;
            font-family: var(--font-mono);
            margin-bottom: 25px;
            letter-spacing: 1px;
            text-transform: uppercase;
          }
          .form-group {
            margin-bottom: 20px;
            text-align: left;
          }
          .form-group label {
            display: block;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 6px;
            text-transform: uppercase;
          }
          .form-input {
            width: 100%;
            background: rgba(10, 17, 32, 0.8);
            border: 1px solid var(--panel-border);
            border-radius: 4px;
            padding: 12px 15px;
            font-family: var(--font-mono);
            color: var(--primary-color);
            font-size: 1.1rem;
            text-align: center;
            letter-spacing: 4px;
          }
          .form-input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 15px var(--primary-glow);
          }
          .error-msg {
            color: var(--danger-color);
            font-family: var(--font-mono);
            font-size: 0.85rem;
            margin-top: 15px;
          }
          .back-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-family: var(--font-mono);
            margin-top: 25px;
            cursor: pointer;
            text-decoration: underline;
            font-size: 0.85rem;
          }
          .back-btn:hover {
            color: var(--text-main);
          }
        `}</style>
        
        <div className="verify-card cyber-panel">
          <h2 className="verify-title glow-green">Seguridad del Certificado</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '25px', lineHeight: '1.4' }}>
            Esta credencial está protegida. Ingresa la contraseña que definiste al registrar tu alias en la simulación.
          </p>

          <form onSubmit={handleVerify}>
            <div className="form-group">
              <label>Contraseña del Certificado</label>
              <input
                type="password"
                className="form-input"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••"
              />
            </div>
            
            <button type="submit" className="btn-cyber" style={{ width: '100%' }} disabled={loading}>
              {loading ? 'VERIFICANDO...' : 'DESBLOQUEAR CERTIFICADO'}
            </button>
          </form>

          {error && <p className="error-msg glow-red">[!] ERROR: {error}</p>}

          <button onClick={() => router.push('/')} className="back-btn">
            &lt; Volver al Ranking General
          </button>
        </div>
      </div>
    );
  }

  // 2. Pantalla de Certificado Desbloqueado
  return (
    <div className="cert-page-wrapper">
      <style>{`
        /* Fuentes cursivas para las firmas */
        @import url('https://fonts.googleapis.com/css2?family=Alex+Brush&family=Great+Vibes&display=swap');

        .cert-page-wrapper {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 30px 20px;
          background: #02040a;
        }

        .action-bar {
          display: flex;
          justify-content: space-between;
          width: 100%;
          max-width: 960px;
          margin-bottom: 20px;
        }

        /* Contenedor del Certificado */
        .certificate-container {
          width: 100%;
          max-width: 960px;
          height: 640px; /* Relación de aspecto landscape fija para pantalla */
          background: #fdfbf7;
          color: #1e293b;
          padding: 40px 50px;
          border: 15px double #c5a059;
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8), inset 0 0 40px rgba(197, 160, 89, 0.05);
          position: relative;
          text-align: center;
          border-radius: 2px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          box-sizing: border-box;
        }

        /* Marca de agua de fondo */
        .cert-watermark {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          font-size: 8rem;
          font-family: var(--font-mono);
          font-weight: bold;
          color: rgba(197, 160, 89, 0.03);
          pointer-events: none;
          z-index: 1;
          letter-spacing: 15px;
          text-transform: uppercase;
        }

        .cert-header {
          font-family: var(--font-mono);
          font-size: 0.8rem;
          font-weight: bold;
          letter-spacing: 3px;
          color: #c5a059;
          text-transform: uppercase;
          z-index: 2;
          position: relative;
        }

        .cert-logo {
          font-size: 1.4rem;
          font-weight: 800;
          color: #1e293b;
          letter-spacing: 1px;
          border-bottom: 1px solid rgba(197, 160, 89, 0.3);
          padding-bottom: 8px;
          display: inline-block;
          min-width: 250px;
          margin: 0 auto;
          z-index: 2;
          position: relative;
        }

        .cert-title {
          font-family: var(--font-display);
          font-size: 2rem;
          font-weight: 800;
          color: #c5a059;
          text-transform: uppercase;
          letter-spacing: 2px;
          margin-top: 10px;
          z-index: 2;
          position: relative;
        }

        .cert-recipient-intro {
          font-style: italic;
          font-size: 0.95rem;
          color: #64748b;
          z-index: 2;
          position: relative;
        }

        .cert-name {
          font-size: 2.4rem;
          font-weight: 800;
          color: #0f172a;
          text-decoration: underline;
          text-decoration-color: #c5a059;
          text-underline-offset: 6px;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin: 5px 0;
          z-index: 2;
          position: relative;
        }

        .cert-body {
          font-size: 1.05rem;
          line-height: 1.6;
          color: #334155;
          max-width: 780px;
          margin: 0 auto;
          z-index: 2;
          position: relative;
        }

        .cert-body strong {
          color: #0f172a;
        }

        .cert-skills-badge {
          background: rgba(197, 160, 89, 0.04);
          border: 1px dashed #c5a059;
          padding: 10px 20px;
          font-size: 0.9rem;
          color: #475569;
          font-family: var(--font-mono);
          line-height: 1.4;
          margin: 0 auto;
          max-width: 800px;
          z-index: 2;
          position: relative;
        }

        /* Bloque de firmas */
        .signatures-section {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 20px;
          margin-top: 15px;
          z-index: 2;
          position: relative;
        }

        .signature-block {
          text-align: center;
          display: flex;
          flex-direction: column;
          justify-content: flex-end;
          align-items: center;
        }

        .signature-line {
          border-top: 1px solid #cbd5e1;
          padding-top: 6px;
          width: 85%;
        }

        .signature-image {
          font-family: 'Great Vibes', cursive;
          font-size: 2.2rem;
          color: #1e3a8a; /* Tinta azul estilizada */
          height: 45px;
          display: flex;
          align-items: center;
          justify-content: center;
          user-select: none;
        }

        /* Firma de Rodrigo Rosa (Adrián) */
        .signature-image.rodrigo {
          font-family: 'Alex Brush', cursive;
          font-size: 2.6rem;
          transform: rotate(-3deg);
        }

        .signature-image.melanie {
          font-family: 'Great Vibes', cursive;
          font-size: 2.4rem;
          transform: rotate(-1deg);
        }

        .signature-image.lemus {
          font-family: 'Alex Brush', cursive;
          font-size: 2.4rem;
          transform: rotate(2deg);
        }

        .signature-name {
          font-weight: bold;
          font-size: 0.85rem;
          color: #0f172a;
          text-transform: uppercase;
          line-height: 1.2;
        }

        .signature-title {
          font-size: 0.75rem;
          color: #64748b;
          font-style: italic;
          line-height: 1.2;
        }

        .cert-footer {
          font-family: var(--font-mono);
          font-size: 0.75rem;
          color: #94a3b8;
          border-top: 1px solid rgba(197, 160, 89, 0.1);
          padding-top: 10px;
          z-index: 2;
          position: relative;
        }

        /* ================= Estilos de Impresión Fijos ================= */
        @page {
          size: A4 landscape; /* Fuerza orientación horizontal */
          margin: 0;
        }

        @media print {
          /* Desactivar efectos de scanlines y cuadrícula globales al imprimir */
          body::before, body::after, html::before, html::after {
            display: none !important;
            content: none !important;
          }
          
          .cyber-grid {
            display: none !important;
          }

          html, body {
            width: 100% !important;
            height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            background: #ffffff !important;
            color: #000000 !important;
            overflow: hidden !important;
          }
          
          * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }
          
          .cert-page-wrapper {
            background: #ffffff !important;
            padding: 0 !important;
            margin: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
          }

          .action-bar {
            display: none !important;
          }

          /* Forzar a ocupar exactamente una página A4 horizontal sin recortarse */
          .certificate-container {
            width: 297mm !important; /* Ancho A4 estándar */
            height: 210mm !important; /* Alto A4 estándar */
            padding: 30px 45px !important;
            margin: 0 !important;
            border: 15px double #c5a059 !important;
            box-shadow: none !important;
            background: #fdfbf7 !important;
            position: relative !important;
            box-sizing: border-box !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
            page-break-inside: avoid !important;
          }
        }
      `}</style>

      {/* Barra de Acciones */}
      <div className="action-bar no-print">
        <button onClick={() => router.push('/')} className="btn-cyber">
          &lt; VOLVER
        </button>
        <button onClick={() => window.print()} className="btn-cyber glow-green">
          IMPRIMIR CERTIFICADO 🖨️
        </button>
      </div>

      {/* Certificado Físico */}
      <div className="certificate-container">
        <div className="cert-watermark">SECURED</div>

        <div className="cert-header">Simulador Cyber Rescue</div>
        <div className="cert-logo">ACREDITACIÓN DE COMPETENCIA</div>
        
        <h3 className="cert-title">Certificado de Logro</h3>
        
        <p className="cert-recipient-intro">El presente reconocimiento se otorga con honor a:</p>
        <h2 className="cert-name">{data.player_name}</h2>
        
        <p className="cert-body">
          Por haber completado con éxito la simulación de mitigación de amenazas virtuales en <strong>Cyber Rescue</strong>, 
          logrando una puntuación destacada de <strong>{data.score} PTS</strong> y logrando erradicar el 
          malware <i>virus</i> en un tiempo récord de <strong>{formatTime(data.time_left)}</strong>.
        </p>

        <div className="cert-skills-badge">
          Demostrando conocimientos base en el uso de la terminal de comandos de seguridad, auditoría de registros de log, inspección del árbol de procesos activos, aislamiento en cuarentena y mitigación efectiva de software malicioso.
        </div>

        {/* Sección de Firmas (3 Columnas) */}
        <div className="signatures-section">
          {/* Firma 1: Melanie */}
          <div className="signature-block">
            <div className="signature-image melanie">Melanie F.</div>
            <div className="signature-line">
              <div className="signature-name">Melanie Fernanda</div>
              <div className="signature-title">Coordinadora de Seguridad 3C</div>
            </div>
          </div>

          {/* Firma 2: Rodrigo Rosa */}
          <div className="signature-block">
            <div className="signature-image rodrigo">Adrián</div>
            <div className="signature-line">
              <div className="signature-name">Rodrigo Rosa</div>
              <div className="signature-title">Coordinador de Desarrollo 3C</div>
            </div>
          </div>

          {/* Firma 3: Rodrigo Lemus */}
          <div className="signature-block">
            <div className="signature-image lemus">Rodrigo L.</div>
            <div className="signature-line">
              <div className="signature-name">Rodrigo Lemus</div>
              <div className="signature-title">Coordinador de Infraestructura 3C</div>
            </div>
          </div>
        </div>

        {/* Pie del certificado */}
        <div className="cert-footer">
          Patrocinado por Estudiantes de Desarrollo de Software 3C — Colegio Español Padre Arrupe
          <br />
          San Salvador, {formatDate(data.created_at)}
        </div>
      </div>
    </div>
  );
}
