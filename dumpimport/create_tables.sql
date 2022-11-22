create table entities (id text, type text, data jsonb) partition by list (type);
create table communities_infrastructures partition of entities for values in ('communities_infrastructures');
create table datasets partition of entities for values in ('dataset');
create table datasources partition of entities for values in ('datasource');
create table organizations partition of entities for values in ('organization');
create table other_research_products partition of entities for values in ('other_research_product');
create table projects partition of entities for values in ('project');
create table publications partition of entities for values in ('publication');
create table software partition of entities for values in ('software');
create table relations (sourceid text, targetid text, reltype text, data jsonb not null);

-- preferably after data ingestion
create index communities_infrastructures_id_idx on communities_infrastructures using btree(id);
create index datasets_id_idx on datasets using brin(id);
create index datasources_id_idx on datasources using btree(id);
create index organizations_id_idx on organizations using btree(id);
create index other_research_products_id_idx on other_research_products using brin(id);
create index projects_id_idx on projects using btree(id);
create index publications_id_idx on publications using brin(id);
create index software_id_idx on software using btree(id);
create index relations_sourceid_idx on relations using brin(sourceid);
create index relations_targetid_idx on relations using brin(targetid);
create index relations_reltype_idx on relations using brin(reltype);

