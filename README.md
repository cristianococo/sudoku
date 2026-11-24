# Sudoku AI — Icons Edition

App Android (Flutter) che fotografa un Sudoku cartaceo, lo digitalizza con **Gemini** tramite una **Supabase Edge Function**, permette la correzione manuale della griglia 9×9 e offre un tutor logico in italiano (suggerimento spiegato, hint progressivi, risoluzione completa).

Questa è la terza edizione: stesso gameplay delle versioni precedenti, ma **nessuna mascotte animale**. Usa icone Material standard (`photo_camera`, `grid_on`, `school`, `person`) e una palette **indigo / ciano / ambra**, diversa sia dal verde-pinguino sia dal rosa-gatto.

> **Stato attuale:** APK ricompilato con Project URL e publishable key del **nuovo progetto dedicato**. Provider Email attivo e tabella `player_progress` presente (vuota). Edge Function `gemini-proxy` deployata e verificata: `/api/status` risponde `configured: true` con modello `gemini-3.6-flash`.

La chiave Gemini **non è nell'APK**: resta nei **Supabase Secrets** e viene usata solo dalla funzione `supabase/functions/gemini-proxy`.

## Identità della build

| Elemento | Valore |
|---|---|
| Nome app | **Sudoku AI** |
| Dart package | `sudoku_ai_icons` |
| Android applicationId | `it.sudokuvision.ai_sudoku_icons` |
| Deep link magic link | `it.sudokuvision.icons://login-callback` |
| APK | `Sudoku-AI-Icons.apk` |
| Database | nuovo progetto Supabase dedicato (vedi `SETUP_SUPABASE.md`) |

## Struttura

```
.
├── app/                 # Progetto Flutter compilabile (copia generata da app_src/)
│   └── android/         # Manifest e Gradle: applicationId, label, deep link, icona
├── app_src/             # SORGENTE CANONICA: lib/, test/, assets/
│   ├── lib/main.dart                 # navigazione Foto / Livelli / Impara / Profilo
│   ├── lib/screens/*.dart            # home, livelli, lezioni, profilo
│   ├── lib/core/*.dart               # API, prefs, solver, livelli, cloud sync, OCR locale
│   └── lib/ui/*.dart                 # icone Material, griglia, tema, nav
├── scripts/
│   ├── build-apk.ps1                 # copia app_src/ → app/, test, build, copia APK
│   └── generate_relazione.py         # genera RELAZIONE.html e RELAZIONE.pdf (2 pagine)
├── supabase/
│   ├── schema.sql                    # tabella player_progress + RLS
│   └── functions/gemini-proxy/       # OCR + spiegazioni lato server
├── docs/                             # diagrammi per la relazione
├── logo.jpg                          # logo generico Sudoku (griglia 9×9 + badge AI)
├── SETUP_SUPABASE.md                 # guida per il nuovo database e la chiave Gemini
├── .env.example                      # solo riferimento, senza segreti reali
├── RELAZIONE.md
└── RELAZIONE.pdf
```

## Prerequisiti

- Flutter SDK stable con Android SDK installato
- Java 17 (richiesto da Gradle)
- Supabase CLI (solo per configurare il nuovo progetto e deployare la funzione)
- Una chiave Google AI Studio (Gemini API), da inserire **solo** nei Supabase Secrets

## 1. Configurare il nuovo database e Gemini

Segui **`SETUP_SUPABASE.md`**. In sintesi:

```powershell
supabase login
supabase link --project-ref <REF_DEL_NUOVO_PROGETTO>
# SQL Editor: esegui supabase/schema.sql
supabase secrets set GEMINI_API_KEY=LA_TUA_CHIAVE_GEMINI
supabase functions deploy gemini-proxy --no-verify-jwt
```

Verifica:

```powershell
$key = "sb_publishable_..."
Invoke-RestMethod `
  -Uri "https://<REF>.supabase.co/functions/v1/gemini-proxy/api/status" `
  -Headers @{ apikey = $key; Authorization = "Bearer $key" }
```

Deve rispondere con `configured: true`. Se la chiave manca, la funzione risponde 503 e l'app passa da sola all'**OCR locale Tesseract**.

## 2. Compilare l'APK

Build già eseguita con URL e chiave del nuovo progetto:

```powershell
.\scripts\build-apk.ps1
```

Se cambi progetto o chiave, ricompila con:

```powershell
.\scripts\build-apk.ps1 `
  -SupabaseUrl "https://<REF>.supabase.co" `
  -SupabaseKey "sb_publishable_..."
```

Lo script esegue `pub get`, i test, la build release e copia l'APK in `Sudoku-AI-Icons.apk`. La chiave publishable è pubblica by design e può stare nell'APK; **mai** la `service_role` o la chiave Gemini.

## 3. Account e cloud sync

Nel nuovo progetto Supabase:

1. Esegui `supabase/schema.sql` in **SQL Editor** (crea `player_progress` con RLS).
2. Abilita **Authentication → Providers → Email**.
3. Aggiungi in **Authentication → URL Configuration → Additional Redirect URLs**:

```
it.sudokuvision.icons://login-callback
```

4. In **Project Settings → API** copia **Project URL** e **publishable key** e mandameli per la rebuild.

Il nome del giocatore si può impostare anche offline; con account viene sincronizzato in `player_progress.settings->>'display_name'`. Ogni utente legge/scrive solo la propria riga grazie a RLS.

## Funzionalità

**Base**
- Acquisizione da fotocamera o galleria; un solo pulsante **Riconosci griglia** prova Gemini e, se non risponde, passa da solo a Tesseract.
- Griglia 9×9 correggibile, cifre lette evidenziate in blu, conflitti rossi, separatori neri tra blocchi 3×3.
- Nei **Livelli**: numeri dati bloccati, barra 1–9, tocco su un numero evidenzia tutte le occorrenze, nessuna tastiera sistema.
- 3 cuori con errore immediato: il numero sbagliato non resta, la cella lampeggia e si perde un cuore; a 0 cuori appare **Riprova**.
- Massimo **3 suggerimenti** per livello, con contatore; il suggerimento compila una cella corretta.
- Riga/colonna/blocco completati cadono come domino e restano verdi; annulla/cancella ripristina il colore.
- Il pulsante **Gioca come nei Livelli** usa lo stesso motore sulla griglia digitalizzata (senza XP).
- Tre pulsanti colorati: **Risolvi** (ambra), **Suggerimento** (ciano), **Tutor** (indigo), sempre con etichetta visibile.
- Hint progressivi: blocco 3×3 → cella e vincoli → numero spiegato.
- Tutor vocale `flutter_tts` in `it-IT`; nessun messaggio SnackBar durante il gioco.

**Bonus**
- Solutore ibrido: backtracking MRV esatto in Dart/TypeScript; Gemini solo per le spiegazioni.
- 8 livelli offline con stelle, XP e tempi migliori; 6 lezioni guidate interattive.
- Overlay AR lite con i numeri mancanti disegnati sopra la foto.
- **Icone Material standard** per tutor (griglia/lampadina/controllo/errore) e per la navigazione; palette indigo/ciano/ambra, nessun animale.
- Profilo con nome modificabile, salvataggio `Ciao, <nome>!`, **Modifica nome**, login email/password o magic link.

## Test e report

```powershell
cd app
flutter test        # 25 test
```

`RELAZIONE.pdf` è generato da `python scripts/generate_relazione.py` (2 pagine A4). Gli screenshot reali dal dispositivo saranno aggiunti dopo l'installazione della build finale.
