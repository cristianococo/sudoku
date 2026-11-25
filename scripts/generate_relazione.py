"""Genera RELAZIONE.html e RELAZIONE.pdf (max 2 pagine A4) per Sudoku AI Icons."""

from __future__ import annotations

import base64
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "logo.jpg"


def data_uri(path: Path) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


TEMPLATE = r"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Sudoku AI · Icons Edition - Relazione tecnica</title>
<style>
  @page { size: A4; margin: 12mm 13mm 10mm; }
  * { box-sizing: border-box; }
  html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { margin: 0; font-family: "Segoe UI", Arial, sans-serif; font-size: 8.8pt;
         line-height: 1.30; color: #20242b; }
  h1 { font-size: 16.5pt; line-height: 1.1; margin: 0 0 2pt; color: #3730a3; }
  .sub { font-size: 7.8pt; color: #626b76; margin: 0 0 7pt; }
  h2 { font-size: 10.4pt; color: #3730a3; margin: 8pt 0 4pt; padding-bottom: 2pt;
       border-bottom: 1.4px solid #dfe3f5; }
  p { margin: 0 0 4pt; }
  ol, ul { margin: 0 0 4pt; padding-left: 15pt; }
  li { margin-bottom: 1.6pt; }
  code { font-family: Consolas, "Courier New", monospace; font-size: 7.7pt;
         background: #f1f3fb; padding: 0 2pt; border-radius: 2pt; }
  table { border-collapse: collapse; width: 100%; font-size: 7.9pt; }
  th, td { border: 1px solid #d6dbe9; padding: 2.6pt 4pt; text-align: left;
           vertical-align: top; }
  th { background: #e9ebfa; color: #3730a3; }
  .page { page-break-after: always; }
  .page:last-child { page-break-after: auto; }
  .flow { display: flex; align-items: stretch; gap: 3pt; margin: 3pt 0 6pt; }
  .flow .box { flex: 1; border: 1px solid #c8cfeb; border-radius: 4pt;
               background: #f6f7fd; padding: 4pt 5pt; text-align: center; }
  .flow .box b { display: block; color: #3730a3; font-size: 8pt; }
  .flow .box span { font-size: 7pt; color: #58636c; }
  .flow .arrow { align-self: center; color: #3730a3; font-weight: bold; }
  .identity { display: flex; align-items: center; gap: 9pt; margin-top: 4pt; }
  .identity img { width: 34mm; height: 34mm; object-fit: cover;
                  border: 1px solid #c8cfeb; border-radius: 5pt; }
  .identity .meta { flex: 1; font-size: 7.8pt; color: #4b5563; }
  .identity .meta b { color: #3730a3; }
  .foot { margin-top: 7pt; padding-top: 3pt; border-top: 1px solid #dfe3f5;
          font-size: 7.4pt; color: #68727c; display: flex; justify-content: space-between; }
</style>
</head>
<body>

<section class="page">
  <h1>Sudoku AI · Icons Edition</h1>
  <p class="sub">Relazione tecnica · database e Edge Function verificati · Flutter + Android SDK · Google Gemini API · Supabase Edge Function</p>

  <h2>1. Obiettivo</h2>
  <p>Applicazione Android installabile che acquisisce una foto di un Sudoku cartaceo incompleto, digitalizza la matrice 9×9 tramite Gemini, permette la correzione manuale e offre un tutor logico in italiano: suggerimento spiegato, hint progressivi e risoluzione completa. Complementano l'esperienza 8 livelli didattici e 6 lezioni guidate, giocabili anche offline. Questa edizione conserva le funzionalità delle precedenti ma usa icone Material standard e una palette indigo/ciano/ambra, senza mascotte animali.</p>

  <h2>2. Architettura scelta</h2>
  <p>Client Flutter → Supabase Edge Function <code>gemini-proxy</code> → Gemini API. La chiave Gemini (<code>GEMINI_API_KEY</code>) vive solo nei Supabase Secrets e non entra mai nell'APK. La funzione è deployata con verifica JWT: l'app crea una sessione anonima in silenzio e invia il token come <code>Bearer</code> insieme alla publishable key come <code>apikey</code>, senza cambiare l'interfaccia. Un contatore per utente accessibile solo alla funzione limita OCR e spiegazioni a 20 richieste al giorno. Il progetto Supabase fornisce Auth e sincronizzazione dei progressi con Row Level Security.</p>

  <div class="flow">
    <div class="box"><b>Foto</b><span>camera / galleria</span></div>
    <div class="arrow">→</div>
    <div class="box"><b>Flutter</b><span>UI, solver, OCR locale</span></div>
    <div class="arrow">→</div>
    <div class="box"><b>Edge Function</b><span>Secrets + validazione JSON</span></div>
    <div class="arrow">→</div>
    <div class="box"><b>Gemini</b><span>OCR + spiegazioni IT</span></div>
  </div>

  <ol>
    <li><b>Acquisizione:</b> <code>image_picker</code> apre fotocamera o galleria; l'immagine viene codificata in base64.</li>
    <li><b>Riconoscimento:</b> <code>POST /api/ocr</code> con Structured Outputs; la funzione valida una matrice 9×9 di interi 0–9. Se rete, funzione o chiave mancano, il client usa l'OCR locale Tesseract (modello <code>eng</code> incluso) e valida il risultato con il solutore.</li>
    <li><b>Verifica:</b> griglia 9×9 editabile, cifre lette in blu, conflitti in rosso, separatori neri tra i riquadri 3×3 e cornice esterna.</li>
    <li><b>Tutor:</b> <code>POST /api/explain</code> restituisce la spiegazione in italiano; senza rete viene generata localmente da regole logiche.</li>
    <li><b>Risoluzione:</b> backtracking esatto con MRV in Dart (e modulo TypeScript nella Edge Function): Gemini non calcola mai i numeri, solo le spiegazioni.</li>
    <li><b>Sync:</b> tabella <code>player_progress</code> con RLS per utente; magic link PKCE (<code>it.sudokuvision.icons://login-callback</code>) o email/password. La <code>service_role</code> non è mai inclusa.</li>
  </ol>

  <h2>3. Integrazione API e gestione JSON</h2>
  <p>Modello primario <code>gemini-3.6-flash</code>, con fallback <code>gemini-3.5-flash-lite</code> e <code>gemini-3.8-flash</code>. Schema OCR: <code>{ valid, grid: number[9][9], note }</code>. Schema spiegazione: <code>{ row, col, valore, spiegazione }</code>. La Edge Function rimuove le fence Markdown, esegue <code>JSON.parse</code>, verifica forma e valori e restituisce errori HTTP significativi (400 input non valido, 422 griglia inconsistente, 502 errore Gemini, 503 chiave mancante). L'URL della funzione è derivato da <code>SUPABASE_URL</code>, con override solo via <code>--dart-define</code>; nessuna schermata di configurazione è esposta all'utente.</p>

  <div class="foot"><span>Sudoku AI · Icons Edition — Relazione tecnica</span><span>Pagina 1/2</span></div>
</section>

<section class="page">
  <h2>4. Funzionalità bonus implementate</h2>
  <table>
    <thead><tr><th style="width:29%">Funzionalità</th><th>Implementazione</th></tr></thead>
    <tbody>
      <tr><td>Tutor vocale (Audio)</td><td><code>flutter_tts</code>, lingua <code>it-IT</code>, attivabile con il pulsante “Leggi”.</td></tr>
      <tr><td>Icone di stato (UI)</td><td><code>MoodIcon</code> con quattro icone Material: griglia, lampadina, controllo, errore. Navigazione con <code>photo_camera</code>, <code>grid_on</code>, <code>school</code>, <code>person</code>.</td></tr>
      <tr><td>Hint progressivi (Didattica)</td><td>Tre livelli: blocco 3×3 → cella e vincoli → numero con spiegazione. Massimo 3 suggerimenti per partita, con contatore.</td></tr>
      <tr><td>Solutore ibrido (Algoritmi)</td><td>Backtracking con MRV in Dart e TypeScript, 100% esatto; Gemini usato solo per la spiegazione testuale.</td></tr>
      <tr><td>Overlay AR lite</td><td>Canvas che sovrappone i numeri mancanti direttamente alla foto acquisita.</td></tr>
      <tr><td>OCR offline</td><td>Tesseract4Android con modello <code>eng</code> incluso; rilettura delle celle e validazione col solver. Nessuna rete e nessuna chiave richiesta.</td></tr>
      <tr><td>Livelli e lezioni</td><td>8 puzzle generati con soluzione unica garantita, 3 cuori con errore immediato, evidenziazione blu delle occorrenze, animazione domino, completamento automatico senza pulsante Controlla, XP/stelle e sblocchi; 6 lezioni interattive senza backend.</td></tr>
      <tr><td>UI e account</td><td>Palette indigo/ciano/ambra con linee nere tra i blocchi; griglia digitalizzata giocabile come i Livelli; nome mostrato come <code>Ciao, &lt;nome&gt;!</code> e modificabile da Profilo/Impostazioni; login Supabase e cloud sync protetto da RLS.</td></tr>
    </tbody>
  </table>

  <h2>5. Identità visiva</h2>
  <div class="identity">
    <img src="__LOGO__" alt="Logo Sudoku AI Icons">
    <div class="meta">
      <b>Logo generico Sudoku</b><br>
      Griglia 9×9 con cifre date e badge “AI”. Nessun pinguino, nessun gatto, nessuna mascotte animale.<br>
      <b>Package:</b> <code>sudoku_ai_icons</code><br>
      <b>ApplicationId:</b> <code>it.sudokuvision.ai_sudoku_icons</code><br>
      <b>Deep link:</b> <code>it.sudokuvision.icons://login-callback</code><br>
      Screenshot reali dal dispositivo saranno inclusi dopo l'installazione della build con database dedicato.
    </div>
  </div>

  <h2>6. Test e risultati</h2>
  <ul>
    <li><code>flutter test</code>: 26 test superati su solver, OCR, parsing JSON, sync cloud, navigazione, gameplay (cuori, suggerimenti, animazioni), griglia digitalizzata e header API protetti.</li>
    <li><code>flutter build apk --release</code>: <code>Sudoku-AI-Icons.apk</code> (Android 8+, minSdk 24), con Tesseract e librerie native incluse.</li>
    <li><code>GET /api/status</code>: verificato <code>configured: true</code>, modello <code>gemini-3.6-flash</code>, fallback <code>gemini-3.5-flash-lite</code> e <code>gemini-3.8-flash</code>.</li>
  </ul>
  <div class="foot"><span>Codice e guida setup: cartella locale sudoku_ai_icons</span><span>Pagina 2/2</span></div>
</section>

</body>
</html>
"""

logo_tag = (
    f'<img src="{data_uri(LOGO)}" alt="Logo Sudoku AI Icons">'
    if LOGO.exists()
    else ''
)
html = TEMPLATE.replace('<img src="__LOGO__" alt="Logo Sudoku AI Icons">', logo_tag)

html_path = ROOT / "RELAZIONE.html"
pdf_path = ROOT / "RELAZIONE.pdf"
html_path.write_text(html, encoding="utf-8")

chrome = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
if not chrome.exists():
    chrome = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

subprocess.run(
    [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        "--virtual-time-budget=5000",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ],
    check=True,
    capture_output=True,
)

from pypdf import PdfReader  # noqa: E402

reader = PdfReader(str(pdf_path))
print(f"HTML: {html_path}")
print(f"PDF:  {pdf_path} ({len(reader.pages)} pagine)")
for number, page in enumerate(reader.pages, 1):
    text = page.extract_text() or ""
    print(f"  pagina {number}: {len(text)} caratteri di testo")
