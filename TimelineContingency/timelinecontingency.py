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
empty_birth = Event()
empty_birth.set_type(EventType.BIRTH)

empty_marriage = Event()
empty_marriage.set_type(EventType.MARRIAGE)


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
        menu = options.menu
        self.person_id    = menu.get_option_by_name('pid').get_value()
        TRACE(getframeinfo(currentframe()),type(self.person_id)) # I0166 (gid)
        TRACE(getframeinfo(currentframe()),self.person_id) # I0166 (gid)

        self.recurse      = False #menu.get_option_by_name('recurse').get_value()
        self.callname     = False #menu.get_option_by_name('callname').get_value()
        self.placeholder  = False #menu.get_option_by_name('placeholder').get_value()
        self.incl_sources = False #menu.get_option_by_name('incl_sources').get_value()
        self.incl_notes   = False #menu.get_option_by_name('incl_notes').get_value()


    def write_report(self):

        sa = SimpleAccess(self.database)

        gid_list = self.person_id.split()
        print(len(gid_list),'names:',gid_list)
        for count, gid in enumerate(gid_list):
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

            if (1): return

            '''
            head_name = str(_Name_get_styled(person.get_primary_name(),
                                         _Name_CALLNAME_DONTUSE))
            print(gid,':',head_name,person.get_primary_name().get_name())
            erl = person.get_event_ref_list()
        #   print(' erl:',type(erl),person.get_event_ref_list()) # produces EvenRef object
        #   for event_ref in person.get_event_ref_list():
            for er_count, event_ref in enumerate(person.get_event_ref_list()):
                print('    ',er_count,type(event_ref),event_ref)
                TRACE(getframeinfo(currentframe()),event_ref)

                event = self.database.get_event_from_handle(event_ref.ref)
                TRACE(getframeinfo(currentframe()),event)
                TRACE(getframeinfo(currentframe()),event.get_type())

            ''' 

        """
        Build the actual report.
        mark1 = docgen.IndexMark(_('Family Sheet'), docgen.INDEX_TYPE_TOC, 1)
        self.doc.start_paragraph('FSR-Key')
        self.doc.write_text('', mark1) # for use in a TOC in a book report
        self.doc.end_paragraph()
        """

#       mark1 = docgen.IndexMark(_('Timeline Contingeny Table'), docgen.INDEX_TYPE_TOC, 1)
        self.doc.start_paragraph('FSR-Title')
        self.doc.write_text('Timeline Contingeny Table')#, mark1) # for use in a TOC in a book report
        self.doc.end_paragraph()
        ''' 
        TRACE(getframeinfo(currentframe()),self.person_id) # I0166 (gid)
        person = self.database.get_person_from_gramps_id(self.person_id)
        TRACE(getframeinfo(currentframe()),person) # <gramps.gen.lib.person.Person object at 0x7f2adbffd5e0>
        names = person.get_alternate_names()
        TRACE(getframeinfo(currentframe()),names) 
        for count,nn in enumerate(names):
            TRACE(getframeinfo(currentframe()),count) 
            gname = nn.get_name()
            TRACE(getframeinfo(currentframe()),gname) 
        '''
        (rank, ahnentafel, person_key) = self.__calc_person_key(person)
        TRACE(getframeinfo(currentframe()),rank) # -1
        TRACE(getframeinfo(currentframe()),ahnentafel) # 0
        TRACE(getframeinfo(currentframe()),person_key) # ' '

        pperson = str(_Name_get_styled(person.get_primary_name(),
                                         _Name_CALLNAME_DONTUSE))

        TRACE(getframeinfo(currentframe()),pperson)


#       self.__process_person(person, rank, ahnentafel, person_key)

       # --- Now let the party begin! ---

#       head_name = str(_Name_get_styled(person.get_primary_name(),
#                                        _Name_CALLNAME_DONTUSE))
#       head_name = "Timeline Contingrency Table (2)"
#       mark2 = docgen.IndexMark(head_name, docgen.INDEX_TYPE_TOC, 2)

