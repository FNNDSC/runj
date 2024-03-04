#!/usr/bin/env python3
#
# (c) 2024 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import  sys, os


from    runj.__init__       import __pkg, __version__

from    argparse            import RawTextHelpFormatter
from    argparse            import ArgumentParser
import  pudb

from    pfmisc._colors      import Colors
from    pfmisc              import other

from    runj.runj           import RunJ, json_respresentation, parser_setup, parser_interpret

CY      = Colors.CYAN
YL      = Colors.YELLOW
NC      = Colors.NO_COLOUR
GR      = Colors.GREEN

str_desc = Colors.CYAN + f"""{CY}
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░       ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░
{NC}
                        run CLI "jobs" from python

                             -- version {YL}{__version__}{NC} --

    {CY}runj{NC} is python module and script for executing arbitrary CLI strings on
    the underlying system. In script mode its utility is somewhat limited (since
    running a script from the CLI to run a CLI string seems rather contorted);
    however from within python it allows for an easy mechanism to run CLI apps
    and capture output.


""" + Colors.NO_COLOUR

package_CLIself = '''
        --exec <CLIcmdToExec>                                                   \\
       [--spawnScript]                                                          \\
       [--log <logDir>]                                                         \\
       [--logPrefix <prefix>]                                                   \\
       [--version]
'''

package_argSynopsisSelf = '''
        --exec <CLIcmdToExec>
        The command line expression to exeute.

        [--spawnScript]
        If specified, create a script around the <CLIcmdToExec> and execute
        the script. This is particularly useful for jobs that need to be run
        in the background.

        [--scriptDir <dir>]
        If specified, write any spawnedScripts to <dir>. If not specified, will
        autogenerate the <dir> given current date, typically in
        `/tmp/runj-history`

        [--background]
        If specified, and in conjunction with --spawnScript, will open the
        subprocess and not wait/block on stdout/stderr.

        IMPORTANT: Even if the <CLIcmdToExec> ends with a "background" '&'
        character, this script will still block until the child has completed.
        To detach and not wait, for the child, you MUST specify this flag.

        In fact, the "&" is not needed in the <CLIcmdToExec>.

        [--log <dir>]
        If specified, create in <dir> a log snapshot of various env/exec
        values (uid, pid, etc).

        [--logPrefix <prefix>]
        If specified, prepend log snapshots with <prefix>.

        [--version]
        If specified, print the version and exit.

        [--man]
        If specified, print a detail man page and exit.

        [--synopsis]
        If specified, print only an overview synposis and exit.

'''

package_CLItagHelp          = """
"""

package_CLIfull             = package_CLIself
package_CLIDS               = package_CLIself
package_argsSynopsisFull    = package_argSynopsisSelf
package_argsSynopsisDS      = package_argSynopsisSelf

def synopsis(ab_shortOnly = False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis =  """
    NAME

        runj

    SYNOPSIS

        runj """ + package_CLIfull + """

    BRIEF EXAMPLE

        runj --exec "ls /"

    """

    description =  '''
    DESCRIPTION

        ``runj`` runs some user specified CLI either "directly"
        or from a created script.


    ARGS ''' +  package_argsSynopsisFull     +\
                package_CLItagHelp + '''

    EXAMPLES

    Perform  `ls -1 /tmp | wc -l`

        runj --exec 'ls -1 /tmp | wc -l'

    '''

    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description


def earlyExit_check(args) -> int:
    """Perform some preliminary checks
    """
    if args.man or args.synopsis:
        print(str_desc)
        if args.man:
            str_help     = synopsis(False)
        else:
            str_help     = synopsis(True)
        print(str_help)
        return 1
    if args.version:
        print("Name:    %s\nVersion: %s" % (__pkg.name, __version__))
        return 2
    return 0

def main(argv:list[str]=[]) -> int:
    add_help:bool           = False
    parserSA:ArgumentParser = parser_setup(
                                    'A command line python helper',
                                    add_help
                                )
    args, extra              = parser_interpret(parserSA, argv)

    if (exit:=earlyExit_check(args)): return exit

    args.version            = __version__
    args.desc               = synopsis(True)

    shell                   = RunJ(args)()
    print(json_respresentation(shell))
    return shell.returncode

if __name__ == "__main__":
    sys.exit(main())
