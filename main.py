# import sys
import Decode
import Instrument
import RebuildApk
import keyGeneration
import AsignKey
import GUITest
import IdentifySourceMethods
import ConvToSig
import TaintAnalysis
import Validation
import Uninstall
apk = 'com.foxsports.android'

# GUITest.install(apk, 'org')

# Uninstall.uninstall(apk)
# Decode.decode(apk)
# Instrument.insertLog(apk)
# RebuildApk.rebuild(apk)
# keyGeneration.generate(apk)
# AsignKey.assign(apk)
# GUITest.install(apk, 'new')
# #
IdentifySourceMethods.findMethod(apk)
ConvToSig.convert(apk)

TaintAnalysis.analyze(apk, 'default')
TaintAnalysis.analyze(apk, 'newSources')

Validation.validation(apk)



