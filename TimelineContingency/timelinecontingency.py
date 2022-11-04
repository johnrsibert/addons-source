print(' ')
print('---------------------------------------')
print('Hello world from timelinecontingency.py')

"""Reports/Text Reports/Family Sheet"""


#------------------------------------------------------------------------
#
# python modules
#
#------------------------------------------------------------------------
#from functools import partial
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
#from gramps.gen.const import GRAMPS_LOCALE as glocale
#_ = glocale.translation.gettext
#from gramps.gen.lib import EventRoleType, EventType, Person, PlaceType, Date
#from gramps.gen.utils.file import media_path_full
#from gramps.gen.utils.thumbnails import (get_thumbnail_path, SIZE_NORMAL,
#                                         SIZE_LARGE)
#from gramps.gen.plug.report import Report
#from gramps.gen.plug.report import utils
#from gramps.gen.plug.report import MenuReportOptions
#from gramps.gen.plug.report import stdoptions
#from gramps.gen.plug.menu import (NumberOption, ColorOption, BooleanOption,
#                                  EnumeratedListOption, PersonListOption,
#                                  SurnameColorOption)
#from gramps.gen.utils.db import get_birth_or_fallback, get_death_or_fallback
#from gramps.gen.proxy import CacheProxyDb
#from gramps.gen.errors import ReportError
#from gramps.gen.display.place import displayer as _pd

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


#------------------------------------------------------------------------
#
# TimelineContingencyReport -- created once the user presses 'OK'
#
#------------------------------------------------------------------------
class TimelineContingency(Report):
    """ TimelineContingency report """

    def __init__(self, database, options, user):
        """
        Initialize the report.

        @param database: the Gramps database instance
        @param options: instance of the Options class for this report
        @param user: a gramps.gen.user.User() instance
        """

        Report.__init__(self, database, options, user)

        menu = options.menu
        self.person_id    = menu.get_option_by_name('pid').get_value()
        self.recurse      = menu.get_option_by_name('recurse').get_value()
        self.callname     = menu.get_option_by_name('callname').get_value()
        self.placeholder  = menu.get_option_by_name('placeholder').get_value()
        self.incl_sources = menu.get_option_by_name('incl_sources').get_value()
        self.incl_notes   = menu.get_option_by_name('incl_notes').get_value()

    print('here')
