from inspect import currentframe, getframeinfo
def HERE(frameinfo):
#   frameinfo = getframeinfo(currentframe())
#   print(frameinfo.filename, frameinfo.lineno)
    print('REACHED LINE', frameinfo.lineno)

def TRACE(frameinfo,value):
    print('value =',value,' at', frameinfo.lineno)

#
# Gramps - a GTK+/GNOME based genealogy program - Family Sheet plugin
#
# Copyright (C) 2008,2009,2010 Reinhard Mueller
# Copyright (C) 2010 Jakim Friant
# Copyright (C) 2016 Serge Noiraud
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# $Id$

"""Reports/Text Reports/Family Sheet"""

#------------------------------------------------------------------------
#
# Standard Python modules
#
#------------------------------------------------------------------------
import string

#------------------------------------------------------------------------
#
# Gramps modules
#
#------------------------------------------------------------------------
from gramps.gen.display.name import displayer
from gramps.gen.display.place import displayer as place_displayer
from gramps.gen.lib import Date, Event, EventType, FamilyRelType, Name
from gramps.gen.lib import StyledText, StyledTextTag, StyledTextTagType
from gramps.gen.plug import docgen
from gramps.gen.plug.menu import BooleanOption, EnumeratedListOption, PersonListOption
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
from gramps.gen.simple._simpleaccess import SimpleAccess

#------------------------------------------------------------------------
#
# Constants
#
#------------------------------------------------------------------------
#empty_birth = Event()
#empty_birth.set_type(EventType.BIRTH)
#
#empty_marriage = Event()
#empty_marriage.set_type(EventType.MARRIAGE)


#------------------------------------------------------------------------
#
# TimelineContingency report
#
#------------------------------------------------------------------------
class TimelineContingencyReport(Report):
    """
    A Family Sheet is a page which contains all available info about a specific
    person, the families this person is a father or mother in, and the children
    of these families.

    The intended use for this report is to get a full dump of the database in
    nice paper form in a way suitable to file it in a folder.

    Each Family Sheet contains a key at the top right which is derived from the
    relationship from the central person in the database and the person for
    which the sheet is printed. For direct ascendants, the Family Sheet key is
    the "Ahnentafel" number (also known as Eytzinger, Sosa, Sosa-Stradonitz, or
    Kekule number). Each child is assigned a letter starting from "a", and the
    Family Sheet key of the child is the Family Sheet key of the parent with
    the child's letter appended.

    The report contains full information (including all events, attributes,
    source references, and notes) for the key person and all its spouses.
    For children that had spouses, only a short section (including only name
    and birth event info) is printed along with a reference to the Family Sheet
    page on which this child would be the key person, while for children that
    had no spouses, full info is printed.

    If recursive printing is selected, each Family Sheet is followed by the
    Family Sheets of the children that had spouses.
    """

    def __init__(self, database, options, user):
        """
        Initialize the report.

        @param database: the Gramps database instance
        @param options: instance of the Options class for this report
        @param user: a gramps.gen.user.User() instance
        """

        Report.__init__(self, database, options, user)
   #    TRACE(getframeinfo(currentframe()),options.get_options())

        menu = options.menu
        self.person_id    = menu.get_option_by_name('pid').get_value()
        TRACE(getframeinfo(currentframe()),type(self.person_id)) # I0166 (gid)
        TRACE(getframeinfo(currentframe()),self.person_id) # I0166 (gid)
        self.gid_list = self.person_id.split()
        TRACE(getframeinfo(currentframe()),self.gid_list) # I0166 (gid)

        self.recurse      = False #menu.get_option_by_name('recurse').get_value()
        self.callname     = False #menu.get_option_by_name('callname').get_value()
        self.placeholder  = False #menu.get_option_by_name('placeholder').get_value()
        self.incl_sources = False #menu.get_option_by_name('incl_sources').get_value()
        self.incl_notes   = False #menu.get_option_by_name('incl_notes').get_value()
    '''
    def start_table(self):
        ncol = len(self.gid_list)+1
        TRACE(getframeinfo(currentframe()),ncol)
        table = docgen.TableStyle(ncol)
        table.set_width(100)
        table.set_columns(ncol)
        w0 = 8
        table.set_column_width(0, w0)
        w = (100-w0)/(ncol-1)
        for c in range(1,ncol):
            print('column',c)
            table.set_column_width(c, w)

        default_style.add_table_style('FSR-Table', table)
    '''

    def write_report(self):

    #   TRACE(getframeinfo(currentframe()),default_style)
        sa = SimpleAccess(self.database)

        print(len(self.gid_list),'names:',self.gid_list)
        for count, gid in enumerate(self.gid_list):
            print()
            person = self.database.get_person_from_gramps_id(gid)
            print(count,gid,person)

            print("Person        : ", sa.name(person))
            print("Gender        : ", sa.gender(person))
            print("Birth date    : ", sa.birth_date(person))
            print("Birth place   : ", sa.birth_place(person))
            print("Death date    : ", sa.death_date(person))
        #   print("Death place   : ", sa.death_place(person))
        #   print("Father        : ", sa.name(sa.father(person)))
        #   print("Mother        : ", sa.name(sa.mother(person)))
        #   print("Spouse        : ", sa.name(sa.spouse(person)))
        #   print("Marriage Type : ", sa.marriage_type(person))
        #   print("Marriage Date : ", sa.marriage_date(person))
        #   print("Marriage Place: ", sa.marriage_place(person))
           
        #   for child in sa.children(person):
        #       print("Child         : ", sa.name(child))

            # Print out burial and baptism events
            for event in sa.events( person):# , [ "Burial", "Death", "Residence", "Marriage" ]):
               print("Event         : ", sa.event_type(event), sa.event_date(event), 
                      sa.event_place(event))

        #   if (1): return


