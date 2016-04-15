from enum import Enum


class Relation(Enum):
    SCHOOLING = dict(weight=3,
                     names=['ontology:academicAdvisor', 'ontology:choreographer', 'ontology:coach', 'property:disciple',
                            'ontology:doctoralAdvisor', 'ontology:doctoralStudent', 'ontology:formerChoreographer',
                            'ontology:formerCoach', 'property:mentor', 'ontology:notableStudent', 'ontology:trainer'])
    POLITICS = dict(weight=3,
                    names=['ontology:chancellor', 'ontology:deputy', 'property:followedBy', 'ontology:governor',
                           'ontology:governorGeneral', 'ontology:monarch', 'ontology:nominee', 'ontology:opponent',
                           'ontology:predecessor', 'ontology:primeMinister', 'ontology:runningMate',
                           'ontology:successor',
                           'ontology:vicePresident', 'ontology:vicePrimeMinister'])
    COLLABORATION = dict(weight=3,
                         names=['property:alongside', 'ontology:appointer', 'ontology:associate',
                                'ontology:associatedAct',
                                'ontology:beatifiedBy', 'ontology:canonizedBy', 'property:chairman',
                                'property:commander',
                                'ontology:incumbent', 'property:leader', 'ontology:lieutenant'])
    PERSONAL = dict(weight=3,
                    names=['ontology:child', 'ontology:currentPartner', 'property:father', 'ontology:formerPartner',
                           'property:heir', 'property:mother', 'ontology:parent', 'ontology:partner',
                           'ontology:relation',
                           'ontology:relative', 'property:sibling', 'ontology:spouse'])
    OTHER = dict(weight=3,
                 names=[])

    def get_relations_names(self):
        return self._value_['names']

    def get_weight(self):
        return self._value_['weight']
