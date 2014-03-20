import json
from main.util.db import openDb
import itertools
from main.util.odds_ratio import oddsRatioForEachTerm
from sklearn.feature_extraction.text import CountVectorizer

db = openDb("stuff/localconnect.json")

cur = db.cursor()
sql = """
SELECT Twitter_ScreenName, Description
FROM users_twitter
"""
cur.execute(sql)

userDescriptions = { }
for row in cur.fetchall():
    userDescriptions[row[0]] = row[1]

negativeUsernames = [ u'yobluemama2', u'emorenolampaya', u'sgivan', u'MyBioTechniques', u'AnantBhan', u'PLOSGenetics', u'MHTF', u'lymereporter', u'Affymetrix', u'pauldennyuk', u'SCPHRP', u'neuroconscience', u'sydnets', u'JuanCIvancevich', u'Keith_Laws', u'UCGHR', u'porousboundary', u'PLoSONE', u'gedankenstuecke', u'pathogenomenick', u'varcsvictoria', u'The_Episiarch', u'michaelscally', u'PLoSMedicine', u'rlanzara', u'hrana', u'Brainpowertips', u'coalescent', u'fungalgenomes', u'dylanlopich', u'Dr_Bik', u'wolfemi', u'duhokudai', u'PLOSONE', u'martinwhite33', u'HIV_Insight', u'rnomics', u'MiguelEscotet', u'Lectoraat_GGZ', u'razoralign', u'gawbul', u'jevives', u'Sequilabs', u'decostatw', u'ScienceEnabled', u'tcellbiology', u'JATetro', u'BioMickWatson', u'BernScience', u'SocLatAlergia', u'NatRevNeurol', u'aghoury79', u'TestCellBio', u'ferwen', u'eqpaho', u'info_TGHN', u'lymereporter1', u'RevistaFosil', u'aemonten', u'PhilippBayer', u'sclopit', u'AndyFarke', u'surt_lab', u'1hc0m', u'nceas', u'brembs', u'StemCellsPortal', u'gauravjain49', u'Mimbrerooo', u'PLoS', u'Aghoury_', u'ATP_CME', u'McDawg', u'TestAllPLoSRSS', u'lshlj', u'peterjgill', u'DrJCThrash', u'BoraZ', u'Genomengin', u'Prison_Health', u'GaBioscience', u'uranus_2', u'reiver', u'edyong209', u'jonmoulton', u'mattjhodgkinson', u'lizabio', u'dopaminergic13', u'SebValenz', u'scilahn', u'IndiGenome', u'JasmineGruiaGr', u'aswang', u'azizrk', u'Protohedgehog', u'n_j_davis', u'phylogenomics', u'selfishneuron', u'dfjpt', u'ISDS', u'wwcode', u'gilbertjacka', u'CambioLtd', u'jamoreno2010', u'MambaRave', u'PLoSNTDs', u'markomanka', u'yawjoshua', u'Why_We_Do_That', u'GeneTools', u'PLOSMedicine', u'm_m_campbell', u'psychoBOBlogy', u'wahyuwei', u'FUNDACIONLIBRA', u'SahaSurya', u'GSSHealth', u'symphonicworks', u'Quercus56', u'MarcelGutCo', u'SAGRudd', u'TLaskyPhD', u'neuroethology', u'boopsboops', u'Hlth_Literacy', u'mocost', u'nutrigenomics', u'GenomicsIo', u'fantomaster', u'HQP_tweets' ]
positiveUsernames = [ u'ialuddington', u'whatDNAtest', u'ProstateCell', u'TheMightyWord', u'Kenzibit', u'GholsonLyon', u'bookapharmacist', u'fmartin1954', u'PLOS', u'moorejh', u'VaillancourtLab', u'NatureRevMicro', u'Kieran_Neuro', u'alexbortvin', u'GaiaTek', u'PLOSCompBiol', u'julponchart', u'AreBrean', u'GeneQuan', u'medskep', u'TomHoltzPaleo', u'Energy_Science', u'mmi_updates', u'PLoSPathogens', u'micro_biome', u'renelaennec', u'WvSchaik', u'HartleyDM', u'kristall36', u'Ichnologist', u'TAGHIVscience', u'Olivier_LG', u'Incidence0', u'exerciseworks', u'nephondemand', u'JChrisPires', u'ken_coburn_md', u'drbachinsky', u'PLoSBiology', u'juanseapi', u'EpicentreBio', u'molecularist', u'GuiomeNicolas', u'Hortusrarus', u'Symbionticism', u'westr', u'Eric_O_Verger', u'TetZoo', u'TAWOP', u'DrLydiaND', u'balapagos', u'jocalynclark', u'BioCodersNet', u'genomigence', u'dylanbgeorge', u'arkhangellohim', u'LuisFernandoGm6', u'Uniparts', u'josebengoechea', u'dracecicastillo', u'AllArkansas', u'PUautomne', u'jjaimemiranda', u'dlizcano', u'WeigelWorld', u'SDHIresearch', u'maitegarolera', u'genetics_blog', u'promega', u'prerana123', u'synt_biology', u'FriEric', u'caseybergman', u'PLoSCompBiol', u'PLOSPathogens', u'MazyadAlfadhli', u'ClRoOdAl', u'QuestAnswers' ]

existingNegativeUsernames = filter(lambda usr: usr in userDescriptions, negativeUsernames)
existingPositiveUsernames = filter(lambda usr: usr in userDescriptions, positiveUsernames)

negativeDescriptions = filter(lambda desc: desc!=None, map(lambda usr: userDescriptions[usr], existingNegativeUsernames))
positiveDescriptions = filter(lambda desc: desc!=None, map(lambda usr: userDescriptions[usr], existingPositiveUsernames))


tokenizer = CountVectorizer().build_tokenizer()
wordCounts = { }
for desc in itertools.chain(positiveDescriptions, negativeDescriptions):
    tokens = tokenizer(desc)

    for token in tokens:
        wordCounts[token] = wordCounts.get(token, 0) + 1

frequentTokens = map(lambda kv: kv[0].lower(), filter(lambda kv: kv[1]>10, wordCounts.items()))

ors = oddsRatioForEachTerm(positiveDescriptions, negativeDescriptions)

print sorted(filter(lambda term: term[0].lower() in frequentTokens, ors), key=lambda x: x[1])