from enum import Enum


class Relation(Enum):
    SCHOOLING = (3, ['ontology:academicAdvisor', 'ontology:choreographer', 'ontology:coach', 'property:disciple',
                     'ontology:doctoralAdvisor', 'ontology:doctoralStudent', 'ontology:formerChoreographer',
                     'ontology:formerCoach', 'property:mentor', 'ontology:notableStudent', 'ontology:trainer'])
    POLITICS = (3, ['ontology:chancellor', 'ontology:deputy', 'property:followedBy', 'ontology:governor',
                    'ontology:governorGeneral', 'ontology:monarch', 'ontology:nominee', 'ontology:opponent',
                    'ontology:predecessor', 'ontology:primeMinister', 'ontology:runningMate', 'ontology:successor',
                    'ontology:vicePresident', 'ontology:vicePrimeMinister'])
    COLLABORATION = (3, ['property:alongside', 'ontology:appointer', 'ontology:associate', 'ontology:associatedAct',
                         'ontology:beatifiedBy', 'ontology:canonizedBy', 'property:chairman', 'property:commander',
                         'ontology:incumbent', 'property:leader', 'ontology:lieutenant'])
    PERSONAL = (3, ['ontology:child', 'ontology:currentPartner', 'property:father', 'ontology:formerPartner',
                    'property:heir', 'property:mother', 'ontology:parent', 'ontology:partner', 'ontology:relation',
                    'ontology:relative', 'property:sibling', 'ontology:spouse'])
    OTHER = (1, [])

    def __init__(self, weight, relations):
        self.relations = relations
        self.weight = weight

    def get_relations(self):
        return self.relations

    def get_weight(self):
        return self.weight
