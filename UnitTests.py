import glob
import os

passedColor = '\033[32m'
boldPassedColor = '\033[1;32m'
failedColor = '\033[1;31m'
resetColor = '\033[0m'
warnColor = '\033[33m'
warnBoldColor = '\033[1;33m'
testNameColor = '\033[1;36m'

def printTestName(text):
    print testNameColor + text + resetColor

failCount = 0
warnCount = 0
#### Test Preprocessing. ####
import eHostess.NotePreprocessing.Preprocessor as preprocessor

printTestName("Testing Preprocesssor duplicate detection.")
dirList = ['./NotePreprocessing/testCorpus/*', './NotePreprocessing/testCorpus2/*']
duplicateProcessor = preprocessor.DuplicateProcessor(dirList)

duplicateProcessor.findDuplicates()
numSubsets = len(duplicateProcessor.subsetsToRemove)
numDuplicates = len(duplicateProcessor.exactDuplicatesToRemove)
numUnion = len(duplicateProcessor._getUnionOfDuplicatesAndSubsets())

if numSubsets == 3 and numDuplicates == 4 and numUnion == 6:
    print passedColor + "Passed\n" + resetColor
else:
    failCount += 1
    print failedColor + '*****************Test Failed***************************' + resetColor
# duplicateProcessor.reportDuplicates()


#### Test eHostInterface.KnowtatorReader.getOriginalFileLength() ####
from eHostess.eHostInterface.KnowtatorReader import getOriginalFileLength
failed = False
printTestName("Testing eHostInterface.KnowtatorReader.getOriginalFileLength()")

length = getOriginalFileLength('./UnitTestDependencies/eHostInterface/OriginalLengthandParseSingle/saved/2530.txt.knowtator.xml',
                               None)
if length != 8442:
    failed = True

length = getOriginalFileLength(
    './UnitTestDependencies/eHostInterface/OriginalLengthandParseSingle/saved/2530.txt.knowtator.xml',
    './UnitTestDependencies/eHostInterface/OriginalLengthandParseSingle/corpus')
if length != 8442:
    failed = True

if failed:
    failCount += 1
    print failedColor + '*****************Test Failed***************************' + resetColor
else:
    print passedColor + "Passed\n" + resetColor


#### Test eHostInterface.KnowtatorReader.parseSingleKnowtatorFile() ####
from eHostess.eHostInterface.KnowtatorReader import KnowtatorReader
failed = False
printTestName("Testing eHostInterface.KnowtatorReader.parseSingleKnowtatorFile()")

document = KnowtatorReader.parseSingleKnowtatorFile('./UnitTestDependencies/eHostInterface/OriginalLengthandParseSingle/saved/2530.txt.knowtator.xml')

if document.numberOfCharacters != 8442 \
    or len(document.annotations) != 1 \
    or document.annotations[0].attributes["present_or_absent"] != 'absent' \
    or document.documentName != '2530' \
    or document.annotations[0].annotationClass != 'doc_classification' \
    or document.annotations[0].annotationId != 'EHOST_Instance_438' \
    or document.annotations[0].annotator != 'Shane':
    failed = True

if failed:
    failCount += 1
    print failedColor + '*****************Test Failed***************************' + resetColor
else:
    print passedColor + "Passed\n" + resetColor


#### Test path cleaner, turns path strings into glob-able directory strings. ####
from eHostess.Utilities.utilities import cleanDirectoryList as cleaner

printTestName('Testing Utilities.cleanDirectoryList()')
dirs = ['/Some/path/to/stuff', '/Some/path/to/stuff/', '/Some/path/to/stuff/*']
cleanDirs = cleaner(dirs)
failed = False
for dirName in cleanDirs:
    if dirName != '/Some/path/to/stuff/*':
        print failedColor + '*****************Test Failed***************************' + resetColor
        failed = True
        failCount += 1
if not failed:
    print passedColor + "Passed\n" + resetColor

#### Test annotation overlap MentionLevelAnnotation.overlap() ####
printTestName('Testing MentionLevelAnnotation.overlap()')
failed = False
from Annotations.MentionLevelAnnotation import MentionLevelAnnotation

annotation1 = MentionLevelAnnotation("annotation 1 text", 0, 0, "annotator1", "annotator1 ID", {})
annotation2 = MentionLevelAnnotation("annotation 2 text", 10, 20, "annotator1", "annotator1 ID", {})

# case 1: same span
annotation1.start = 10
annotation1.end = 20
if MentionLevelAnnotation.overlap(annotation1, annotation2) != True:
    failed = True

