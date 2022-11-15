print(' ')
print('---------------------------------------')
print('Hello world from timelinecontingency.py')
'''
from inspect import currentframe, getframeinfo

def TRACE():
    frameinfo = getframeinfo(currentframe())
    print(frameinfo.filename, frameinfo.lineno)

TRACE()
'''

"""Reports/Text Reports/Family Sheet"""


#------------------------------------------------------------------------
#
# python modules
#
#------------------------------------------------------------------------
from functools import partial
#import html

import string
#------------------------------------------------------------------------
#
# Set up logging
#
#------------------------------------------------------------------------
#import logging
#LOG = logging.getLogger(".TimelineContingency")


#------------------------------------------------------------------------
#
# Gramps module
#
#------------------------------------------------------------------------
from gramps.gen.plug.docgen import (IndexMark, FontStyle, ParagraphStyle,
                                    TableStyle, TableCellStyle,
                                    FONT_SANS_SERIF, INDEX_TYPE_TOC,
                                    PARA_ALIGN_CENTER, PARA_ALIGN_RIGHT)

from gramps.gen.display.name import displayer
from gramps.gen.display.place import displayer as place_displayer
from gramps.gen.lib import Date, Event, EventType, FamilyRelType, Name
from gramps.gen.lib import StyledText, StyledTextTag, StyledTextTagType
from gramps.gen.plug import docgen
from gramps.gen.plug.menu import BooleanOption, EnumeratedListOption, PersonOption
from gramps.gen.plug.report import Report
from gramps.gen.plug.report import utils
from gramps.gen.plug.report import MenuReportOptions
import gramps.gen.datehandler
from gramps.gen.relationship import get_relationship_calculator
from gramps.gen.const import GRAMPS_LOCALE as glocale

try:
    _trans = glocale.get_addon_translator(__file__)
except ValueError:
    _trans = glocale.translation
_ = _trans.gettext

'''
   TimelineContingencyReport -- created once the user presses 'OK'
   The optionclass defined in the gpr file must inherit from MenuReportOptions.
'''
class TimelineContingency(MenuReportOptions):
    # TimelineContingency report

    RECURSE_NONE = 0
    RECURSE_SIDE = 1
    RECURSE_ALL = 2

 
    def __init__(self, name, dbase):
        self.__db = dbase
        self.__pid = None
        print('start MenuReportOptions.__init__(self, name, dbase)')
        MenuReportOptions.__init__(self, name, dbase)
        print('finish MenuReportOptions.__init__(self, name, dbase)')


    def add_menu_options(self, menu):
        print('start def add_menu_options(self, menu):')

        ##########################
        category_name = _("Report Options")
        add_option = partial(menu.add_option, category_name)
        ##########################

    #   print(self.__pid)
        self.__pid = PersonOption(_("People"))
        self.__pid.set_help(
            _("Select people to use in the contingency report."))
        menu.add_option(category_name, "pid", self.__pid)
        print(type(self.__pid))
        print(self.__pid)
        self.person_list = PersonOption(_("People"))
        menu.add_option(category_name, 'pid_list',self.person_list)
        print(type(self.person_list))
        print(self.person_list)

    #   person_list = PersonListOption(_('People of interest'))
    #   person_list.set_help(_('People of interest are used as a starting '
    #                          'point when determining "family lines".'))
        add_option('gidlist', self.person_list)

        print('finish def add_menu_options(self, menu):')

    def write_report(self):
        print('reached def write_report(self)')

        """ write the report """

        self.doc.start_paragraph("IDS-Normal")
        doc.write_text('writing text')
        doc.end_paragraph()