#       self.start_table()

       

        self.doc.start_paragraph('TCR-Title')
        self.doc.write_text('Timeline Contingeny Table')
        self.doc.end_paragraph()

        pperson = str(_Name_get_styled(person.get_primary_name()))
                                      #  _Name_CALLNAME_DONTUSE))

        TRACE(getframeinfo(currentframe()),pperson)


#       self.__process_person(person, rank, ahnentafel, person_key)

       # --- Now let the party begin! ---


        self.doc.start_table(None, 'TCR-Table')
        table = docgen.TableStyle()
        TRACE(getframeinfo(currentframe()),type(table))
        ncol = len(self.gid_list)+1
        TRACE(getframeinfo(currentframe()),ncol)
        TRACE(getframeinfo(currentframe()),type(ncol))
        table.set_width(100)
        table.set_columns(ncol)
        w0 = 8
        table.set_column_width(0, w0)
        w = (100-w0)/(ncol-1)
        for c in range(1,ncol):
            print('column',c)
            table.set_column_width(c, w)


        self.doc.start_row()

        self.doc.start_cell('TCR-HeadCell', 1)
        self.doc.start_paragraph('TCR-Name')
        self.doc.write_text("Year")#, mark)
        self.doc.end_paragraph()
        self.doc.end_cell()

        for c, gid in enumerate(self.gid_list):
            self.doc.start_cell('TCR-HeadCell', 1)
            self.doc.start_paragraph('TCR-Name')
#  note = '{0} Largest Counties; {1:,} Cases; {2:,} Deaths'.format(nG,tcases,tdeaths)
            person = self.database.get_person_from_gramps_id(gid)
            pperson = str(_Name_get_styled(person.get_primary_name()))
                                       # _Name_CALLNAME_DONTUSE))

            
        #   print(c,type(gid),gid,pperson)
        #   if c == 2:
        #       print('----',c,type(gid),gid,pperson)
        #       print('    ',person.get_primary_event_ref_list())

        #   self.doc.write_text(gid)
            self.doc.write_text('{0}\n({1})'.format(pperson,gid))
            self.doc.end_paragraph()
            self.doc.end_cell()

        self.doc.end_row()

        self.doc.end_table()