# case 2:
annotation1.start = 10
annotation1.end = 15
if MentionLevelAnnotation.overlap(annotation1, annotation2) != True:
    failed = True

# case 3:
annotation1.start = 15
annotation1.end = 20
if MentionLevelAnnotation.overlap(annotation1, annotation2) != True:
    failed = True

# case 4:
annotation1.start = 0
annotation1.end = 5
if MentionLevelAnnotation.overlap(annotation1, annotation2) != False:
    failed = True

# case 5:
annotation1.start = 0
annotation1.end = 10
if MentionLevelAnnotation.overlap(annotation1, annotation2) != False:
    failed = True

# case 6:
annotation1.start = 0
annotation1.end = 15
if MentionLevelAnnotation.overlap(annotation1, annotation2) != True:
    failed = True

# case 7:
annotation1.start = 12
annotation1.end = 17
if MentionLevelAnnotation.overlap(annotation1, annotation2) != True:
    failed = True

# case 8:
annotation1.start = 15
annotation1.end = 25
if MentionLevelAnnotation.overlap(annotation1, annotation2) != True:
    failed = True

# case 9:
annotation1.start = 20
annotation1.end = 25
if MentionLevelAnnotation.overlap(annotation1, annotation2) != False:
    failed = True

# case 10:
annotation1.start = 25
annotation1.end = 30
if MentionLevelAnnotation.overlap(annotation1, annotation2) != False:
    failed = True

# case 11:
annotation1.start = 5
annotation1.end = 25
if MentionLevelAnnotation.overlap(annotation1, annotation2) != True:
    failed = True


if failed:
    failCount += 1
    print failedColor + '*****************Test Failed***************************' + resetColor
else:
    print passedColor + "Passed\n" + resetColor


#### Test PyConTextInterface.SentenceReconstructor ####
from PyConTextInterface.SentenceReconstructor import SentenceReconstructor as Reconstructor
from pyConTextNLP.helpers import sentenceSplitter as Splitter
printTestName('Testing PyConTextInterface.SentenceReconstructor.SentenceReconstructor()')

infile = open('./UnitTestDependencies/SentenceReconstructor/11.txt', 'r')
noteBody1 = infile.read()
infile.close()
infile = open('./UnitTestDependencies/SentenceReconstructor/12.txt', 'r')
noteBody2 = infile.read()
infile.close()

reconstructor = Reconstructor()

failed = False
for note in [noteBody1, noteBody2]:
    reconstructor.startNewNote(note)
    sentences = Splitter().splitSentences(note)
    reconstructedNote = ""
    for sentence in sentences:
        reconstructedNote += reconstructor.reconstructSentence(sentence)
    if reconstructedNote != note:
        failed = True
        break
if failed:
    failCount += 1
    print failedColor + '*****************Test Failed***************************' + resetColor
else:
    print passedColor + "Passed\n" + resetColor

#### Test PyConTextInterface.SentenceSplitters.PyConTextBuiltinSplitter ####
    printTestName('Testing PyConTextInterface.SentenceSplitters.PyConTextBuiltinSplitter')
    from eHostess.PyConTextInterface.SentenceSplitters.PyConTextBuiltinSplitter import splitSentencesSingleDocument
    from eHostess.PyConTextInterface.SentenceSplitters.PyConTextBuiltinSplitter import splitSentencesMultipleDocuments

    failed = False
    testDocPath = "./UnitTestDependencies/PyConText/SentenceSplitters/BuiltinSplitter/Docs/TestDocToSplit.txt"

    pyConTextInput = splitSentencesSingleDocument(testDocPath)
    if len(pyConTextInput.keys()) != 1:
        failed = True
    if pyConTextInput['TestDocToSplit'][0].text != 'Here is the first\nsentence.' or \
                    pyConTextInput['TestDocToSplit'][1].text != ' And, here\nis the second sentence.':
        print "Text was parsed incorrectly."
        failed = True
    if pyConTextInput['TestDocToSplit'][0].documentSpan != (0, 27) or pyConTextInput['TestDocToSplit'][1].documentSpan != (27, 61):
        print "Span parsed incorrectly."
        failed = True
    if pyConTextInput['TestDocToSplit'][0].documentName != 'TestDocToSplit' or pyConTextInput['TestDocToSplit'][1].documentName != 'TestDocToSplit':
        print "Document name parsed incorrectly."
        failed = True
    if pyConTextInput['TestDocToSplit'][0].documentLength != 61 or pyConTextInput['TestDocToSplit'][1].documentLength != 61:
        print "Document length parsed incorrectly."
        failed = True

    testDirPath = "./UnitTestDependencies/PyConText/SentenceSplitters/BuiltinSplitter/Docs"
    multiDocInput = splitSentencesMultipleDocuments(testDirPath)

    if multiDocInput['TestDocToSplit'][0].text != pyConTextInput['TestDocToSplit'][0].text or multiDocInput['TestDocToSplit'][0].documentSpan != pyConTextInput['TestDocToSplit'][0].documentSpan\
            or multiDocInput['TestDocToSplit'][0].documentName != pyConTextInput['TestDocToSplit'][0].documentName\
            or multiDocInput['TestDocToSplit'][0].documentLength != pyConTextInput['TestDocToSplit'][0].documentLength:
        failed = True

    if failed:
        failCount += 1
        print failedColor + '*****************Test Failed***************************' + resetColor
    else:
        print passedColor + "Passed\n" + resetColor