#       self.doc.start_paragraph('FSR-Key')
#       self.doc.write_text(person_key, mark2)
#       self.doc.end_paragraph()

        self.doc.start_table(None, 'FSR-Table')

        self.doc.start_row()

        self.doc.start_cell('FSR-HeadCell', 1)
        self.doc.start_paragraph('FSR-Name')
        self.doc.write_text("Year")#, mark)
        self.doc.end_paragraph()
        self.doc.end_cell()

        for c, gid in enumerate(gid_list):
            self.doc.start_cell('FSR-HeadCell', 1)
            self.doc.start_paragraph('FSR-Name')
#  note = '{0} Largest Counties; {1:,} Cases; {2:,} Deaths'.format(nG,tcases,tdeaths)
            person = self.database.get_person_from_gramps_id(gid)
            pperson = str(_Name_get_styled(person.get_primary_name(),
                                         _Name_CALLNAME_DONTUSE))

            
            print(c,type(gid),gid,pperson)
            if c == 2:
                print('----',c,type(gid),gid,pperson)
                print('    ',person.get_primary_event_ref_list())

        #   self.doc.write_text(gid)
            self.doc.write_text('{0}\n({1})'.format(pperson,gid))
            self.doc.end_paragraph()
            self.doc.end_cell()

        self.doc.end_row()

        self.doc.end_table()

  

    def __process_person(self, person, rank, ahnentafel, person_key):
        """
        Recursively build the Family Sheet for this person and all children
        with spouses.

        @param person: Person object for the key person of the Family Sheet.
        @param rank: Numerical distance between the central person in the
            database and the person in the parameter (the number of births
            needed to connect them).
        @param ahnentafel: "Ahnentafel" number of the common ancestor of the
            central person in the database and the person in the parameter,
            seen from the side of the central person in the database.
        @param person_key: Family Sheet key to be printed on the top right of
            the corner.
        """

        # List of (person, rank, ahnentafel, person_key) tuples for persons to
        # process recursively after this one.
        more_sheets = []

        # Numbering of spouses (integer, but printed in roman numbers).
        spouse_index = 0

        # Numbering of children (integer, but printed as lowercase letters).
        child_index = 0

        # Source references to print as footnotes.
        self.__citation_index = 0
        self.__citations = []

        # Notes to print as footnotes.
        self.__note_index = 0
        self.__notes = []

        # --- Now let the party begin! ---

#       head_name = str(_Name_get_styled(person.get_primary_name(),
#                                        _Name_CALLNAME_DONTUSE))
#       mark2 = docgen.IndexMark(head_name, docgen.INDEX_TYPE_TOC, 2)

