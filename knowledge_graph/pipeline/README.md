# KG Pipeline

This is where we define the mapping between OpenMetadata assets and Neo4J.

## Teams

```cypher
CREATE (t:Team {name:'name', displayName:'displayName', description:'description', type:'type'})
CREATE (u:User {name:'name', displayName:'displayName', email:'email'})

CREATE (team)-[:CONTAINS]->(user)
CREATE (team)-[:HAS]->(subTeam)
```

## Governance

```cypher
CREATE (c:Classification {name:'name', displayName:'displayName', description:'description', mutuallyExclusive:'mutuallyExclusive'})
CREATE (t:Tag {name:'name', displayName:'displayName', description:'description'})
CREATE (g:Glossary {name:'name', displayName:'displayName', description:'description', mutuallyExclusive:'mutuallyExclusive', votes:'votes'})
CREATE (t:GlossaryTerm {name:'name', displayName:'displayName', description:'description', status:'status', mutuallyExclusive:'mutuallyExclusive', votes:'votes'})

CREATE (classification)-[:CONTAINS]->(tag) 
CREATE (glossary)-[:CONTAINS]->(glossaryTerm)
CREATE (glossaryTerm)-[:CONTAINS]->(glossaryTerm)
CREATE (glossaryTerm)-[:RELATED_TO]->(glossaryTerm)

CREATE (glossary)-[:HAS]->(tag)
CREATE (glossaryTerm)-[:HAS]->(tag)

CREATE (user)-[:OWNS]->(glossary)
CREATE (user)-[:OWNS]->(glossaryTerm)
CREATE (user)-[:REVIEWS]->(glossary)
CREATE (user)-[:REVIEWS]->(glossaryTerm)

CREATE (user)-[:VOTES]->(glossary)
CREATE (user)-[:VOTES]->(glossaryTerm)
```

## Domains

```cypher
CREATE (d:Domain {name:'name', displayName:'displayName', description:'description', type:'type'})
CREATE (p:DataProduct {name:'name', displayName:'displayName', description:'description'})
```


## Tables

```cyper
CREATE (s:DatabaseService {name:'name', displayName:'displayName', description:'description', type:'type'})
CREATE (d:Database {name:'name', displayName:'displayName', description:'description', votes:'votes'})
CREATE (s:DatabaseSchema {name:'name', displayName:'displayName', description:'description', votes:'votes'})
CREATE (t:Table {name:'name', displayName:'displayName', description:'description', ddl:'ddl', votes:'votes'})
CREATE (c:Column {name:'name', displayName:'displayName', description:'description', dataType:'dataType', constraint:'constraint'})

CREATE (databaseService)-[:CONTAINS]->(database)
CREATE (database)-[:CONTAINS]->(databaseSchema)
CREATE (databaseSchema)-[:CONTAINS]->(table)
CREATE (table)-[:CONTAINS]->(column)
CREATE (column)-[:CONTAINS]->(column)

CREATE (user)-[:VOTES]->(database)
CREATE (user)-[:VOTES]->(databaseSchema)
CREATE (user)-[:VOTES]->(table)

CREATE (user)-[:OWNS]->(databaseService)
CREATE (user)-[:OWNS]->(database)
CREATE (user)-[:OWNS]->(databaseSchema)
CREATE (user)-[:OWNS]->(table)
CREATE (team)-[:OWNS]->(databaseService)
CREATE (team)-[:OWNS]->(database)
CREATE (team)-[:OWNS]->(databaseSchema)
CREATE (team)-[:OWNS]->(table)

CREATE (databaseService)-[:HAS]->(tag)
CREATE (databaseService)-[:HAS]->(glossaryTerm)
CREATE (database)-[:HAS]->(tag)
CREATE (database)-[:HAS]->(glossaryTerm)
CREATE (databaseSchema)-[:HAS]->(tag)
CREATE (databaseSchema)-[:HAS]->(glossaryTerm)
CREATE (table)-[:HAS]->(tag)
CREATE (table)-[:HAS]->(glossaryTerm)
CREATE (column)-[:HAS]->(tag)
CREATE (column)-[:HAS]->(glossaryTerm)

CREATE (databaseService)-[:BELONGS_TO]->(domain)
CREATE (database)-[:BELONGS_TO]->(domain)
CREATE (databaseSchema)-[:BELONGS_TO]->(domain)
CREATE (table)-[:BELONGS_TO]->(domain)

CREATE (dataProduct)-[:CONTAINS]->(table)
```