#### Test PyConTextInterface.SentenceSplitters.TargetSpanSplitter ####
    printTestName('Testing PyConTextInterface.SentenceSplitters.TargetSpanSplitter')
    from eHostess.PyConTextInterface.SentenceSplitters.TargetSpanSplitter import splitSentencesSingleDocument
    from eHostess.PyConTextInterface.SentenceSplitters.TargetSpanSplitter import splitSentencesMultipleDocuments
    import pyConTextNLP.itemData as itemData
    from eHostess.PyConTextInterface.SentenceSplitters.PyConTextInput import DocumentPlaceholder
    failed = False
    testDocPath = "./UnitTestDependencies/PyConText/SentenceSplitters/TargetSpanSplitter/Docs/TestDocToSplit.txt"
    testTargetsPath = os.path.join(os.getcwd(), "./UnitTestDependencies/PyConText/SentenceSplitters/TargetSpanSplitter/testTargets.tsv")
    targets = itemData.instantiateFromCSVtoitemData(testTargetsPath)
    pyConTextInput = splitSentencesSingleDocument(testDocPath, targets, 4, 4)

    if len(pyConTextInput.keys()) != 1 or len(pyConTextInput['TestDocToSplit']) != 3:
        failed = True
    if pyConTextInput['TestDocToSplit'][0].text != 'twelve thir^$#)(teen hemorrhage fourteen, brbpr [fifteen]' \
            or pyConTextInput['TestDocToSplit'][1].text != 'three, four% five s^$#)ix bleed seven, eight [nine]'\
            or pyConTextInput['TestDocToSplit'][2].text != 'ten,\neleven% twelve thir^$#)(teen hemorrhage fourteen, brbpr [fifteen]':
        print "Text was parsed incorrectly."
        failed = True
    if pyConTextInput['TestDocToSplit'][0].documentSpan != (74, 131) or pyConTextInput['TestDocToSplit'][1].documentSpan != (8, 59) \
            or pyConTextInput['TestDocToSplit'][2].documentSpan != (61, 131):
        print "Span parsed incorrectly."
        failed = True
    if pyConTextInput['TestDocToSplit'][0].documentName != 'TestDocToSplit' or pyConTextInput['TestDocToSplit'][1].documentName != 'TestDocToSplit'\
            or pyConTextInput['TestDocToSplit'][2].documentName != 'TestDocToSplit':
        print "Document name parsed incorrectly."
        failed = True
    if pyConTextInput['TestDocToSplit'][0].documentLength != 140 or pyConTextInput['TestDocToSplit'][1].documentLength != 140 \
            or pyConTextInput['TestDocToSplit'][2].documentLength != 140:
        print "Document length parsed incorrectly."
        failed = True

    testDirPath = "./UnitTestDependencies/PyConText/SentenceSplitters/TargetSpanSplitter/Docs"
    pyConTextInput = splitSentencesMultipleDocuments(testDirPath, targets, 4, 4)
    if len(pyConTextInput.keys()) != 3:
        failed = True
    if not isinstance(pyConTextInput['TestDocToSplit3'], DocumentPlaceholder):
        failed = True
    if not isinstance(pyConTextInput['TestDocToSplit'], list) or not isinstance(pyConTextInput['TestDocToSplit2'], list):
        failed = True

    if failed:
        failCount += 1
        print failedColor + '*****************Test Failed***************************' + resetColor
    else:
        print passedColor + "Passed\n" + resetColor

