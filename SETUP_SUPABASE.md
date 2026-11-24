# Setup del nuovo database Supabase — Sudoku AI · Icons Edition

Questa edizione usa un **progetto Supabase tutto suo**: i progressi non sono condivisi con la versione pinguino né con quella gatto.

## Cosa devi fare tu

### A. Creare il progetto

1. Vai su https://database.new e crea un progetto (nome suggerito: `sudoku-ai-icons`).
2. Segna la **regione** e imposta una password database (salvala, ma **non mandarmela**).
3. Quando è pronto, apri **Project Settings → API** e copia:
   - **Project URL**: `https://xxxxxxxx.supabase.co`
   - **publishable key**: `sb_publishable_...`
4. In **Authentication → URL Configuration → Additional Redirect URLs** aggiungi esattamente:

```
it.sudokuvision.icons://login-callback
```

5. In **Authentication → Providers → Email** abilita Email. Per il login con password disattiva “Confirm email”; per il magic link lasciala attiva.

### B. Creare la tabella e le policy RLS

Apri **SQL Editor → New query**, incolla tutto il contenuto di `supabase/schema.sql` e premi **Run**. Crea la tabella `player_progress` con Row Level Security: ogni utente vede solo la propria riga.

### C. Inserire la chiave Gemini nei Secrets

Prendi la chiave da **Google AI Studio → Get API key** (non condividerla in chat). Poi scegli uno dei due modi:

**Dashboard:** Supabase → **Edge Functions → Secrets** → `Add secret`

- Name: `GEMINI_API_KEY`
- Value: la tua chiave `AIza...`

**CLI:**

```powershell
supabase login
supabase link --project-ref <REF>
supabase secrets set GEMINI_API_KEY=AIza...
```

Il modello predefinito è `gemini-3.6-flash`; la funzione ha fallback automatico a `gemini-3.5-flash-lite` e `gemini-3.8-flash`. Puoi cambiare modello con `GEMINI_MODEL` sempre nei Secrets.

### D. Deployare la Edge Function

Con la CLI, dalla root del progetto:

```powershell
supabase functions deploy gemini-proxy --no-verify-jwt
```

Il `--no-verify-jwt` è necessario perché l'app chiama la funzione con la publishable key, non con un JWT utente.

### E. Verificare

```powershell
$key = "sb_publishable_..."
$ref = "xxxxxxxx"

Invoke-RestMethod `
  -Uri "https://$ref.supabase.co/functions/v1/gemini-proxy/api/status" `
  -Headers @{ apikey = $key; Authorization = "Bearer $key" }
```

Risposta attesa:

```json
{ "configured": true, "model": "gemini-3.6-flash" }
```

Se vedi `configured: false`, la chiave non è nei Secrets oppure il deploy non è andato a buon fine.

## Cosa mandarmi

Mandami **solo** queste tre cose:

1. `Project URL` — `https://xxxxxxxx.supabase.co`
2. `publishable key` — `sb_publishable_...`
3. Conferma che `/api/status` risponde `configured: true`

**Non mandarmi:**
- `service_role` key
- password del database
- chiave Gemini
- token GitHub

Con quei valori ricompilo:

```powershell
.\scripts\build-apk.ps1 `
  -SupabaseUrl "https://xxxxxxxx.supabase.co" `
  -SupabaseKey "sb_publishable_..."
```

e consegno `Sudoku-AI-Icons.apk` aggiornato, con OCR online, account e sync attivi.

> Se hai incollato la chiave Gemini in una chat, ruotala su Google AI Studio e usa la nuova nei Supabase Secrets.