#       self.doc.start_paragraph('FSR-Key')
#       self.doc.write_text(person_key, mark2)
#       self.doc.end_paragraph()

        self.doc.start_table(None, 'FSR-Table')

        # Main person
        self.doc.start_row()
        self.doc.start_cell('FSR-HeadCell', 3)
        self.__dump_person(person, False, None)
        self.doc.end_cell()
        self.doc.end_row()

        # Spouses
        for family_handle in person.get_family_handle_list():
            family = self.database.get_family_from_handle(family_handle)

            spouse_index += 1

            spouse_handle = utils.find_spouse(person, family)
            if spouse_handle:
                spouse = self.database.get_person_from_handle(spouse_handle)
            else:
                spouse = None

            # Determine relationship between the center person and the spouse.
            # If the spouse has a closer blood relationship than the current
            # person, we refer to the Family Sheet of the spouse instead of
            # printing the child list, because all children are more closely
            # related to the center person via the spouse than via the current
            # person. The same happens if the relationship is on the same
            # level, but the relationship via the spouse goes via a common
            # ancestor with a lower Ahnentafel numbering (i.e. a relationship
            # stronger father-sided). In these cases, refer_spouse will be set
            # to True.
            (spouse_rank, spouse_at, spouse_key) = \
                    self.__calc_person_key(spouse)
            if self.recurse != TimelineContingencyOptions.RECURSE_ALL:
                refer_spouse = (spouse_rank != -1 and \
                        (spouse_rank < rank or
                            (spouse_rank == rank and spouse_at < ahnentafel)))
            else:
                refer_spouse = False

            self.doc.start_row()

            self.doc.start_cell('FSR-NumberCell', 1)
            self.doc.start_paragraph('FSR-Number')
            self.doc.write_text(utils.roman(spouse_index))
            self.doc.end_paragraph()
            self.doc.end_cell()

            self.doc.start_cell('FSR-DataCell', 2)
            self.__dump_family(family, spouse)
            if refer_spouse:
                self.doc.start_paragraph('FSR-Normal')
                self.doc.write_text(_("\u2192 %s") % spouse_key)
                self.doc.end_paragraph()
            self.doc.end_cell()

            self.doc.end_row()

            if refer_spouse:
                # Spouse with closer relationship than current person? Don't
                # print children on this Family Sheet (but count them for the
                # numbering).
                child_index += len(family.get_child_ref_list())
                continue

            # Children
            for child_ref in family.get_child_ref_list():
                child = self.database.get_person_from_handle(child_ref.ref)
                child_letter = string.ascii_lowercase[child_index]

                self.doc.start_row()

                self.doc.start_cell('FSR-EmptyCell', 1)
                self.doc.end_cell()

                self.doc.start_cell('FSR-NumberCell', 1)
                self.doc.start_paragraph('FSR-Number')
                self.doc.write_text(child_letter)
                self.doc.end_paragraph()
                self.doc.end_cell()

                self.doc.start_cell('FSR-DataCell', 1)

                has_spouses = (child.get_family_handle_list() != [])

                self.__dump_person(child, has_spouses, child_ref)

                if has_spouses:
                    # We have to recalculate the key for this person, it could
                    # be closer related if it is a direct ancestor of the
                    # central person or one of its spouses.
                    (child_rank, child_at, child_key) = \
                            self.__calc_person_key(child)

                    self.doc.start_paragraph('FSR-Normal')
                    self.doc.write_text(_("\u2192 %s") % child_key)
                    self.doc.end_paragraph()

                    # We recursively print this child *only* if its
                    # relationship with the central person is closest via the
                    # current person. This way, we avoid that a person is
                    # printed recursively from more than one of its ancestors.
                    if child_key == person_key + child_letter or \
                            self.recurse == TimelineContingencyOptions.RECURSE_ALL:
                        more_sheets.append(
                                (child, child_rank, child_at, child_key))

                self.doc.end_cell()

                self.doc.end_row()

                child_index += 1

        self.doc.start_row()
        self.doc.start_cell('FSR-FootCell', 3)
        self.doc.end_cell()
        self.doc.end_row()

        self.doc.end_table()

        self.__dump_sources()
        self.__dump_notes()

        # Now print the sheets for the children.
        if self.recurse != TimelineContingencyOptions.RECURSE_NONE:
            for (child, child_rank, child_at, child_key) in more_sheets:
                self.doc.page_break()
                self.__process_person(child, child_rank, child_at, child_key)


    def __dump_family(self, family, spouse):
        """
        Output all data of a family the key person is a parent in, and all data
        of the corresponding spouse.
        """

        self.__dump_attributes(family)

        # If this is a married couple, it must at least have a marriage event.
        # If no marriage event is there, print placeholders for it
        # nevertheless.
        if family.get_relationship() == FamilyRelType.MARRIED and spouse:
            for event_ref in family.get_event_ref_list():
                event = self.database.get_event_from_handle(event_ref.ref)
                if event.get_type() == EventType.MARRIAGE:
                    break
            else:
                self.__dump_event(empty_marriage, None)

        for event_ref in family.get_event_ref_list():
            self.__dump_event_ref(event_ref)

        if spouse:
            self.__dump_person(spouse, False, family)
        else:
            self.doc.start_paragraph('FSR-Normal')
            self.__write_sources(family)
            self.__write_notes(family)
            self.doc.end_paragraph()


    def __dump_person(self, person, short, ref):
        """
        Output all data of a person.

        @param person: Person object to output.
        @param short: If True, print only name and birth event.
        @param ref: Reference through which this person is linked into the
            Family Sheet. Can be a family object (for the spouses) or a
            child_ref object (for the children). Source references and notes
            for this reference object will also be output.
        """

        name = person.get_primary_name()
        name_text = _Name_get_styled(name, self.callname, self.placeholder)

        self.doc.start_paragraph('FSR-Name')
        mark = utils.get_person_mark(self.database, person)
        self.doc.write_text("", mark)
        self.doc.write_markup(str(name_text), name_text.get_tags())
        self.__write_sources(name)
        self.__write_notes(name)
        self.__write_sources(person)
        self.__write_notes(person)
        if ref:
            self.__write_sources(ref)
            self.__write_notes(ref)
        self.doc.end_paragraph()

        if short:
            event_ref = person.get_birth_ref()
            if event_ref:
                self.__dump_event_ref(event_ref)
        else:
            for alt_name in person.get_alternate_names():
                name_type = str(alt_name.get_type())
                name = _Name_get_styled(alt_name, self.callname,
                        self.placeholder)
                self.__dump_line(name_type, name, alt_name)

            self.__dump_attributes(person)

            # Each person should have a birth event. If no birth event is
            # there, print the placeholders for it nevertheless.
            if not person.get_birth_ref():
                self.__dump_event(empty_birth, None)

            person_events = self.__sort_events_by_sdate(list(person.get_primary_event_ref_list()))
            for event_ref in person_events:
                self.__dump_event_ref(event_ref)

            for addr in person.get_address_list():
                location = utils.get_address_str(addr)
                date = gramps.gen.datehandler.get_date(addr)

                self.doc.start_paragraph('FSR-Normal')
                if date:
                    self.doc.write_text(_("Address (%(date)s): %(location)s") % {
                        'date': date,
                        'location': location})
                else:
                    self.doc.write_text(_("Address: %(location)s") % {
                        'location': location})
                self.__write_sources(addr)
                self.__write_notes(addr)
                self.doc.end_paragraph()


    def __get_event_sort_value(self, event_ref):
        """
        Helper function for sorting events
        """
        sort_value = self.database.get_event_from_handle(event_ref.ref).date.get_sort_value()
        if self.database.get_event_from_handle(event_ref.ref).get_type().is_birth():
            return -1
        return sort_value


    def __sort_events_by_sdate(self, event_ref_list):
        """
        Sort event references based on start date, birth event is always first.
        """
        return sorted(event_ref_list, key=self.__get_event_sort_value)


    def __dump_event_ref(self, event_ref):
        """
        Output all data for an event given as a reference.
        """

        event = self.database.get_event_from_handle(event_ref.ref)
        self.__dump_event(event, event_ref)


    def __dump_event(self, event, ref):
        """
        Output all data for an event.

        @param event: Event object
        @param ref: Reference through which this event is linked to the
            currently processed object. Source references and notes for this
            reference object will also be output.
        """

        description = event.get_description()
        date_text = _Event_get_date_text(event, self.placeholder)
        place_text = _Event_get_place_text(event, self.database,
                self.placeholder)

        self.doc.start_paragraph('FSR-Normal')
        self.doc.write_text("%s:" % event.get_type())
        if description:
            self.doc.write_text(" ")
            self.doc.write_text(description)
        if date_text:
            self.doc.write_text(" ")
            self.doc.write_text(date_text)
        if place_text:
            self.doc.write_text(" ")
            self.doc.write_text(place_text)
        if event.get_place_handle():
            place = self.database.get_place_from_handle(event.get_place_handle())
            self.__write_sources(place)
            self.__write_notes(place)
        self.__write_sources(event)
        self.__write_notes(event)
        if ref:
            self.__write_notes(ref)
        for attr in event.get_attribute_list():
            self.doc.write_text(_("; %(type)s: %(value)s") % {
                'type' : attr.get_type(),
                'value': attr.get_value()})
            self.__write_sources(attr)
            self.__write_notes(attr)
        self.doc.end_paragraph()


    def __dump_attributes(self, obj):
        """
        Output all attributes of the given object
        """

        for attr in obj.get_attribute_list():
            self.__dump_line(str(attr.get_type()), attr.get_value(), obj)


    def __dump_line(self, name, text, obj):
        """
        Output a name/text pair (like an attribute) with its related source
        references and notes.
        """

        self.doc.start_paragraph('FSR-Normal')
        self.doc.write_text("%s: " % name)
        if isinstance (text, StyledText):
            self.doc.write_markup(str(text), text.get_tags())
        else:
            self.doc.write_text(text)
        self.__write_sources(obj)
        self.__write_notes(obj)
        self.doc.end_paragraph()


    def __write_sources(self, obj):
        """
        Output source reference numbers for the given object (numbers like [1]
        in superscript) and collect the source references to be printed at the
        end of the report.
        """

        if not self.incl_sources:
            return

        for citation_handle in obj.get_citation_list():
            # Citation already in list? If yes, use same number again.
            if citation_handle in self.__citations:
                index = self.__citations.index(citation_handle) + 1
            else:
                self.__citations.append(citation_handle)
                self.__citation_index += 1
                index = self.__citation_index
            self.doc.start_superscript()
            self.doc.write_text(" [%s]" % index)
            self.doc.end_superscript()


    def __write_notes(self, obj):
        """
        Output note reference numbers for the given object (numbers like (1) in
        superscript) and collect the note handles to be printed at the end of
        the report.
        """

        if not self.incl_notes:
            return

        for note_handle in obj.get_note_list():
            # Note already in list? If yes, use same number again.
            if note_handle in self.__notes:
                index = self.__notes.index(note_handle) + 1
            else:
                self.__notes.append(note_handle)
                self.__note_index += 1
                index = self.__note_index
            self.doc.start_superscript()
            self.doc.write_text(" (%s)" % index)
            self.doc.end_superscript()


    def __dump_sources(self):
        """
        Print the collected sources.
        """

        if self.__citations:
            self.doc.start_paragraph('FSR-Footnote')
            self.doc.write_text("\n")
            self.doc.write_text(_("Source references:"))
            self.doc.end_paragraph()

        index = 0
        for citation_handle in self.__citations:
            citation = self.database.get_citation_from_handle(citation_handle)
            source = self.database.get_source_from_handle(citation.get_reference_handle())
            index += 1
            self.doc.start_paragraph('FSR-Footnote')
            self.doc.write_text("[%s]: " % index)
            if source.get_abbreviation():
                self.doc.write_text(source.get_abbreviation())
            else:
                if source.get_author():
                    self.doc.write_text(_("%s: ") % source.get_author())
                self.doc.write_text(source.get_title())
            self.__write_notes(source)
            if citation.get_page():
                self.doc.write_text(_(", page %s") % citation.get_page())
            self.__write_notes(citation)
            self.doc.end_paragraph()


    def __dump_notes(self):
        """
        Print the collected notes.
        """

        if self.__notes:
            self.doc.start_paragraph('FSR-Footnote')
            self.doc.write_text("\n")
            self.doc.write_text(_("Notes:"))
            self.doc.end_paragraph()

        index = 0
        for note_handle in self.__notes:
            note = self.database.get_note_from_handle(note_handle)
            index += 1
            self.doc.start_paragraph('FSR-Footnote')
            self.doc.write_text("(%s): " % index)
            self.doc.write_text(note.get())
            self.doc.end_paragraph()


    def __calc_person_key(self, person):
        """
        The person key is a unique identifier that is built from the
        relationship to the default person. It consists of the "Ahnentafel"
        number of the common ancestor of the person with the default person,
        and then a letter representing the child number for each generation
        from the common ancestor to the person.

        If more than one common ancestor exists, the common ancestor with the
        lowest "Ahnentafel" number has precedence.

        For example, the second child of the third child of the father of the
        mother of the central person gets the person key "6cb".
        """

        relationship = get_relationship_calculator()

        default_person = self.database.get_default_person()

        # No home person set.
        if default_person is None:
            return (-1, 0, "")

        # First try direct relationship.
        spousestring = ""
        info, msg = relationship.get_relationship_distance_new(
                self.database, default_person, person, all_dist=True)
        info = relationship.collapse_relations(info)[0]
        (rank, ancestor_handle, default_rel, default_fam, person_rel,
                person_fam) = info

        # Then try relationship to any spouse.
        if rank == -1:
            index = 0
            for family_handle in default_person.get_family_handle_list():
                index += 1
                family = self.database.get_family_from_handle(family_handle)
                spouse_handle = utils.find_spouse(default_person, family)
                if not spouse_handle:
                    continue
                spouse = self.database.get_person_from_handle(spouse_handle)
                info, msg = relationship.get_relationship_distance_new(
                        self.database, spouse, person, all_dist=True)
                info = relationship.collapse_relations(info)[0]
                (rank, ancestor_handle, default_rel, default_fam, person_rel,
                        person_fam) = info
                if rank != -1:
                    spousestring = utils.roman(index)
                    break
            # If no relationship found at all, exit here.
            if rank == -1:
                return (rank, 0, "")

        # Calculate Ahnentafel number of common ancestor.
        ahnentafel = 1
        for rel in default_rel:
            ahnentafel *= 2
            if rel in (relationship.REL_MOTHER,
                    relationship.REL_MOTHER_NOTBIRTH):
                ahnentafel += 1

        # Find out child letters.
        child = person
        childletters = ""
        for rel in person_rel:
            family_handle = child.get_main_parents_family_handle()
            family = self.database.get_family_from_handle(family_handle)
            if rel in (relationship.REL_MOTHER,
                    relationship.REL_MOTHER_NOTBIRTH):
                parent_handle = family.get_mother_handle()
            else:
                parent_handle = family.get_father_handle()
            parent = self.database.get_person_from_handle(parent_handle)
            # Count *all* children from this parent
            childletter = "?"
            index = 0
            for family_handle in parent.get_family_handle_list():
                family = self.database.get_family_from_handle(family_handle)
                for child_ref in family.get_child_ref_list():
                    if child_ref.ref == child.get_handle():
                        childletter = string.ascii_lowercase[index]
                        break
                    index += 1
                else:
                    continue
                break
            childletters = childletter + childletters
            child = parent

        return (rank, ahnentafel,
                "%s%s%s" % (spousestring, ahnentafel, childletters))


