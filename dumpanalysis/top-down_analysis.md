## Communities infrastructures

### General info

* Id prefix: `00`
* Sample id: `00|context_____::3ee95893613de7450247d7fef747136f` (DARIAH EU)
* Total count: **13**

### Relations

| domain | relation | range | status |
| ------ | -------- | ----- | ------ |
| Community infrastructure  | IsRelatedTo | Datasource | exists |
|   | IsRelatedTo | Project | exists |
|   | IsRelatedTo | Research product | exists |
|   | IsRelatedTo | Community infrastructure | not exists |
|   | IsRelatedTo | Organization | not exists |

So for example, a community infrastructure such as [DARIAH EU](https://dariah.openaire.eu) can be related to:
* a project ([CENDARI](https://dariah.openaire.eu/search/project?grantId=284432&funder=EC)): `40|corda_______::6d15cb89d1e1d91c69299ad5f7e2b132`
* a datasource ([NAKALA](https://dariah.openaire.eu/search/dataprovider?datasourceId=re3data_____::f5b9831893a8aae2371f829870c149e8)): `10|re3data_____::f5b9831893a8aae2371f829870c149e8`
* a research product ([The Trouble With Big Data: How Datafication Displaces Cultural Practices](https://dariah.openaire.eu/search/publication?pid=10.5040%2F9781350239654)): `50|doi_dedup___::7646df520187212b1eca34d7b759d27f`

### Relevant instances

For our purposes, the following communities might be of interest, either for thematic or geographical narrowing:
* [Digital Humanities and Cultural Heritage](https://dh-ch.openaire.eu): `00|context_____::04a00617ca659adc944977ac700ea14b`
* [DARIAH EU](https://dariah.openaire.eu): `00|context_____::3ee95893613de7450247d7fef747136f`

### Finding ids of research products related to DH-CH

```sql
select * from relations
where sourceid = '00|context_____::04a00617ca659adc944977ac700ea14b' and targetid like '50%'
```

Total count is **5,029,081**.

- [ ] Check in what measure the research products found have subjects related to "digital humanities" and "cultural heritage".

### Finding ids of research products related to DARIAH EU

```sql
select * from relations
where sourceid = '00|context_____::3ee95893613de7450247d7fef747136f' and targetid like '50%'
```

Total count is **53,953**.

- [ ] Check from what countries these research products come.
- [ ] Check what subjects these research products display (especially related to "digital humanities").

## Organizations

### General info

* Id prefix: `20`
* Sample id: `20|pending_org_::2fecc0aa1080bef76b7cd9c7f8304393` (Österreichische Akademie der Wissenschaften - Austrian Centre for Digital Humanities (ACDH))
* Total count: **283,672**

### Relations

| domain | relation | range | status |
| ------ | -------- | ----- | ------ |
| Organization | isAuthorInstitutionOf | Research product | exists |
|   | isParticipant | Project | exists |
|   | provides | Datasource | exists |
|   | provides | Research product | not exists |

- [ ] Check also `isRelatedTo` with all possible combinations

### Which organizations do not have property "country"?

```sql
select count(*) from organizations o where data->>'country' is null
```

Organizations with no `country` property: **76,946** (about **27%** of the total)

### Check if organizations have both code and label for country

When an organization has a “country” property, it has both “code” and “label”.

Queries like:

```sql
select count(*) from organizations o
where data->'country'->>'code' is null
and data->'country'->>'label' is not null 
```

and

```sql
select count(*) from organizations o
where data->'country'->>'label' is null
and data->'country'->>'country' is not null
```

return `0`.

### Get all organizations with country AT

```sql
select id, data->'legalname' as name, data->'country' as country 
from organizations
where data->'country'->>'code' = 'AT'
or data->'country'->>'label' = 'Austria'
```

Total count: **2380**.

### Check if there are any inconsistencies between code and label for Austria

All organizations with code “AT” also have label “Austria”, and the inverse too. The following two queries return `0`:

```sql
select count(*) from organizations o
where data->'country'->>'code' = 'AT'
and data->'country'->>'label' != 'Austria'
```

```sql
select count(*) from organizations o
where data->'country'->>'code' != 'AT'
and data->'country'->>'label' = 'Austria' 
```

### Get all organizations with country ≠ Austria, but "Austria" (or sim.) in their name

A very quick search with the `LIKE` operator revealed four organizations that feature “Austria”, “austria” (just to check misprints), “Österreich” or “österreich” in their name, but are assigned to different countries:

```sql
select id, data->>'legalname' as legalname, data->'country'->>'code' as code, data->'country'->>'label' as label
from organizations o
where data->'country'->>'code' != 'AT' and
(data->>'legalname' like '%Austria%'
or data->>'legalname' like '%austria%'
or data->>'legalname' like '%Österreich%'
or data->>'legalname' like '%österreich%')
```

|id|legalname|code|label|
|--|---------|----|-----|
|`20&#124;pending_org_::74980f511f97e3d35c98385415227c01`|Österreichisches Archäologisches Institut Zweigstelle Athen|GR|Greece|
|`20&#124;openorgs____::05268c4fd826af1f9e98472b1f6a6797`|Institute e-Austria Timisoara|RO|Romania|
|`20&#124;openorgs____::202c63c9b124e2e68d9389ead6dfa39f`|Office of Science & Technology Austria|US|United States|
|`20&#124;pending_org_::5afce48c1140d6c4a2fdbf0bc312d029`|Austrian Cultural Forum|GB|United Kingdom|

Remarkably, these are **NOT** mistakes, because:
* Institute e-Austria Timisoara is actually Romanian. It has Austria in its name because the institute start-up was funded by BMWF and BMWA (see https://ieat.ro), and probably its main focus at first was on the relationships between Romania and Austria.
* The Ministry of Education has [two Offices of Science and Technology Austria](https://www.bmbwf.gv.at/en/Topics/Research/Research-international/International-research-collaboration/OSTA.html), one in China and one in the US. Therefore, the Office we find in the OpenAIRE data is the American one (https://www.ostaustria.org, as indicated in OpenAIRE; among its “alternativenames”, one can find also “OSTA Washington”).
* The same goes for the Austrian Cultural Forum in London, UK (https://www.acflondon.org)
* The last result is clearly a “Zweigstelle” of the ÖAI in Athens, Greece.

### Get all organizations with no country property, but "Austria" (or sim.) in their name

```sql
select id, data->>'legalname' as legalname from organizations o
where data->>'country' is null and
(data->>'legalname' like '%Austria%'
or data->>'legalname' like '%austria%'
or data->>'legalname' like '%Österreich%'
or data->>'legalname' like '%österreich%')
```

| Labels | Count |
|------------------------------------|---------------------------------------|
|%Austria%                           |64                                     |
|%austria% (just to check misprints) |0                                      |
|%Österreich%                        |56                                     |
|%österreich%                        |10                                     |
|Combined                            |126 (≠ sum of four numbers above: 130) |

Since the four numbers given above have as sum 130, there are some organizations where more than one of these filters apply – one of them being us:

|id                                  |legalname                              |
|------------------------------------|---------------------------------------|
|20&#124;pending_org_::7149152ae0552b68193b6673df03e7aa |Österreichische Computer Gesellschaft (OCG) - Austrian Computer Society - Österreichische Computer Gesellschaft (OCG) - Austrian Computer Society |
|20&#124;pending_org_::60c8c54fe22007374a83146dca448d2c |Austrian Institute for International Affairs - OIIP - Österreichisches Institut für Internationale Politik |
|20&#124;pending_org_::2fecc0aa1080bef76b7cd9c7f8304393 |Österreichische Akademie der Wissenschaften - Austrian Centre for Digital Humanities (ACDH) |
|20&#124;pending_org_::470b627d6f4b824914fd7f021f9fedd3 |Österreichische Akademie der Wissenschaften - ACE - Austrian Corpora and Editions |

### Find all organizations with country domain .at in their website URLs

```sql

```

### To do

- [ ] Check also all "Austrian" designations in `legalshortname` (results might be different)
- [ ] Another possibility would be to search for specific place names, or have a list of Austrian institutions

## Projects

### Relations

| domain | relation | range | status |
| ------ | -------- | ----- | ------ |
| Project | hasParticipant | Organization | exists |
|   | produces | Research product | exists |
|   | IsRelatedTo | Project |   |
|   |   | Community infrastructure |   |
|   |   | Datasource |   |
|   |   | Organization |   |
|   |   | Research product |   |
