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
        MenuReportOptions.__init__(self, name, dbase)
        print('finished __init__')

#   def get_subject(self):
    #   self.__filter = FilterOption(_("People"), 0)
    #   self.__filter.set_help(
    #       _("Select people to use in the contingency report."))

        """ Return a string that describes the subject of the report. """
    #   gid = self.__pid.get_value()
    #   person = self.__db.get_person_from_gramps_id(gid)
    #   print('gid,person',gid,person)
    #   print('returning from get_subject')
    #   return displayer.display(person)

    def add_menu_options(self, menu):

        ##########################
        category_name = _("Report Options")
        ##########################

    #   print(self.__pid)
        self.__pid = PersonOption(_("People"))
        print(type(self.__pid))
        self.__pid.set_help(
            _("Select people to use in the contingency report."))
        menu.add_option(category_name, "pid", self.__pid)
        print(type(self.__pid))

    #   recurse = EnumeratedListOption(_("Print sheets for"), self.RECURSE_NONE)
    #   recurse.set_items([
    #       (self.RECURSE_NONE, _("Center person only")),
    #       (self.RECURSE_SIDE, _("Center person and descendants in side branches")),
    #       (self.RECURSE_ALL,  _("Center person and all descendants"))])
    #   recurse.set_help(_("Whether to include descendants, and which ones."))
    #   print('here 2')
    #   menu.add_option(category_name, "recurse", recurse)

        '''
        # --------------------------------
        add_option = partial(menu.add_option, _('People of Interest'))
        # --------------------------------

        person_list = PersonListOption(_('People of interest'))
        person_list.set_help(_('People of interest are used as a starting '
                               'point when determining "family lines".'))
        add_option('gidlist', person_list)

        '''