#------------------------------------------------------------------------
#
# Reusable functions (could be methods of gramps.gen.lib.*)
#
#------------------------------------------------------------------------

_Name_CALLNAME_DONTUSE = 0
_Name_CALLNAME_REPLACE = 1
_Name_CALLNAME_UNDERLINE_ADD = 2


def _Name_get_styled(name, callname, placeholder=False):
    """
    Return a StyledText object with the name formatted according to the
    parameters:

    @param callname: whether the callname should be used instead of the first
        name (CALLNAME_REPLACE), underlined within the first name
        (CALLNAME_UNDERLINE_ADD) or not used at all (CALLNAME_DONTUSE).
    @param placeholder: whether a series of underscores should be inserted as a
        placeholder if first name or surname are missing.
    """

    # Make a copy of the name object so we don't mess around with the real
    # data.
    n = Name(source=name)

    # Insert placeholders.
    if placeholder:
        if not n.first_name:
            n.first_name = "____________"
        if not n.get_surname():
            n.get_primary_surname().set_surname("____________")

    if n.call:
        if callname == _Name_CALLNAME_REPLACE:
            # Replace first name with call name.
            n.first_name = n.call
        elif callname == _Name_CALLNAME_UNDERLINE_ADD:
            if n.call not in n.first_name:
                # Add call name to first name.
                n.first_name = "\"%(call)s\" (%(first)s)" % {
                        'call':  n.call,
                        'first': n.first_name}

    text = displayer.display_name(n)
    tags = []

    if n.call:
        if callname == _Name_CALLNAME_UNDERLINE_ADD:
            # "name" in next line is on purpose: only underline the call name
            # if it was a part of the *original* first name
            if n.call in name.first_name:
                # Underline call name
                callpos = text.find(n.call)
                tags = [StyledTextTag(StyledTextTagType.UNDERLINE, True,
                            [(callpos, callpos + len(n.call))])]

    return StyledText(text, tags)


