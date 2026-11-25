# Sudoku AI · Icons Edition — Relazione tecnica

**Versione stampabile (2 pagine A4):** [RELAZIONE.pdf](RELAZIONE.pdf) · **Stato:** build locale completa; database e Edge Function verificati.

SDK: Flutter + Android SDK · API: Google Gemini · Backend: Supabase Edge Function

## 1. Obiettivo

App Android installabile che fotografa un Sudoku cartaceo incompleto, digitalizza la matrice 9×9 tramite Gemini, consente la correzione manuale e offre un tutor logico in italiano (suggerimento spiegato, hint progressivi, risoluzione completa). Complementano l'esperienza 8 livelli didattici e 6 lezioni guidate, giocabili anche offline.

Questa edizione mantiene le stesse funzionalità delle precedenti ma sostituisce le mascotte con **icone Material standard** e adotta una palette **indigo / ciano / ambra**, così non sembra la versione pinguino né quella gatto.

## 2. Architettura scelta

`Foto → Flutter → Supabase Edge Function (gemini-proxy) → Gemini API`.

La chiave Gemini (`GEMINI_API_KEY`) risiede **solo nei Supabase Secrets**: non è nell'APK e non è in `.env`. URL e publishable key sono iniettati a build time con `--dart-define`. La Edge Function è deployata con verifica JWT attiva: l'app crea una sessione anonima in silenzio all'avvio e invia il token come `Bearer`, oltre alla publishable key come `apikey`. Nessun popup o pulsante aggiuntivo: l'esperienza utente non cambia. Un contatore per utente (`gemini_usage`, accessibile solo alla funzione tramite `service_role`) limita OCR e spiegazioni a 20 richieste/giorno. Il progetto Supabase fornisce Auth (magic link PKCE o email/password) e sync dei progressi con Row Level Security; la `service_role` non è mai inclusa nell'APK.

1. **Acquisizione** — `image_picker` da fotocamera o galleria, immagine in base64.
2. **OCR** — `POST /api/ocr` con Structured Outputs; validazione di una matrice 9×9 di interi 0–9. Se rete/funzione/chiave mancano, scatta l'OCR locale Tesseract (modello `eng` incluso) validato dal solutore.
3. **Verifica** — griglia 9×9 editabile, cifre lette in blu, conflitti rossi, separatori neri tra i blocchi 3×3.
4. **Tutor** — `POST /api/explain` per la spiegazione in italiano; offline vengono usate regole locali.
5. **Risoluzione** — backtracking esatto con MRV in Dart e TypeScript: Gemini non calcola mai i numeri.
6. **Sync** — tabella `player_progress` con RLS per utente; deep link `it.sudokuvision.icons://login-callback`; nessuna UI di configurazione esposta all'utente.

![Architettura](docs/architettura.svg)
*Figura 1 — Architettura e solver ibrido.*

## 3. Integrazione API e JSON

Modello primario `gemini-3.6-flash`, fallback `gemini-3.5-flash-lite` e `gemini-3.8-flash`. Schema OCR: `{ valid, grid: number[9][9], note }`; schema spiegazione: `{ row, col, valore, spiegazione }`. La Edge Function rimuove le fence Markdown, esegue `JSON.parse`, valida forma e valori e restituisce errori HTTP 400/422/502/503.

## 4. Funzionalità bonus implementate

| Bonus | Implementazione |
|---|---|
| Tutor vocale | `flutter_tts` in `it-IT`, pulsante “Leggi” |
| Icone di stato | `MoodIcon` con quattro icone Material (griglia, lampadina, controllo, errore); navigazione con `photo_camera`, `grid_on`, `school`, `person` |
| Hint progressivi | Blocco → cella → numero spiegato; max 3 suggerimenti per partita |
| Solutore ibrido | Backtracking MRV in Dart/TypeScript, Gemini solo per spiegare |
| Overlay AR lite | Numeri mancanti sovrapposti alla foto |
| OCR offline | Tesseract4Android con modello `eng` incluso, senza rete né API key |
| Livelli e lezioni | 8 puzzle a soluzione unica, 3 cuori, errore immediato, cascade domino, completamento automatico senza pulsante Controlla, XP/stelle; 6 lezioni interattive |
| UI e account | Palette indigo/ciano/ambra, linee nere 3×3, griglia della foto giocabile come i Livelli; nome mostrato come `Ciao, <nome>!` e modificabile da Profilo/Impostazioni; cloud sync RLS |

## 5. Identità visiva

Identità visiva: icone Material standard con palette indigo/ciano/ambra; nessuna mascotte animale.

## 6. Screenshot dall'app

![Schermata Foto](foto.jpeg)
*Figura 1 — Foto: acquisizione da fotocamera/galleria e griglia digitalizzata.*

![Schermata Livelli](livelli.jpeg)
*Figura 2 — Livelli: puzzle, cuori, evidenziazioni e completamento automatico.*

![Schermata Impara](impara.jpeg)
*Figura 3 — Impara: lezioni guidate interattive.*

![Schermata Profilo](profilo.jpeg)
*Figura 4 — Profilo: nome salvato, Modifica nome e accesso Supabase.*


## 7. Test e risultati

- `flutter test`: **26 test superati** (solver, OCR, JSON, sync, navigazione, gameplay, griglia digitalizzata, header API protetti).
- `flutter build apk --release`: APK `Sudoku-AI-Icons.apk`, Android 8+ (minSdk 24).
- `GET /api/status`: verificato `configured: true`, modello `gemini-3.6-flash`, fallback `gemini-3.5-flash-lite` e `gemini-3.8-flash`; senza token `401`, con sessione anonima `200`.

## Consegna

- [x] Copia sorgente locale completata
- [x] Icone Material e palette dedicata
- [x] `.env.example` senza chiave reale
- [x] Configurazione Supabase, Secrets e README aggiornati
- [x] Relazione tecnica in 2 pagine con screenshot: `RELAZIONE.pdf`
- [x] URL + publishable key del nuovo database
- [x] APK con URL/chiave incluse
- [x] Deploy di `gemini-proxy` con `GEMINI_API_KEY` e verifica `configured: true`
- [x] Screenshot reali inclusi in `RELAZIONE.md`, `RELAZIONE.html` e `RELAZIONE.pdf`

Il PDF si rigenera con `python scripts/generate_relazione.py`.
