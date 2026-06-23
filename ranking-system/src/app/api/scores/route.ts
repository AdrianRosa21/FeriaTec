import { NextRequest, NextResponse } from 'next/server';
import { getScores, addScore } from '@/lib/db';

export const dynamic = 'force-dynamic';

// Clave secreta para autorizar registros de puntuación
const API_KEY = process.env.RANKING_API_KEY || 'feriatec-secret-key-2026';

export async function GET() {
  try {
    const scores = await getScores();
    
    // Ocultar contraseñas del GET público para evitar problemas de seguridad
    const publicScores = scores.map(s => ({
      id: s.id,
      player_name: s.player_name,
      score: s.score,
      time_left: s.time_left,
      status: s.status,
      created_at: s.created_at
    }));

    return NextResponse.json(publicScores, { status: 200 });
  } catch (error: any) {
    console.error("Error en GET /api/scores:", error);
    return NextResponse.json({ error: 'Error al obtener puntuaciones' }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    // Validar autenticación
    const authHeader = req.headers.get('authorization');
    if (!authHeader) {
      return NextResponse.json({ error: 'No autorizado: Cabecera Authorization ausente' }, { status: 401 });
    }

    const token = authHeader.replace(/^Bearer\s+/i, '').trim();
    if (token !== API_KEY) {
      return NextResponse.json({ error: 'No autorizado: Clave de API inválida' }, { status: 401 });
    }

    // Obtener y validar el cuerpo
    const body = await req.json();
    const { player_name, score, time_left, status, password } = body;

    if (!player_name || typeof player_name !== 'string' || player_name.trim() === '') {
      return NextResponse.json({ error: 'Alias de jugador inválido' }, { status: 400 });
    }

    if (typeof score !== 'number' || score < 0) {
      return NextResponse.json({ error: 'Puntuación inválida (debe ser número >= 0)' }, { status: 400 });
    }

    if (typeof time_left !== 'number') {
      return NextResponse.json({ error: 'Tiempo restante inválido' }, { status: 400 });
    }

    if (!status || typeof status !== 'string') {
      return NextResponse.json({ error: 'Estado del juego inválido' }, { status: 400 });
    }

    if (!password || typeof password !== 'string' || password.length < 4) {
      return NextResponse.json({ error: 'Contraseña inválida (mínimo 4 caracteres)' }, { status: 400 });
    }

    // Agregar puntuación a la base de datos (con fallback local)
    await addScore({
      player_name: player_name.trim(),
      score,
      time_left,
      status: status.toUpperCase(),
      password: password
    });

    return NextResponse.json({ message: 'Puntuación registrada con éxito' }, { status: 201 });
  } catch (error: any) {
    console.error("Error en POST /api/scores:", error);
    return NextResponse.json({ error: 'Error al registrar puntuación', details: error.message }, { status: 500 });
  }
}