def _Date_get_text(date, placeholder=False):
    """
    Return a textual representation of the date to be used in textual context,
    like "on 1 January 1980" or "in January 1980" or "after January 1980".

    @param placeholder: whether a series of underscores should be inserted as a
        placeholder if the date is missing or incomplete.
    """

    text = gramps.gen.datehandler.displayer.display(date)

    if date.get_modifier() == Date.MOD_NONE \
            and date.get_quality() == Date.QUAL_NONE:
        if date.get_day_valid():
            text = _("on %(ymd_date)s") % {'ymd_date': text}
        elif date.get_month_valid():
            text = _("in %(ym_date)s") % {'ym_date': text}
        elif date.get_year_valid():
            text = _("in %(y_date)s") % {'y_date': text}

    if placeholder:
        if date.is_empty():
            text = _("on %(placeholder)s") % { 'placeholder': "__________"}
        elif not date.is_regular():
            text = _("on %(placeholder)s (%(partial)s)") % {
                    'placeholder': "__________",
                    'partial': text}

    return text


# Output placeholders for missing dates and places only for the
# following event types.
_Event_needs_date_place = [
        EventType.BIRTH,
        EventType.DEATH,
        EventType.MARRIAGE,
        EventType.DIVORCE]


def _Event_get_date_text(event, placeholder=False):
    """
    Return a textual representation of the event's date to be used in textual
    context, like "on 1 January 1980" or "in January 1980" or "after January
    1980".

    @param placeholder: whether a series of underscores should be inserted as a
        placeholder if the date is missing or incomplete.
    """

    return _Date_get_text(event.get_date_object(),
            placeholder and event.get_type() in _Event_needs_date_place)