#### Test PyConTextInterface.PyConText.AnnotateSentences() ####
printTestName('Testing PyConTextInterface.PyConText.AnnotateSingleDocument()')
from eHostess.PyConTextInterface.PyConText import PyConTextInterface
from eHostess.PyConTextInterface.SentenceSplitters.PyConTextBuiltinSplitter import splitSentencesSingleDocument as splitBuiltin
from eHostess.PyConTextInterface.SentenceSplitters.PyConTextBuiltinSplitter import splitSentencesMultipleDocuments as splitBuiltinMultiple

failed = False

#Test with sentences from a single document, builtin splitter.
testDocPath = './UnitTestDependencies/PyConText/AnnotateSingleDocument/TestAffirmedAndNegatedInSameSentence.txt'
pyConTextInput = splitBuiltin(testDocPath)

#Contradictory Document, single annotation
contradictoryDoc = PyConTextInterface.PerformAnnotation(pyConTextInput)
if contradictoryDoc.documentName != 'TestAffirmedAndNegatedInSameSentence':
    failed = True
if len(contradictoryDoc.annotations) != 1:
    failed = True
contradictoryAnnotation = contradictoryDoc.annotations[0]
if contradictoryAnnotation.annotationClass != 'bleeding_absent':
    warnCount += 1
    print """********Warning: PyConText is annotating the sentence "%s" as %s. Please ensure that this is the desired
    outcome for a target that is modified by both NEGATED_EXISTENCE and AFFIRMED_EXISTANCE.""" % (contradictoryAnnotation.text, contradictoryAnnotation.annotationClass)

#Normal document, multiple annotations
pyConTextInput = splitBuiltin('./UnitTestDependencies/PyConText/AnnotateSingleDocument/testDoc.txt')
document = PyConTextInterface.PerformAnnotation(pyConTextInput)
spans = [(0, 75), (75, 157), (157, 248)]
# [(69, 74), (148, 153), (242, 247)]
classifications = ["bleeding_present", "bleeding_absent", "bleeding_present"]
for index, annotation in enumerate(document.annotations):
    if annotation.start != spans[index][0] or annotation.end != spans[index][1] \
            or classifications[index] != annotation.annotationClass:
        failed = True

#Test with sentences from multiple documents.

doc1spans = [(0, 75), (75, 157), (157, 248)]
doc1classifications = ["bleeding_present", "bleeding_absent", "bleeding_present"]

doc2spans = [(0, 81), (81, 172), (172, 248)]
doc2classifications = ["bleeding_absent", "bleeding_present", "bleeding_present"]

doc3spans = [(0, 90), (90, 166), (166, 248)]
doc3classifications = ["bleeding_present", "bleeding_present", "bleeding_absent"]

doc4spans = [(0, 75), (75, 166), (166, 248)]
doc4classifications = ["bleeding_present", "bleeding_present", "bleeding_absent"]

doc5spans = [(0, 81), (81, 157), (157, 248)]
doc5classifications = ["bleeding_absent", "bleeding_present", "bleeding_present"]

doc6spans = [(0, 90), (90, 172), (172, 248)]
doc6classifications = ["bleeding_present", "bleeding_absent", "bleeding_present"]

allSpans = [doc1spans, doc2spans, doc3spans, doc4spans, doc5spans, doc6spans]
allClassifications = [doc1classifications, doc2classifications, doc3classifications, doc4classifications,
                   doc5classifications, doc6classifications]

directories = glob.glob('./UnitTestDependencies/PyConText/AnnotateMultipleDocuments/*')
sentences = splitBuiltinMultiple(directories)
documents = PyConTextInterface.PerformAnnotation(sentences)
documents.sort(key=lambda x: x.documentName)
for docIndex, document in enumerate(documents):
    spans = allSpans[docIndex]
    classifications = allClassifications[docIndex]
    for index, annotation in enumerate(document.annotations):
        if annotation.start != spans[index][0] or annotation.end != spans[index][1] \
                or classifications[index] != annotation.annotationClass:
            failed = True

if failed:
    failCount += 1
    print failedColor + '*****************Test Failed***************************' + resetColor
else:
    print passedColor + "Passed\n" + resetColor

#### Test PyConTextInterface.PyConText.AnnotateSentences() ability to Remove Duplicate Annotations####
printTestName('Testing PyConTextInterface.PyConText.AnnotateSingleDocument() ability to Remove Duplicate Annotations.')
from eHostess.PyConTextInterface.SentenceSplitters.TargetSpanSplitter import splitSentencesSingleDocument as targetSpanSingleSplit
from eHostess.PyConTextInterface.SentenceSplitters.TargetSpanSplitter import splitSentencesMultipleDocuments as targetSpanSplitMultiple

failed = False