_Name_CALLNAME_DONTUSE = 0
_Name_CALLNAME_REPLACE = 1
_Name_CALLNAME_UNDERLINE_ADD = 2


def _Name_get_styled(name):#, callname, placeholder=False):
    return StyledText(displayer.display_name(Name(source=name)))


  


#------------------------------------------------------------------------
#
# MenuReportOptions
#
#------------------------------------------------------------------------
class TimelineContingencyOptions(MenuReportOptions):
    """
    Defines options and provides handling interface.
    """

    RECURSE_NONE = 0
    RECURSE_SIDE = 1
    RECURSE_ALL = 2

    def __init__(self, name, dbase):
        self.__db = dbase
        self.__pid = None
        MenuReportOptions.__init__(self, name, dbase)
        HERE(getframeinfo(currentframe()))

    def get_subject(self):
        HERE(getframeinfo(currentframe()))
        """ Return a string that describes the subject of the report. """
        gid = self.__pid.get_value()
        TRACE(getframeinfo(currentframe()),gid) # I0166 (gid)
        person = self.__db.get_person_from_gramps_id(gid)
        TRACE(getframeinfo(currentframe()),person) 
        names = person.get_alternate_names()
        TRACE(getframeinfo(currentframe()),names) 


    def add_menu_options(self, menu):

        ##########################
        category_name = _("Report Options")
        ##########################

        self.__pid = PersonListOption(_("People of Interest"))
        self.__pid.set_help(
            _("Names of people comprising columns of table."))
        menu.add_option(category_name, "pid", self.__pid)


    def make_default_style(self, default_style):
        """Make default output style for the Family Sheet Report."""
        TRACE(getframeinfo(currentframe()),default_style)
        HERE(getframeinfo(currentframe()))
        pnames = default_style.get_paragraph_style_names()
        TRACE(getframeinfo(currentframe()),pnames)
        #Paragraph Styles
        table = docgen.TableStyle()
        table.set_width(100)
   #    table.set_columns(4)
        w0 = 8
        table.set_column_width(0, w0)
   #    w = (100-w0)/3
   #    for c in range(1,4):
   #        print('column',c)
   #        table.set_column_width(c, w)

        default_style.add_table_style('TCR-Table', table)

        TRACE(getframeinfo(currentframe()),default_style)
        pnames = default_style.get_paragraph_style_names()
        TRACE(getframeinfo(currentframe()),pnames)

        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(14)
        font.set_bold(1)
        para = docgen.ParagraphStyle()
        para.set_alignment(docgen.PARA_ALIGN_CENTER)
        para.set_font(font)
        para.set_description(_("The style used for table title"))
        default_style.add_paragraph_style('TCR-Title', para) 

        TRACE(getframeinfo(currentframe()),default_style)
        pnames = default_style.get_paragraph_style_names()
        TRACE(getframeinfo(currentframe()),pnames)

        #Table Styles
        cell = docgen.TableCellStyle()
        cell.set_padding(0.1)
        cell.set_top_border(1)
        cell.set_left_border(1)
        cell.set_right_border(1)
        default_style.add_cell_style('TCR-HeadCell', cell)

        TRACE(getframeinfo(currentframe()),default_style)
        pnames = default_style.get_paragraph_style_names()
        TRACE(getframeinfo(currentframe()),pnames)

        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(12)
        font.set_bold(1)
        para = docgen.ParagraphStyle()
        para.set_alignment(docgen.PARA_ALIGN_CENTER)
        para.set_font(font)
        para.set_description(_("The style used for names"))
        default_style.add_paragraph_style('TCR-Name', para) # *

        TRACE(getframeinfo(currentframe()),default_style)
        pnames = default_style.get_paragraph_style_names()
        TRACE(getframeinfo(currentframe()),pnames)




