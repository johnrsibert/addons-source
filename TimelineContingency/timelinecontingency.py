from inspect import currentframe, getframeinfo
def HERE(frameinfo):
#   HERE(getframeinfo(currentframe()))
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

#import pandas as pd
#import numpy as np

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

        self.__options = options
        print('options:')
        TRACE(getframeinfo(currentframe()),vars(options))

   #    self.__pid_LIST = options.__pid_list

        menu = options.menu
        self.__menu = menu
        print()
        print('menu:')
        TRACE(getframeinfo(currentframe()),vars(menu))
    #   print()
    #   self.__pid_list = menu.get_option_by_name('pid_list')
    #   TRACE(getframeinfo(currentframe()),self.__pid_list)

        self.person_id = menu.get_option_by_name('pid').get_value()
    #   TRACE(getframeinfo(currentframe()),type(self.person_id)) # I0166 (gid)
    #   TRACE(getframeinfo(currentframe()),self.person_id) # I0166 (gid)

        self.__gid_list = self.person_id.split()
    #   TRACE(getframeinfo(currentframe()),self.__gid_list) # I0166 (gid)

    #   self.placeholder  = False #menu.get_option_by_name('placeholder').get_value()
    #   self.incl_sources = False #menu.get_option_by_name('incl_sources').get_value()
    #   self.incl_notes   = False #menu.get_option_by_name('incl_notes').get_value()
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
    
    def get_year(self,event):
        date = event.get_date_object()
        return(int(date.get_year()))

    def get_place(self,event):
        place_handle = event.get_place_handle()
    #   TRACE(getframeinfo(currentframe()),place_handle)
        '''
        if place_handle != '': #is not None:
            place = self.database.get_place_from_handle(place_handle)
            place_title = place_displayer.display(self.database, place)
        else:
            place_title = None
        '''
        try:
            place = self.database.get_place_from_handle(place_handle)
            place_title = place_displayer.display(self.database, place)
        except Exception as ex:
        #   print(ex)
        #   print(repr(ex))
        #   print(ex.args)
            place_title = 'Unspecified location.'

        '''
        except Exception as e: # (as opposed to except Exception, e:)
                           # ^ that will just look for two classes, Exception and e
        # for the repr
        print(repr(e))
        # for just the message, or str(e), since print calls str under the hood
        print(e)
        # the arguments that the exception has been called with. 
        # the first one is usually the message. (OSError is different, though)
        print(e.args)
        '''

        return(place_title)


    def write_report(self):
    #   sa = SimpleAccess(self.database)
        HERE(getframeinfo(currentframe()))
    
        year_list = []

    #   loop through persons of interest 
    #   print(len(self.gid_list),'gids:',self.menu)
    #   self.__options.set_table_columns(len(self.gid_list))
    
        for gcount, gid in enumerate(self.__gid_list):
            print()
            person = self.database.get_person_from_gramps_id(gid)
            pperson = str(_Name_get_styled(person.get_primary_name()))
            print(gcount,gid,pperson)

            # loop through events associated with person of interest
            for endx, erefl in enumerate(person.event_ref_list):
                event = self.database.get_event_from_handle(erefl.get_reference_handle())
                eid = event.get_gramps_id()
                date = event.get_date_object()
                year = date.get_year()
            #   place_handle = event.get_place_handle()
            #   place = self.database.get_place_from_handle(place_handle)
            #   place_title = place_displayer.display(self.database, place)
                place_title = self.get_place(event)
                year_list.append(int(year))

                print('endx:',endx,type(erefl),erefl.ref)
                print(' len:',type(person.event_ref_list),len(person.event_ref_list))
                print('    :',person.event_ref_list[endx])
                print('  ID:',eid)
                print('year:',year)
                print('plac:',place_title)
                print('')


        #   print(year_list)
        place = None

   
        print()
    #   print(year_list)
        year_set = set(year_list)
    #   print(year_set)
        year_set = sorted(year_set)
        print(year_set)

    #   --- Now let the party begin! ---

        self.doc.start_paragraph('TCR-Title')
        self.doc.write_text('Timeline Contingeny Table')
        self.doc.end_paragraph()

        self.doc.start_table(None, 'TCR-Table')

        self.doc.start_row()
        self.doc.start_cell('TCR-HeadCell', 1)
        self.doc.start_paragraph('TCR-Name')
        self.doc.write_text("Year")#, mark)
        self.doc.end_paragraph()
        self.doc.end_cell()

        for gcount, gid in enumerate(self.__gid_list):
            self.doc.start_cell('TCR-HeadCell', 1)
            self.doc.start_paragraph('TCR-Name')
            person = self.database.get_person_from_gramps_id(gid)
            pperson = str(_Name_get_styled(person.get_primary_name()))
            self.doc.write_text('{0}\n({1})'.format(pperson,gid))
            self.doc.end_paragraph()
            self.doc.end_cell()
        self.doc.end_row()


        for yndx, year in enumerate(year_set):
    #   for yndx in range(0,1):
    #       year = year_set[yndx]
            print('Starting row',yndx,'year',year)
            test_line = str(year)

            self.doc.start_row()

            self.doc.start_cell('TCR-Entries', 1)
            self.doc.start_paragraph('TCR-Contents')
            self.doc.write_text(str(year))
            self.doc.end_paragraph()
            self.doc.end_cell()

            for pndx, gid in enumerate(self.__gid_list):
        #   for pndx in range(0,1):
        #       gid = self.pid_list[pndx]
                self.doc.start_cell('TCR-Entries', 1)

                person = self.database.get_person_from_gramps_id(gid)
                pperson = str(_Name_get_styled(person.get_primary_name()))
                print('    ',gid,pperson,year)
                
            #   for erefl in person.event_ref_list:
                for endx, erefl in enumerate(person.event_ref_list):
            #   for endx in range (0,1):
            #       erefl = person.event_ref_list[endx]
                #   endx = 0

                #   event = self.database.get_event_from_handle(erefl.get_reference_handle())
                #   print('endx:',endx,type(person.event_ref_list),len(person.event_ref_list))
                #   print('    ',person.event_ref_list)
                #   print('    ',person.event_ref_list[endx])
                #   print()
     
                    erefl = person.event_ref_list[endx]
                    event = self.database.get_event_from_handle(erefl.get_reference_handle())
                    eid = event.get_gramps_id()
                    date = event.get_date_object()
                    eyear = date.get_year()
                    etype = event.get_type()
                #   place_handle = event.get_place_handle()
                #   place = self.database.get_place_from_handle(place_handle)
                #   place_title = place_displayer.display(self.database, place)
                    place_title = self.get_place(event)
                    event_text = None
    
                    if (eyear == year):
                        event_text = '{0}; {1}\n{2}'.format(eid,etype,place_title)
                        print('         ',year,eid,etype,place_title)
                        self.doc.start_paragraph('TCR-Contents')
                        self.doc.write_text(event_text)
                        self.doc.end_paragraph()
                '''
                while eyear >= year:

                    if (eyear == year):
                        event_text = '{0}; {1}\n{2}'.format(eid,etype,place_title)
                        self.doc.start_paragraph('TCR-Contents')
                        self.doc.write_text(event_text)
                        self.doc.end_paragraph()

                    endx = ecount + 1
          #    print(endx,person.event_ref_list[ecount])
                    print(endx,len(person.event_ref_list))
                    print(endx,list(person.event_ref_list)[ecount])
                    print(endx,person.event_ref_list[ecount])
                    erefl = person.event_ref_list[endx]
                    event = self.database.get_event_from_handle(erefl.get_reference_handle())
                    eid = event.get_gramps_id()
                    date = event.get_date_object()
                    eyear = date.get_year()
                    etype = event.get_type()
                    place_handle = event.get_place_handle()
                    place = self.database.get_place_from_handle(place_handle)
                    place_title = place_displayer.display(self.database, place)

                '''

                if event_text is not None:
                    test_line = test_line + '  ' + event_text
                else:
                    test_line =' '

                self.doc.end_cell()

            print(test_line) 

            self.doc.end_row()


        self.doc.end_table()