def _Event_get_place_text(event, database, placeholder=False):
    """
    Return a textual representation of the event's place to be used in textual
    context. This is basically "in " + the place title.

    @param placeholder: whether a series of underscores should be inserted as a
        placeholder if the place is missing.
    """

    place_handle = event.get_place_handle()
    date = event.get_date_object()

    if place_handle:
        place = database.get_place_from_handle(place_handle)
        place_title = place_displayer.display(database, place, date)
        text = _("in %(place)s") % {'place': place_title}
    elif placeholder and event.get_type() in _Event_needs_date_place:
        text = _("in %(place)s") % {'place': "__________"}
    else:
        text = ""

    return text


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

    def get_subject(self):
        """ Return a string that describes the subject of the report. """
        gid = self.__pid.get_value()
        TRACE(getframeinfo(currentframe()),gid) # I0166 (gid)
        person = self.__db.get_person_from_gramps_id(gid)
        TRACE(getframeinfo(currentframe()),person) 
        names = person.get_alternate_names()
        TRACE(getframeinfo(currentframe()),names) 

        return displayer.display(person)

    def add_menu_options(self, menu):

        ##########################
        category_name = _("Report Options")
        ##########################

        self.__pid = PersonListOption(_("People of Interest"))
        self.__pid.set_help(
            _("Names of people comprising columns of table."))
        menu.add_option(category_name, "pid", self.__pid)

