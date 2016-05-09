class TypeHelper:
    TYPES = [
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

    @staticmethod
    def get_level(ptype):
        for index in range(len(TypeHelper.TYPES)):
            if ptype in TypeHelper.TYPES[index]:
                return index
        return 5
