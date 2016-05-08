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


class Type:
    def __init__(self):
        self.types = [
            ['Ambassador', 'Archeologist', 'Architect', 'Aristocrat', 'AdultActor', 'VoiceActor', 'Comedian',
             'ComicsCreator', 'Dancer', 'FashionDesigner', 'Humorist', 'BackScene', 'ClassicalMusicArtist', 'Guitarist',
             'MusicDirector', 'Singer', 'Painter', 'Photographer', 'Sculptor', 'Astronaut', 'ArcherPlayer',
             'AthleticsPlayer', 'AustralianRulesFootballPlayer', 'BadmintonPlayer', 'BaseballPlayer',
             'BasketballPlayer', 'Bodybuilder', 'AmateurBoxer', 'BullFighter', 'Canoeist', 'ChessPlayer', 'Cricketer',
             'Cyclist', 'DartsPlayer', 'Fencer', 'GaelicGamesPlayer', 'GolfPlayer', 'AmericanFootballPlayer',
             'CanadianFootballPlayer', 'Gymnast', 'HandballPlayer', 'HighDiver', 'HorseRider', 'Jockey',
             'LacrossePlayer', 'MartialArtist', 'MotocycleRacer', 'SpeedwayRider', 'DTMRacer', 'FormulaOneRacer',
             'NascarDriver', 'RallyDriver', 'NationalCollegiateAthleticAssociationAthlete', 'NetballPlayer',
             'PokerPlayer', 'Rower', 'RugbyPlayer', 'SnookerChamp', 'SoccerPlayer', 'SquashPlayer', 'Surfer', 'Swimmer',
             'TableTennisPlayer', 'TeamMember', 'TennisPlayer', 'BeachVolleyballPlayer', 'WaterPoloPlayer', 'Biathlete',
             'BobsleighAthlete', 'CrossCountrySkier', 'Curler', 'FigureSkater', 'IceHockeyPlayer', 'NordicCombined',
             'Skater', 'Ski_jumper', 'Skier', 'SpeedSkater', 'SumoWrestler', 'BeautyQueen', 'BusinessPerson',
             'Celebrity', 'Chef', 'Cardinal', 'ChristianBishop', 'ChristianPatriarch', 'Pope', 'Priest', 'Saint',
             'Vicar', 'AmericanFootballCoach', 'CollegeCoach', 'VolleyballCoach', 'SerialKiller', 'Economist',
             'Egyptologist', 'Engineer', 'Farmer', 'AnimangaCharacter', 'DisneyCharacter', 'MythologicalFigure',
             'NarutoCharacter', 'SoapCharacter', 'HorseTrainer', 'Journalist', 'Judge', 'Lawyer', 'Linguist',
             'MemberResistanceMovement', 'MilitaryPerson', 'Model', 'Monarch', 'MovieDirector', 'Noble', 'OfficeHolder',
             'SportsTeamMember', 'Orphan', 'Philosopher', 'PlayboyPlaymate', 'Chancellor', 'Congressman', 'Deputy',
             'Governor', 'Lieutenant', 'Mayor', 'MemberOfParliament', 'President', 'PrimeMinister', 'Senator',
             'VicePresident', 'VicePrimeMinister', 'PoliticianSpouse', 'RadioHost', 'TelevisionHost', 'Producer',
             'Psychologist', 'Referee', 'Religious', 'RomanEmperor', 'Baronet', 'Biologist', 'Entomologist', 'Medician',
             'Professor', 'SoccerManager', 'TelevisionDirector', 'Host', 'TheatreDirector', 'Historian',
             'MusicComposer', 'PlayWright', 'Poet', 'ScreenWriter', 'SongWriter'
             ],
            ['Actor', 'Instrumentalist', 'Boxer', 'GridironFootballPlayer', 'MotorcycleRider', 'RacingDriver',
             'SnookerPlayer', 'VolleyballPlayer', 'WinterSportPlayer', 'Wrestler', 'Cleric', 'Coach', 'Murderer',
             'ComicsCharacter', 'OrganisationMember', 'Politician', 'Presenter', 'BritishRoyalty', 'Scientist',
             'SportsManager', 'TelevisionPersonality', 'Writer'
             ],
            ['MusicalArtist', 'MotorsportRacer', 'Criminal', 'FictionalCharacter', 'Royalty'],
            ['Athlete', 'Artist']
        ]

    def get_types(self):
        return self.types