#       recurse = EnumeratedListOption(_("Print sheets for"), self.RECURSE_NONE)
#       recurse.set_items([
#           (self.RECURSE_NONE, _("Center person only")),
#           (self.RECURSE_SIDE, _("Center person and descendants in side branches")),
#           (self.RECURSE_ALL,  _("Center person and all descendants"))])
#       recurse.set_help(_("Whether to include descendants, and which ones."))
#       menu.add_option(category_name, "recurse", recurse)

#       callname = EnumeratedListOption(_("Use call name"), _Name_CALLNAME_DONTUSE)
#       callname.set_items([
#           (_Name_CALLNAME_DONTUSE, _("Don't use call name")),
#           (_Name_CALLNAME_REPLACE, _("Replace first name with call name")),
#           (_Name_CALLNAME_UNDERLINE_ADD, _("Underline call name in first name / add call name to first name"))])
#       callname.set_help(_("Whether to include call name, and how."))
#       menu.add_option(category_name, "callname", callname)

#       placeholder = BooleanOption( _("Print placeholders for missing information"), True)
#       placeholder.set_help(
#           _("Whether to include fields for missing information."))
#       menu.add_option(category_name, "placeholder", placeholder)

#       incl_sources = BooleanOption( _("Include sources"), True)
#       incl_sources.set_help(_("Whether to include source references."))
#       menu.add_option(category_name, "incl_sources", incl_sources)

