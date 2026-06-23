import { sql } from '@vercel/postgres';
import fs from 'fs';
import path from 'path';
import { initializeApp, getApps, getApp } from 'firebase/app';
import { getFirestore, collection, addDoc, getDocs, query, orderBy, limit, Timestamp } from 'firebase/firestore';

export interface Score {
  id?: number | string;
  player_name: string;
  score: number;
  time_left: number;
  status: string;
  password?: string;
  created_at?: string;
}

const FILE_DB_PATH = path.join(process.cwd(), 'scores_db.json');

// Inicializa el archivo local si no existe
function initFileDb() {
  if (!fs.existsSync(FILE_DB_PATH)) {
    fs.writeFileSync(FILE_DB_PATH, JSON.stringify([], null, 2), 'utf-8');
  }
}

// Obtener base de datos Firebase Firestore si está configurado
function getFirestoreDb() {
  const firebaseConfig = {
    apiKey: process.env.FIREBASE_API_KEY,
    authDomain: process.env.FIREBASE_AUTH_DOMAIN,
    projectId: process.env.FIREBASE_PROJECT_ID,
    storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.FIREBASE_APP_ID
  };

  const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();
  return getFirestore(app);
}

export async function getScores(): Promise<Score[]> {
  const useFirebase = !!process.env.FIREBASE_PROJECT_ID;
  const usePostgres = !useFirebase && !!process.env.POSTGRES_URL;

  if (useFirebase) {
    try {
      const db = getFirestoreDb();
      const scoresCol = collection(db, 'scores');
      // Consulta ordenada por score para evitar requerir un índice compuesto en la consola
      const q = query(scoresCol, orderBy('score', 'desc'), limit(100));
      const querySnapshot = await getDocs(q);
      
      const scoresList: Score[] = [];
      querySnapshot.forEach((doc) => {
        const data = doc.data();
        let createdStr = new Date().toISOString();
        if (data.created_at) {
          if (data.created_at instanceof Timestamp) {
            createdStr = data.created_at.toDate().toISOString();
          } else if (typeof data.created_at === 'string') {
            createdStr = data.created_at;
          }
        }
        scoresList.push({
          id: doc.id,
          player_name: data.player_name,
          score: Number(data.score),
          time_left: Number(data.time_left),
          status: data.status,
          password: data.password || "",
          created_at: createdStr
        });
      });

      // Ordenar en memoria para resolver desempates por mayor tiempo restante
      return scoresList.sort((a, b) => {
        if (b.score !== a.score) return b.score - a.score;
        return b.time_left - a.time_left;
      });
    } catch (e) {
      console.error("Error al consultar Firebase Firestore, usando respaldo de archivo local:", e);
    }
  }

  if (usePostgres) {
    try {
      // Intentar crear la tabla con la columna password
      await sql`
        CREATE TABLE IF NOT EXISTS scores (
          id SERIAL PRIMARY KEY,
          player_name VARCHAR(50) NOT NULL,
          score INTEGER NOT NULL,
          time_left INTEGER NOT NULL,
          status VARCHAR(20) NOT NULL,
          password VARCHAR(100) DEFAULT '',
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
      `;
      // Intentar alterar la tabla por si ya existía sin la columna password
      await sql`
        ALTER TABLE scores ADD COLUMN IF NOT EXISTS password VARCHAR(100) DEFAULT '';
      `;

      const { rows } = await sql`
        SELECT id, player_name, score, time_left, status, password, created_at
        FROM scores
        ORDER BY score DESC, time_left DESC, created_at DESC
        LIMIT 100;
      `;

      return rows.map(r => ({
        id: r.id,
        player_name: r.player_name,
        score: Number(r.score),
        time_left: Number(r.time_left),
        status: r.status,
        password: r.password || "",
        created_at: r.created_at ? new Date(r.created_at).toISOString() : new Date().toISOString()
      }));
    } catch (e) {
      console.error("Error al consultar Postgres, usando respaldo de archivo local:", e);
    }
  }

  // Respaldo de archivo local (Desarrollo / Offline)
  initFileDb();
  try {
    const data = fs.readFileSync(FILE_DB_PATH, 'utf-8');
    const scores: Score[] = JSON.parse(data);
    return scores.sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return b.time_left - a.time_left;
    });
  } catch (e) {
    console.error("Error al leer archivo local:", e);
    return [];
  }
}

export async function addScore(score: Score): Promise<void> {
  const useFirebase = !!process.env.FIREBASE_PROJECT_ID;
  const usePostgres = !useFirebase && !!process.env.POSTGRES_URL;

  if (useFirebase) {
    try {
      const db = getFirestoreDb();
      const scoresCol = collection(db, 'scores');
      await addDoc(scoresCol, {
        player_name: score.player_name,
        score: score.score,
        time_left: score.time_left,
        status: score.status,
        password: score.password || "",
        created_at: Timestamp.fromDate(new Date())
      });
      return;
    } catch (e) {
      console.error("Error al guardar en Firebase, usando respaldo de archivo local:", e);
    }
  }

  if (usePostgres) {
    try {
      await sql`
        CREATE TABLE IF NOT EXISTS scores (
          id SERIAL PRIMARY KEY,
          player_name VARCHAR(50) NOT NULL,
          score INTEGER NOT NULL,
          time_left INTEGER NOT NULL,
          status VARCHAR(20) NOT NULL,
          password VARCHAR(100) DEFAULT '',
          created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
      `;
      await sql`
        ALTER TABLE scores ADD COLUMN IF NOT EXISTS password VARCHAR(100) DEFAULT '';
      `;

      await sql`
        INSERT INTO scores (player_name, score, time_left, status, password)
        VALUES (${score.player_name}, ${score.score}, ${score.time_left}, ${score.status}, ${score.password || ''});
      `;
      return;
    } catch (e) {
      console.error("Error al guardar en Postgres, guardando en archivo local:", e);
    }
  }

  // Respaldo de archivo local (Desarrollo / Offline)
  initFileDb();
  try {
    const data = fs.readFileSync(FILE_DB_PATH, 'utf-8');
    const scores: Score[] = JSON.parse(data);
    scores.push({
      player_name: score.player_name,
      score: score.score,
      time_left: score.time_left,
      status: score.status,
      password: score.password || "",
      created_at: new Date().toISOString()
    });
    fs.writeFileSync(FILE_DB_PATH, JSON.stringify(scores, null, 2), 'utf-8');
  } catch (e) {
    console.error("Error al guardar en archivo local:", e);
  }
}
