'use client';

import React, { useState, useEffect } from 'react';
import styles from './page.module.css';

interface Score {
  id?: string;
  player_name: string;
  score: number;
  time_left: number;
  status: string;
  created_at: string;
}

export default function LeaderboardPage() {
  const [scores, setScores] = useState<Score[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Función para obtener las puntuaciones
  const fetchScores = async (showSpinner = false) => {
    if (showSpinner) setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/scores');
      if (!res.ok) {
        throw new Error(`Código de estado HTTP: ${res.status}`);
      }
      const data = await res.json();
      setScores(data);
    } catch (e: any) {
      console.error("Error al obtener scores:", e);
      setError(e.message || 'Error al conectar con la base de datos de ranking.');
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  };

  // Carga inicial y encuesta en segundo plano cada 5 segundos
  useEffect(() => {
    fetchScores(true);
    const interval = setInterval(() => {
      fetchScores(false);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleManualRefresh = () => {
    setIsRefreshing(true);
    fetchScores(false);
  };

  // Filtrado de puntuaciones según el término de búsqueda
  const filteredScores = scores.filter(item =>
    item.player_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Cálculo de estadísticas globales
  const totalPlays = scores.length;
  const maxScore = scores.length > 0 ? Math.max(...scores.map(s => s.score)) : 0;
  
  const victories = scores.filter(s => s.status === 'VICTORIA');
  const mitigationRate = totalPlays > 0 ? Math.round((victories.length / totalPlays) * 100) : 0;

  const averageTimeSecs = victories.length > 0
    ? Math.round(victories.reduce((acc, curr) => acc + curr.time_left, 0) / victories.length)
    : 0;

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
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    } catch {
      return '-';
    }
  };

  return (
    <main className={styles.container}>
      {/* Cabecera */}
      <header className={styles.header}>
        <h1 className={`${styles.title} glow-green`}>Cyber Rescue</h1>
        <div className={styles.subtitle}>
          <span className={styles.heartbeat}></span>
          <span>MONITOR DE RANKING EN VIVO</span>
        </div>
      </header>

      {/* Tarjetas de Estadísticas Globales */}
      <section className={styles.statsGrid}>
        <div className={`${styles.statCard} cyber-panel`}>
          <div className={styles.statTitle}>Simulaciones Totales</div>
          <div className={`${styles.statValue} glow-green`}>{totalPlays}</div>
        </div>
        <div className={`${styles.statCard} ${styles.secondary} cyber-panel`}>
          <div className={styles.statTitle}>Record de Puntuación</div>
          <div className={`${styles.statValue} glow-yellow`}>{maxScore} PTS</div>
        </div>
        <div className={`${styles.statCard} cyber-panel`}>
          <div className={styles.statTitle}>Eficacia de Mitigación</div>
          <div className={`${styles.statValue} glow-green`}>{mitigationRate}%</div>
        </div>
        <div className={`${styles.statCard} ${styles.danger} cyber-panel`}>
          <div className={styles.statTitle}>Tiempo Medio de Resolución</div>
          <div className={`${styles.statValue} glow-red`}>{formatTime(averageTimeSecs)}</div>
        </div>
      </section>

      {/* Controles de Búsqueda y Actualización */}
      <div className={styles.controls}>
        <div className={styles.searchWrapper}>
          <input
            type="text"
            className={styles.searchInput}
            placeholder="BUSCAR ESTUDIANTE / ALIAS..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <button 
          className="btn-cyber" 
          onClick={handleManualRefresh}
          disabled={isRefreshing}
        >
          {isRefreshing ? 'SINCRONIZANDO...' : 'SINCRONIZAR AHORA'}
        </button>
      </div>

      {/* Tabla de Leaderboard */}
      <section className={`${styles.tableWrapper} cyber-panel`}>
        {loading ? (
          <div className={styles.loading}>
            <div className={styles.spinner}></div>
            <p>CONECTANDO CON EL MAINFRAME DE CLASIFICACIÓN...</p>
          </div>
        ) : error ? (
          <div className={styles.empty}>
            <p className="glow-red">[!] ERROR: {error}</p>
            <button className="btn-cyber" style={{ marginTop: '15px' }} onClick={() => fetchScores(true)}>
              REINTENTAR CONEXIÓN
            </button>
          </div>
        ) : filteredScores.length === 0 ? (
          <div className={styles.empty}>
            <p>NO SE ENCONTRARON REGISTROS DE PUNTUACIONES EN EL SISTEMA.</p>
          </div>
        ) : (
          <table className={styles.table}>
            <thead>
              <tr>
                <th style={{ width: '80px' }}>Rank</th>
                <th>Estudiante</th>
                <th>Puntuación</th>
                <th>Tiempo Restante</th>
                <th>Estatus</th>
                <th>Marca de Tiempo</th>
              </tr>
            </thead>
            <tbody>
              {filteredScores.map((score, index) => {
                const rank = index + 1;
                let rankClass = styles.rankNormal;
                if (rank === 1) rankClass = styles.rank1;
                else if (rank === 2) rankClass = styles.rank2;
                else if (rank === 3) rankClass = styles.rank3;

                const isWin = score.status === 'VICTORIA';

                return (
                  <tr key={index}>
                    <td>
                      <span className={`${styles.rankBadge} ${rankClass}`}>
                        {rank}
                      </span>
                    </td>
                    <td style={{ fontWeight: 'bold', letterSpacing: '0.5px' }}>
                      {score.player_name.toUpperCase()}
                    </td>
                    <td className={isWin ? 'glow-green' : ''} style={{ fontWeight: 'bold' }}>
                      {score.score} PTS
                    </td>
                    <td>
                      {isWin ? formatTime(score.time_left) : '-'}
                    </td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <span className={`${styles.statusBadge} ${isWin ? styles.statusWin : styles.statusLose}`}>
                          {score.status}
                        </span>
                        {isWin && (
                          <a 
                            href={`/certificate/${score.id}`}
                            className="btn-cyber"
                            style={{
                              padding: '4px 10px',
                              fontSize: '0.70rem',
                              letterSpacing: '1px',
                              textDecoration: 'none',
                              borderWidth: '1px'
                            }}
                          >
                            CERTIFICADO
                          </a>
                        )}
                      </div>
                    </td>
                    <td style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                      {formatDate(score.created_at)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}