_Name_CALLNAME_DONTUSE = 0
_Name_CALLNAME_REPLACE = 1
_Name_CALLNAME_UNDERLINE_ADD = 2


def _Name_get_styled(name):
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
        self.__table = None
        self.__pid_list = None
        MenuReportOptions.__init__(self, name, dbase)
        HERE(getframeinfo(currentframe()))
        

    def get_subject(self):
        HERE(getframeinfo(currentframe()))
        """ Return a string that describes the subject of the report. """
        TRACE(getframeinfo(currentframe()),self.__pid)
        gid = self.__pid.get_value()
        TRACE(getframeinfo(currentframe()),gid)
        print(type(gid))
        self.__pid_list = gid.split()
        TRACE(getframeinfo(currentframe()),self.__pid_list) 
        print(len(self.__pid_list)) 

    def add_menu_options(self, menu):
        HERE(getframeinfo(currentframe()))

        ##########################
        category_name = _("Report Options")
        ##########################

        self.__pid = PersonListOption(_("People of Interest"))
        gid = self.__pid.get_value()
        self.__pid.set_help(
            _("Names of people comprising columns of table."))
        menu.add_option(category_name, "pid", self.__pid)

    '''
    def set_table_columns(self,ncol):
        TRACE(getframeinfo(currentframe()),ncol)
        table = docgen.TableStyle()
        table.set_width(100)
        table.set_columns(ncol+1)
        w0 = 8
        table.set_column_width(0, w0)
        w = (100-w0)/(ncol-1)
        for c in range(1,ncol):
            print('column',c)
            table.set_column_width(c, w)

        TRACE(getframeinfo(currentframe()),ncol)

        default_style = self.__menu.get_default_style()
        TRACE(getframeinfo(currentframe()),ncol)

        default_style.add_table_style('TCR-Table', table)
        TRACE(getframeinfo(currentframe()),ncol)
    '''

    def make_default_style(self, default_style):
        '''Make default styles for Timeline Contingency Report'''
        self.get_subject()

        table = docgen.TableStyle()
        table.set_width(100.0)
        TRACE(getframeinfo(currentframe()),len(self.__pid_list)) 
        npid = len(self.__pid_list) 
        table.set_columns(npid+1)
        w0 = 7.0
        print('column 0 width =',w0)
        table.set_column_width(0, w0)
        w = (100.0-w0)/npid

        for p in range(0,npid):
            c = p+1
            print('column',c,'width =',w)
            table.set_column_width(c, w)

        default_style.add_table_style('TCR-Table', table)
        self.__table = table

        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(14)
        font.set_bold(1)
        para = docgen.ParagraphStyle()
        para.set_alignment(docgen.PARA_ALIGN_CENTER)
        para.set_font(font)
        para.set_description(_("The style used for table title"))
        default_style.add_paragraph_style('TCR-Title', para) 

        
        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(12)
        font.set_bold(1)
        para = docgen.ParagraphStyle()
        para.set_alignment(docgen.PARA_ALIGN_CENTER)
        para.set_font(font)
        para.set_description(_("The style used for names"))
        default_style.add_paragraph_style('TCR-Name', para) # *

        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(10)
        para = docgen.ParagraphStyle()
        para.set_alignment(docgen.PARA_ALIGN_LEFT)
        para.set_font(font)
        para.set_description(_("The style used for cell contents"))
        default_style.add_paragraph_style('TCR-Contents', para) # *

#       pnames = default_style.get_paragraph_style_names()

        #Table Styles
        cell = docgen.TableCellStyle()
        cell.set_padding(0.1)
        cell.set_top_border(1)
        cell.set_left_border(1)
        cell.set_right_border(1)
        default_style.add_cell_style('TCR-HeadCell', cell)

        cell = docgen.TableCellStyle()
        cell.set_padding(0.1)
        cell.set_top_border(1)
        cell.set_bottom_border(1)
        cell.set_left_border(1)
        cell.set_right_border(1)
        default_style.add_cell_style('TCR-Entries', cell)

    #   cell = docgen.TableCellStyle()
    #   cell.set_padding(0.1)
    #   cell.set_left_border(1)
    #   default_style.add_cell_style('TCR-EmptyCell', cell)

