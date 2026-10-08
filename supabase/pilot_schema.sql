-- 5D-Pilotstudie: Tabelle für pseudonyme Datenspenden
-- Einmalig im Supabase-Dashboard unter "SQL Editor" ausführen
-- (Projekt in der Region "Central EU (Frankfurt)").
--
-- Sicherheitsmodell:
--   * Die Teilnahme-Seite nutzt den öffentlichen anon-Schlüssel. Er darf NUR neue
--     Zeilen einfügen (INSERT), und zwar nur mit approved = false.
--     Kein SELECT, kein UPDATE, kein DELETE.
--   * Freigabe (approved = true) setzt nur der Projektverantwortliche im Dashboard.
--   * Der Export in den öffentlichen Datensatz liest mit dem service_role-Schlüssel,
--     der ausschließlich als GitHub-Secret hinterlegt ist.

create table if not exists public.pilot_submissions (
    participant_code text primary key
        check (participant_code ~ '^[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}$'),
    -- Nur der Monat, keine genaue Uhrzeit (erschwert Verknüpfung mit Server-Protokollen).
    submitted_month date not null default date_trunc('month', now())::date,
    age_group text not null default ''
        check (age_group in ('', '18-24', '25-34', '35-44', '45-54', '55-64', '65+')),
    attention_ok boolean not null,
    imp smallint[] not null
        check (cardinality(imp) = 25 and imp <@ '{1,2,3,4,5}'::smallint[]),
    swls smallint[] not null
        check (cardinality(swls) = 5 and swls <@ '{1,2,3,4,5,6,7}'::smallint[]),
    schema_version smallint not null default 1 check (schema_version = 1),
    approved boolean not null default false
);

comment on table public.pilot_submissions is
    '5D-Pilotstudie: pseudonyme Datenspenden. Freigabe über die Spalte approved.';

alter table public.pilot_submissions enable row level security;

-- Alle Standardrechte entziehen, dann nur INSERT erlauben.
revoke all on table public.pilot_submissions from anon, authenticated;
-- Spaltengenau: approved, submitted_month und schema_version kann anon nicht selbst setzen.
grant insert (participant_code, age_group, attention_ok, imp, swls)
    on table public.pilot_submissions to anon;

drop policy if exists "anon darf nur unfreigegeben einfuegen" on public.pilot_submissions;
create policy "anon darf nur unfreigegeben einfuegen"
    on public.pilot_submissions
    for insert
    to anon
    with check (approved = false and schema_version = 1);

-- Kontrolle (sollte nur INSERT für anon zeigen):
-- select grantee, privilege_type from information_schema.role_table_grants
--  where table_name = 'pilot_submissions';
