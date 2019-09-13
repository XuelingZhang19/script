import sys
import commands
import os
import re

decodeFilePath = "/home/xueling/researchProjects/sourceDetection/decodeFile/"
methodPath = "/home/xueling/researchProjects/sourceDetection/methods/"
signaturePath = "/home/xueling/researchProjects/sourceDetection/sourceSignature/"



def convert(apk):
    print 'Converting methods into FLowDroid source signatures.................'
    files = commands.getoutput('ls ' + signaturePath).split('\n')
    if apk in files:
        print apk + 'exists!!'

    else:
        fw = open(signaturePath + apk, 'a')
        sigOrgPath = methodPath + apk
        # apk = log[:-4]
        print apk
        sigOrgs = open(sigOrgPath).readlines()

        for sig in sigOrgs:
            # print sig.strip()
            className = sig.strip().split('.')[-2]
            # print className
            methodName = sig.strip().split('.')[-1]
            # print methodName

            classPaths = sig.strip().split('.')[:-1]
            classPath = '.'.join(classPaths)
            filePath = '/'.join(classPaths)
            # print classPaths
            # print filePath


            cmd = 'grep --include ' + className + '.smali -F ' + '\'' + methodName + '(\' ' + decodeFilePath  +  apk +' -r '  + '| grep \'.method\' ' + '| grep \')Ljava/lang/String;\''
            # cmd = 'grep --include *.smali -F ' + '\'' + methodName + '(\' ' + decodeFilePath  + ' -r '  + '| grep \'.method\' '
            # print cmd
            outs = commands.getoutput(cmd).split('\n')                                # all mathes, one app could have multiple method using same name under different classes
            # print outs
            for out in outs:
                # print out
                flag = 0

                if filePath in out:                  # check the path
                    flag = 1
                    # print out
                    # print "in flag1"

                else:
                    # print "in flag0"
                    flag = 0
                    continue

                if flag == 1:
                    methodDeclar = out.split(':')[1]
                    # print methodDeclar
                    arguments = re.findall(r'\(.*\)', methodDeclar)[0]
                    # print "arguments: %s" %arguments

                    if arguments == '()':          # no argument
                        sigNew = '<' + classPath + ': ' + 'java.lang.String ' + methodName + '()' + '>' + ' -> _SOURCE_'
                        fw.write(sigNew + '\n')
                        # print out
                        print sigNew
                        continue

                    else:
                        # print "argument exists!"
                        newArgumentsList = []
                        arguments = arguments.lstrip('(')
                        arguments = arguments.rstrip(')')
                        # print arguments
                        argumentsList = arguments.split(';')     # multiple arguments

                        # if len(argumentsList) > 2:
                        #     print "multiple argument!!!!"


                        for argument in argumentsList:
                            # print argument
                            if argument == 'V':
                                argument = 'void'
                            elif argument == 'Z':
                                argument ='boolean'
                            elif argument == 'B':
                                argument = 'byte'
                            elif argument == 'I':
                                argument = 'int'
                            elif argument == 'C':
                                argument = 'char'
                            elif argument == 'S':
                                argument = 'short'
                            elif argument == 'J':
                                argument = 'long'
                            elif argument == 'D':
                                argument = 'double'
                            elif argument == 'F':
                                argument = 'float'
                            elif argument == 'IZ':
                                argument = 'int,boolean'

                            elif "[" in argument:
                                argument = argument.lstrip('[') + ("[]")


                            newArgument = argument.lstrip('L').replace("/", ".")
                            # print newArgument
                            newArgumentsList.append(newArgument)
                        newArguments = ','.join(newArgumentsList).rstrip(',')
                        sigNew = '<' + classPath + ': ' + 'java.lang.String ' + methodName + '(' + newArguments + ')' + '>' + ' -> _SOURCE_'
                        fw.write(sigNew + '\n')
                        print sigNew


                else:
                    continue






