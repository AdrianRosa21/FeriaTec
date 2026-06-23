import { NextRequest, NextResponse } from 'next/server';
import { getScores } from '@/lib/db';

export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    const { id, password } = await req.json();

    if (!id || !password) {
      return NextResponse.json({ error: 'Faltan parámetros requeridos: id o contraseña' }, { status: 400 });
    }

    const scores = await getScores();
    
    // Buscar la puntuación por ID
    const scoreRecord = scores.find(s => String(s.id) === String(id));

    if (!scoreRecord) {
      return NextResponse.json({ error: 'Registro de puntuación no encontrado' }, { status: 404 });
    }

    // Verificar si el jugador ganó (requisito solicitado para descargar certificado)
    if (scoreRecord.status !== 'VICTORIA') {
      return NextResponse.json({ error: 'Solo los jugadores victoriosos pueden descargar el certificado' }, { status: 400 });
    }

    // Verificar contraseña
    if (scoreRecord.password !== password) {
      return NextResponse.json({ error: 'Contraseña del certificado incorrecta' }, { status: 401 });
    }

    // Si coincide, retornar los datos necesarios para renderizar el certificado
    return NextResponse.json({
      success: true,
      player_name: scoreRecord.player_name,
      score: scoreRecord.score,
      time_left: scoreRecord.time_left,
      created_at: scoreRecord.created_at
    }, { status: 200 });

  } catch (error: any) {
    console.error("Error en POST /api/scores/verify:", error);
    return NextResponse.json({ error: 'Error interno en el servidor de verificación' }, { status: 500 });
  }
}
