from enum import Enum


class Relation(Enum):
    SCHOOLING = dict(weight=3,
                     names=['ontology:academicAdvisor', 'ontology:choreographer', 'ontology:coach', 'property:disciple',
                            'ontology:doctoralAdvisor', 'ontology:doctoralStudent', 'ontology:formerChoreographer',
                            'ontology:formerCoach', 'property:mentor', 'ontology:notableStudent', 'ontology:trainer'])
    POLITICS = dict(weight=3,
                    names=['ontology:deputy', 'property:followedBy', 'ontology:governor',
                           'ontology:governorGeneral', 'ontology:nominee', 'ontology:opponent',
                           'ontology:runningMate',
                           ])
    COLLABORATION = dict(weight=3,
                         names=['property:alongside', 'ontology:appointer', 'ontology:associate',
                                'ontology:associatedAct',
                                'ontology:beatifiedBy', 'ontology:canonizedBy',
                                'property:commander',
                                'ontology:incumbent', 'ontology:lieutenant'])
    PERSONAL = dict(weight=3,
                    names=['ontology:currentPartner', 'property:father', 'ontology:formerPartner',
                           'property:mother', 'ontology:partner', 'ontology:relation',
                           'ontology:relative', 'property:sibling', 'ontology:spouse'])
    HERITAGE = dict(weight=3,
                    names=['property:heir', 'ontology:child', 'ontology:parent', 'ontology:successor',
                           'ontology:predecessor'])
    LEADERSHIP = dict(weight=3,
                      names=['ontology:primeMinister', 'ontology:vicePresident', 'ontology:vicePrimeMinister',
                             'property:chairman', 'property:leader', 'ontology:chancellor', 'ontology:monarch'])
    OTHER = dict(weight=3,
                 names=[])

    def get_relations_names(self):
        return self._value_['names']

    def get_weight(self):
        return self._value_['weight']
