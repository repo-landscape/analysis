create table entities (id text, type text, data jsonb, primary key (id, type)) partition by list (type);
create table communities_infrastructures partition of entities for values in ('communities_infrastructures');
create table datasets partition of entities for values in ('dataset');
create table datasources partition of entities for values in ('datasource');
create table organizations partition of entities for values in ('organization');
create table other_research_products partition of entities for values in ('other_research_product');
create table projects partition of entities for values in ('project');
create table publications partition of entities for values in ('publication');
create table software partition of entities for values in ('software');
create table relations (sourceid text, targetid text, reltype text, data jsonb not null, primary key (sourceid, targetid));
