from connection import RepositoryConnection
from SPARQLWrapper import SPARQLWrapper, JSON

rep = 'http://LAPTOP-FRRSP1GB:7200/repositories/Mineral'
endpoint = SPARQLWrapper(rep)


def execute_query_rel(sourse_query):
    endpoint.setQuery(sourse_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    rez = []
    for result in results['results']['bindings']:
        rez.append((result['sub']['value'] + ' ', result['pName']['value'] + ' ', result['obj']['value'] + ' '))
    return rez


def execute_query(sourse_query):
    endpoint.setQuery(sourse_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    rez = []
    for result in results['results']['bindings']:
        rez.append(result['pName']['value'])
    return rez


query = '''
SELECT DISTINCT (strafter(str(?class), \'#\') AS ?pName) WHERE {
  ?class a owl:Class .
  FILTER NOT EXISTS { ?class rdfs:subClassOf ?superclass }
}
'''

lst_classes = list(execute_query(query))
print(lst_classes)

min = 'Minerals'
query_minerals = """
    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
    SELECT (strafter(str(?p), \'#\') AS ?pName)
    WHERE {
        ?p a :%s.
    }
""" % min

lst_minerals = list(execute_query(query_minerals))
print(lst_minerals)

query_use = """
    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
    SELECT (strafter(str(?p), \'#\') AS ?pName)
    WHERE {
        ?p a :FieldOfUsage .
    }
"""

lst_use = list(execute_query(query_use))
print(lst_use)

query_classification = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
    SELECT (strafter(str(?p), \'#\') AS ?pName)
    WHERE {
        ?p rdfs:subClassOf :Classification .
        FILTER EXISTS { ?e rdfs:subClassOf ?p }
    }
"""

lst_class = list(execute_query(query_classification))
print(lst_class)

query_chem = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
    SELECT (strafter(str(?p), \'#\') AS ?pName)
    WHERE {
        ?p rdfs:subClassOf :ByChemicalComposition .
    }
"""

lst_chem = list(execute_query(query_chem))
print(lst_chem)

mins = []
for i in lst_chem:
    query_mins = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
        SELECT (strafter(str(?p), \'#\') AS ?pName)
        WHERE {
            ?p a :%s .
        }
    """ % i
    ls = list(execute_query(query_mins))
    mins.append(ls)

print(mins)

query_orig = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
    SELECT (strafter(str(?p), \'#\') AS ?pName)
    WHERE {
        ?p rdfs:subClassOf :ByFormOfOrigin .
    }
"""

lst_orig = list(execute_query(query_orig))
print(lst_orig)

query_art = """
    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
    SELECT (strafter(str(?p), \'#\') AS ?pName)
    WHERE {
        ?p a :Artificial.
    }
"""

lst_art = list(execute_query(query_art))
print(lst_art)

query_org = """
    PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
    SELECT (strafter(str(?p), \'#\') AS ?pName)
    WHERE {
        ?p a :Organic.
    }
"""

lst_org = list(execute_query(query_org))
print(lst_org)

t = 'Topaz'

rels = """
      PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
      PREFIX owl: <http://www.w3.org/2002/07/owl#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
      SELECT DISTINCT (strafter(str(?p), \'#\') AS ?pName) (strafter(str(?subject), \'#\') AS ?sub) (strafter(str(?object), \'#\') AS ?obj)
      WHERE { 
      ?subject ?p ?object .
      ?p rdf:type owl:ObjectProperty.
      FILTER(contains(lcase(str(?subject)), lcase(STR("%s")))).
      } 
""" % t

lst_rels = list(execute_query_rel(rels))
print(lst_rels)


rel = """
      PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
      PREFIX owl: <http://www.w3.org/2002/07/owl#>
      SELECT DISTINCT (strafter(str(?p), \'#\') AS ?pName) 
      WHERE { 
      ?p rdf:type owl:ObjectProperty.
      } 
"""

lst_rel = list(execute_query(rel))
print(lst_rel)

ent = '''
 PREFIX : <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
      PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT (strafter(str(?p), \'#\') AS ?pName) 
WHERE {
 ?p a owl:NamedIndividual .
}
'''

lst_ent = list(execute_query(ent))
print(lst_ent)

# g = Graph()
# g.parse("http://localhost:8890/DAV/temp/min.owl")
# # n = Namespace('http://localhost:8890/DAV/temp/min.owl')
# # nm = g.namespace_manager
# # nm.bind(prefix, n)
#
# for subj, pred, obj in g:
#     if (subj, pred, obj) not in g:
#         raise Exception("It better be!")

# minerals_address = [i for i in g.query(query_minerals)]
# minerals = [str(str(i).split('#')[1]).split("'")[0] for i in minerals_address]
#
# use_address = [i for i in g.query(query_use)]
# usage = [str(str(i).split('#')[1]).split("'")[0] for i in use_address]
#
# classification_address = [i for i in g.query(query_classification)]
# classification = [str(str(i).split('#')[1]).split("'")[0] for i in classification_address]
#
# chem_address = [i for i in g.query(query_chem)]
# chem = [str(str(i).split('#')[1]).split("'")[0] for i in chem_address]
#
# orig_address = [i for i in g.query(query_orig)]
# orig = [str(str(i).split('#')[1]).split("'")[0] for i in orig_address]
#
# # for i in minerals_address:
# #     print(i)
# # for i in orig:
# #     print(i)
# # for i in usage:
# #     print(i)
# insert_min = '''
# INSERT DATA {
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     PREFIX my: <http://localhost:8890/DAV/temp/min.owl#>
#         "Talcum" a my:Minerals.
#         }
# '''
#
# onto = get_ontology("http://localhost:8890/DAV/temp/min.owl")
# #onto_path.append("http://localhost:8890/DAV/temp/#")
# onto.load()
# talcum = onto.Minerals("Talcum")
# # print(talcum.name)
# # print(talcum.iri)
# # for i in onto.individuals():
# #     print(i)
#
# l = list(default_world.sparql("""
#            SELECT (COUNT(?x) AS ?nb)
#            { ?x a owl:Class . }
#     """))
#
# minerals = [str(i[0]).split('.')[1] for i in list(default_world.sparql("""
#     PREFIX my: <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
#     SELECT ?p
#     WHERE {
#         ?p a my:Minerals .
#     }
# """))]
#
# use = [str(i[0]).split('.')[1] for i in list(default_world.sparql("""
#     PREFIX my: <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
#     SELECT ?p
#     WHERE {
#         ?p a my:FieldOfUsage .
#     }
# """))]
#
# classification = [str(i[0]).split('.')[1] for i in list(default_world.sparql( """
#     PREFIX my: <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT ?p
#     WHERE {
#         ?p rdfs:subClassOf my:Classification .
#     }
# """))]
#
# chem = [str(i[0]).split('.')[1] for i in list(default_world.sparql( """
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     PREFIX my: <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
#     SELECT ?p
#     WHERE {
#         ?p rdfs:subClassOf my:ByChemicalComposition .
#     }
# """))]
#
# origin = [str(i[0]).split('.')[1] for i in list(default_world.sparql( """
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     PREFIX my: <http://www.semanticweb.org/maria/ontologies/2023/2/Mineral#>
#     SELECT ?p
#     WHERE {
#         ?p rdfs:subClassOf my:ByFormOfOrigin .
#     }
# """))]
#
# print(minerals)
