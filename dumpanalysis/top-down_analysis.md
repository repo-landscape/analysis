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

### Which organizations have property "country"?

```sql
select count(*) from organizations o where data->>'country' is null
```

Organizations with no `country` property: **76,946** (about **27%** of the total)

### Get all organizations with country AT

```sql
select id, data->'legalname' as name, data->'country' as country 
from organizations
where data->'country'->>'code' = 'AT'
or data->'country'->>'label' = 'Austria'
```

### Get all organizations with 

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

