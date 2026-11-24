# Sudoku AI · Icons Edition — Relazione tecnica

**Versione stampabile (2 pagine A4):** [RELAZIONE.pdf](RELAZIONE.pdf) · **Stato:** build locale completa; database e Edge Function verificati.

SDK: Flutter + Android SDK · API: Google Gemini · Backend: Supabase Edge Function

## 1. Obiettivo

App Android installabile che fotografa un Sudoku cartaceo incompleto, digitalizza la matrice 9×9 tramite Gemini, consente la correzione manuale e offre un tutor logico in italiano (suggerimento spiegato, hint progressivi, risoluzione completa). Complementano l'esperienza 8 livelli didattici e 6 lezioni guidate, giocabili anche offline.

Questa edizione mantiene le stesse funzionalità delle precedenti ma sostituisce le mascotte con **icone Material standard** e adotta una palette **indigo / ciano / ambra**, così non sembra la versione pinguino né quella gatto.

## 2. Architettura scelta

`Foto → Flutter → Supabase Edge Function (gemini-proxy) → Gemini API`.

La chiave Gemini (`GEMINI_API_KEY`) risiede **solo nei Supabase Secrets**: non è nell'APK e non è in `.env`. L'app invia la publishable key come header `apikey` / `Bearer`; URL e chiave sono iniettati a build time con `--dart-define`. Il nuovo progetto Supabase fornisce anche Auth (magic link PKCE o email/password) e il sync dei progressi con Row Level Security. La `service_role` non è mai inclusa.

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
| Livelli e lezioni | 8 puzzle a soluzione unica, 3 cuori, errore immediato, cascade domino, XP/stelle; 6 lezioni interattive |
| UI e account | Palette indigo/ciano/ambra, linee nere 3×3, griglia della foto giocabile come i Livelli, nome modificabile e cloud sync RLS |

## 5. Identità visiva

![Logo Sudoku AI](logo.jpg)
*Figura 2 — Logo generico: griglia 9×9 con cifre date e badge “AI”. Nessuna mascotte animale.*

Screenshot reali dal dispositivo saranno inclusi dopo l'installazione della build con il database dedicato.

## 6. Test e risultati

- `flutter test`: **25 test superati** (solver, OCR, JSON, sync, navigazione, gameplay, griglia digitalizzata).
- `flutter build apk --release`: APK `Sudoku-AI-Icons.apk`, Android 8+ (minSdk 24).
- `GET /api/status`: verificato `configured: true`, modello `gemini-3.6-flash`, fallback `gemini-3.5-flash-lite` e `gemini-3.8-flash`.

## Consegna

- [x] Copia sorgente locale completata
- [x] Icone Material e palette dedicata
- [x] `.env.example` senza chiave reale
- [x] Guida `SETUP_SUPABASE.md` per database e Secrets
- [x] Relazione tecnica in 2 pagine: `RELAZIONE.pdf`
- [x] URL + publishable key del nuovo database
- [x] APK con URL/chiave incluse
- [x] Deploy di `gemini-proxy` con `GEMINI_API_KEY` e verifica `configured: true`
- [ ] Screenshot reali e pubblicazione (su richiesta)

Il PDF si rigenera con `python scripts/generate_relazione.py`.
