create table communities_infrastructures (id text primary key, data jsonb not null);
create table datasets (id text primary key, data jsonb not null);
create table datasources (id text primary key, data jsonb not null);
create table organizations (id text primary key, data jsonb not null);
create table other_research_products (id text primary key, data jsonb not null);
create table projects (id text primary key, data jsonb not null);
create table publications (id text primary key, data jsonb not null);
create table relations (sourceid text, targetid text, sourcetype text, targettype text, reltype text, data jsonb not null, primary key (sourceid, targetid));
create table software (id text primary key, data jsonb not null);