#       incl_notes = BooleanOption( _("Include notes"), True)
#       incl_notes.set_help(_("Whether to include notes."))
#       menu.add_option(category_name, "incl_notes", incl_notes)


    def make_default_style(self, default_style):
        """Make default output style for the Family Sheet Report."""

        #Paragraph Styles
        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(10)
        font.set_bold(0)
        para = docgen.ParagraphStyle()
        para.set_font(font)
        para.set_description(_('The basic style used for the text display'))
        default_style.add_paragraph_style('FSR-Normal', para)

        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(10)
        font.set_bold(0)
        para = docgen.ParagraphStyle()
        para.set_font(font)
        para.set_alignment(docgen.PARA_ALIGN_RIGHT)
        para.set_description(_('The style used for the page key on the top'))
        default_style.add_paragraph_style('FSR-Key', para)

        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(12)
        font.set_bold(1)
        para = docgen.ParagraphStyle()
        para.set_alignment(docgen.PARA_ALIGN_CENTER)
        para.set_font(font)
        para.set_description(_("The style used for names"))
        default_style.add_paragraph_style('FSR-Name', para) # *


        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(14)
        font.set_bold(1)
        para = docgen.ParagraphStyle()
        para.set_alignment(docgen.PARA_ALIGN_CENTER)
        para.set_font(font)
        para.set_description(_("The style used for table title"))
        default_style.add_paragraph_style('FSR-Title', para) # *


        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(12)
        font.set_bold(1)
        para = docgen.ParagraphStyle()
        para.set_font(font)
        para.set_alignment(docgen.PARA_ALIGN_CENTER)
        para.set_description(_("The style used for numbers"))
        default_style.add_paragraph_style('FSR-Number', para)

        font = docgen.FontStyle()
        font.set_type_face(docgen.FONT_SANS_SERIF)
        font.set_size(8)
        font.set_bold(0)
        para = docgen.ParagraphStyle()
        para.set_font(font)
        para.set_description(_(
            'The style used for footnotes (notes and source references)'))
        default_style.add_paragraph_style('FSR-Footnote', para)

        #Table Styles
        cell = docgen.TableCellStyle()
        cell.set_padding(0.1)
        cell.set_top_border(1)
        cell.set_left_border(1)
        cell.set_right_border(1)
        default_style.add_cell_style('FSR-HeadCell', cell)

        cell = docgen.TableCellStyle()
        cell.set_padding(0.1)
        cell.set_left_border(1)
        default_style.add_cell_style('FSR-EmptyCell', cell)

        cell = docgen.TableCellStyle()
        cell.set_padding(0.1)
        cell.set_top_border(1)
        cell.set_left_border(1)
        default_style.add_cell_style('FSR-NumberCell', cell)

        cell = docgen.TableCellStyle()
        cell.set_padding(0.1)
        cell.set_top_border(1)
        cell.set_right_border(1)
        cell.set_left_border(1)
        default_style.add_cell_style('FSR-DataCell', cell)

        cell = docgen.TableCellStyle()
        cell.set_padding(0.1)
        cell.set_top_border(1)
        default_style.add_cell_style('FSR-FootCell', cell)

        table = docgen.TableStyle()
        table.set_width(100)
        table.set_columns(4)
        w0 = 8
        table.set_column_width(0, w0)
        w = (100-w0)/3
        for c in range(1,4):
            print('column',c)
            table.set_column_width(c, w)

#       table.set_column_width(0, 7)
#       table.set_column_width(1, 7)
#       table.set_column_width(2, 86)
        default_style.add_table_style('FSR-Table', table)