singleDocPath = "./UnitTestDependencies/PyConText/RemoveDuplicateAnnotations/Docs/Doc1.txt"
targets = itemData.instantiateFromCSVtoitemData(os.path.join(os.getcwd(), "./UnitTestDependencies/PyConText/RemoveDuplicateAnnotations/testTargets.tsv"))
sentences = targetSpanSingleSplit(singleDocPath, targets, 3, 3)

document = PyConTextInterface.PerformAnnotation(sentences)

if len(document.annotations) != 2:
    failed = True
if document.annotations[0].text != 'one two bleed four hemorrhage six'\
    or document.annotations[1].text != 'two bleed four hemorrhage six seven eight':
    failed = True

if failed:
    failCount += 1
    print failedColor + '*****************Test Failed***************************' + resetColor
else:
    print passedColor + "Passed\n" + resetColor

#### Test Analysis.Output.ConvertComparisonsToTSV() ####
printTestName('Testing Analysis.Output.ConvertComparisonsToTSV()')
# !!!!! This test doesn't really verify anything except that ConvertComparisonToTSV() doesn't raise any exceptions.
# To verify that the method is working correctly it is currently necessary to check the output file located at
# ./UnitTestDependencies/Output/ComparisonsToTSV/TestOutput/discrepancies.tsv
from eHostess.Analysis.Output import ConvertComparisonsToTSV
from eHostess.Analysis.DocumentComparison import Comparison

failed = False

doc1 = KnowtatorReader.parseSingleKnowtatorFile(
    './UnitTestDependencies/Output/ComparisonsToTSV/annotator2/saved/2530.txt.knowtator.xml')
doc2 = KnowtatorReader.parseSingleKnowtatorFile(
    './UnitTestDependencies/Output/ComparisonsToTSV/annotator1/saved/2530.txt.knowtator.xml')

discrepancies = Comparison.CompareAllAnnotations(doc1, doc2)
ConvertComparisonsToTSV(discrepancies, './UnitTestDependencies/Output/ComparisonsToTSV/TestOutput/discrepancies.tsv')

if failed:
    failCount += 1
    print failedColor + '*****************Test Failed***************************' + resetColor
else:
    print passedColor + "Passed\n" + resetColor

#### Test Analysis.Metrics.calculateRecallPrecisionFScoreAndSupport() ####
printTestName('Analysis.Metrics.calculateRecallPrecisionFScoreAndSupport()')
from eHostess.Analysis.Metrics import CalculateRecallPrecisionFScoreAndSupport
failed = False

recall, precision, fscore, support = CalculateRecallPrecisionFScoreAndSupport(discrepancies)

if recall != .25 or precision != .5:
    failed = True

if failed:
    failCount += 1
    print failedColor + '*****************Test Failed***************************' + resetColor
else:
    print passedColor + "Passed\n" + resetColor


#### Test PyConTextInterface.SentenceSplitters.PyConTextInput ####
printTestName('PyConTextInterface.SentenceSplitters.PyConTextInput')
from eHostess.PyConTextInterface.SentenceSplitters.PyConTextInput import PyConTextInput
failed = False

pyConTextInput = PyConTextInput()
pyConTextInput.addSentence("TestDoc1 1", (0, 0), "TestDoc1", 0)
pyConTextInput.addSentence("TestDoc1 2", (0, 0), "TestDoc1", 0)
pyConTextInput.addSentence("TestDoc2 1", (0, 0), "TestDoc2", 0)


if len(pyConTextInput.keys()) != 2:
    failed = True
if len(pyConTextInput["TestDoc1"]) != 2 or len(pyConTextInput["TestDoc2"]) != 1:
    failed = True

gotException = False
try:
    pyConTextInput.addDocumentPlaceholder("TestDoc1")
except RuntimeError as error:
    gotException = True
if not gotException:
    failed = True

gotException = False
pyConTextInput.addDocumentPlaceholder("TestDoc3")
try:
    pyConTextInput.addSentence("TestDoc3 1", (0, 0), "TestDoc3", 0)
except RuntimeError as error:
    gotException = True
if not gotException:
    failed = True



if failed:
    failCount += 1
    print failedColor + '*****************Test Failed***************************' + resetColor
else:
    print passedColor + "Passed\n" + resetColor

if failCount == 0:
    print boldPassedColor + "ALL TESTS PASSED" + resetColor
else:
    print failedColor + "%d TEST(S) FAILED" % failCount + resetColor
if warnCount != 0:
    print warnBoldColor + "%i Warning(s)" % warnCount + resetColor
