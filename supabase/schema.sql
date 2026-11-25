-- Esegui questo script una volta in Supabase -> SQL Editor -> New query.
-- Crea la tabella che memorizza progressi e impostazioni di ogni giocatore.

create table if not exists public.player_progress (
  user_id uuid primary key references auth.users(id) on delete cascade,
  progress jsonb not null default '{}'::jsonb,
  settings jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.player_progress enable row level security;

-- Ogni utente autenticato può leggere/scrivere SOLO la propria riga.
drop policy if exists "player_progress_select_own" on public.player_progress;
create policy "player_progress_select_own"
  on public.player_progress for select to authenticated
  using (auth.uid() = user_id);

drop policy if exists "player_progress_insert_own" on public.player_progress;
create policy "player_progress_insert_own"
  on public.player_progress for insert to authenticated
  with check (auth.uid() = user_id);

drop policy if exists "player_progress_update_own" on public.player_progress;
create policy "player_progress_update_own"
  on public.player_progress for update to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists "player_progress_delete_own" on public.player_progress;
create policy "player_progress_delete_own"
  on public.player_progress for delete to authenticated
  using (auth.uid() = user_id);

-- Contatore giornaliero per la Gemini Edge Function.
-- Solo la funzione (service_role) può leggerlo/scriverlo: nessuna policy per
-- anon/authenticated, quindi l'utente non può aggirare il limite.
create table if not exists public.gemini_usage (
  user_id uuid primary key references auth.users(id) on delete cascade,
  day date not null default current_date,
  requests integer not null default 0,
  updated_at timestamptz not null default now()
);

alter table public.gemini_usage enable row level security;
revoke all on public.gemini_usage from anon, authenticated;
