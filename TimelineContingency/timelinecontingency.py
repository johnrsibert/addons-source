# Shamless plagarization of gramps/gramps/plugins/graph/gvfamilylines.py
print('Hello world from timelinecontingency.py')

from inspect import currentframe, getframeinfo
def HERE(frameinfo):
#   frameinfo = getframeinfo(currentframe())
#   print(frameinfo.filename, frameinfo.lineno)
    print('REACHED LINE', frameinfo.lineno)



print(' ')
print('---------------------------------------')
print('Hello world from timelinecontingency.py')
HERE(getframeinfo(currentframe()))

#------------------------------------------------------------------------
#
# python modules
#
#------------------------------------------------------------------------
from functools import partial
import html

import string
#------------------------------------------------------------------------
#
# Set up logging
#
#------------------------------------------------------------------------
import logging
LOG = logging.getLogger(".TimelineContingency")


#------------------------------------------------------------------------
#
# Gramps module
#
#------------------------------------------------------------------------
from gramps.gen.const import GRAMPS_LOCALE as glocale
_ = glocale.translation.gettext
from gramps.gen.lib import EventRoleType, EventType, Person, PlaceType, Date
from gramps.gen.utils.file import media_path_full
from gramps.gen.utils.thumbnails import (get_thumbnail_path, SIZE_NORMAL,
                                         SIZE_LARGE)
from gramps.gen.plug.report import Report
from gramps.gen.plug.report import utils
from gramps.gen.plug.report import MenuReportOptions
from gramps.gen.plug.report import stdoptions
from gramps.gen.plug.menu import (NumberOption, ColorOption, BooleanOption,
                                  EnumeratedListOption, PersonListOption,
                                  SurnameColorOption)
from gramps.gen.utils.db import get_birth_or_fallback, get_death_or_fallback
from gramps.gen.proxy import CacheProxyDb
from gramps.gen.errors import ReportError
from gramps.gen.display.place import displayer as _pd

from gramps.gen.plug import docgen

#------------------------------------------------------------------------
#
# A quick overview of the classes we'll be using:
#
#   class TimelineContingencyOptions(MenuReportOptions)
#       - this class is created when the report dialog comes up
#       - all configuration controls for the report are created here
#
#   class TimelineContingencyReport(Report)
#       - this class is created only after the user clicks on "OK"
#       - the actual report generation is done by this class
#
#------------------------------------------------------------------------
# <option name="gidlist" value="I0003 I0222 I0223 I0217 I0216 I0170 I0166 I0108 "/>


class TimelineContingencyOptions(MenuReportOptions):
    HERE(getframeinfo(currentframe()))

    def __init__(self, name, dbase):
        HERE(getframeinfo(currentframe()))
        print('start def __init__(self, name, dbase)')
        print('name:',name)
        self.limit_parents = None
        self.max_parents = None
        self.limit_children = None
        self.max_children = None
        self.include_images = None
        self.image_location = None
        self.justyears = None
        self.include_dates = None

        MenuReportOptions.__init__(self, name, dbase)
        print('finish def __init__(self, name, dbase)')


    def add_menu_options(self, menu):
        HERE(getframeinfo(currentframe()))
        print('start def add_menu_options(self, menu):')

        # ---------------------
        category_name = _('Report Options')
        add_option = partial(menu.add_option, category_name)
        # ---------------------

#       followpar = BooleanOption(_('Follow parents to determine '
#                                   '"family lines"'), True)
#       followpar.set_help(_('Parents and their ancestors will be '
#                            'considered when determining "family lines".'))
#       add_option('followpar', followpar)

#       followchild = BooleanOption(_('Follow children to determine '
#                                     '"family lines"'), True)
#       followchild.set_help(_('Children will be considered when '
#                              'determining "family lines".'))
#       add_option('followchild', followchild)

#       remove_extra_people = BooleanOption(_('Try to remove extra '
#                                             'people and families'), True)
#       remove_extra_people.set_help(_('People and families not directly '
#                                      'related to people of interest will '
#                                      'be removed when determining '
#                                      '"family lines".'))
#       add_option('removeextra', remove_extra_people)

#       arrow = EnumeratedListOption(_("Arrowhead direction"), 'd')
#       for i in range( 0, len(_ARROWS) ):
#           arrow.add_item(_ARROWS[i]["value"], _ARROWS[i]["name"])
#       arrow.set_help(_("Choose the direction that the arrows point."))
#       add_option("arrow", arrow)

#       color = EnumeratedListOption(_("Graph coloring"), "filled")
#       for COLOR in _COLORS:
#           color.add_item(COLOR["value"], COLOR["name"])
#       color.set_help(_("Males will be shown with blue, females "
#                        "with red, unless otherwise set above for filled. "
#                        "If the sex of an individual "
#                        "is unknown it will be shown with gray."))
#       add_option("color", color)

#       roundedcorners = EnumeratedListOption(_("Rounded corners"), '')
#       for i in range( 0, len(_CORNERS) ):
#           roundedcorners.add_item(_CORNERS[i]["value"], _CORNERS[i]["name"])
#       roundedcorners.set_help(_("Use rounded corners e.g. to differentiate "
#                        "between women and men."))
#       add_option("useroundedcorners", roundedcorners)

#       stdoptions.add_gramps_id_option(menu, category_name, ownline=True)

#       # ---------------------
#       category_name = _('Report Options (2)')
#       add_option = partial(menu.add_option, category_name)
#       # ---------------------

#       stdoptions.add_name_format_option(menu, category_name)

#       stdoptions.add_private_data_option(menu, category_name, default=False)

#       stdoptions.add_living_people_option(menu, category_name)

#       locale_opt = stdoptions.add_localization_option(menu, category_name)

#       stdoptions.add_date_format_option(menu, category_name, locale_opt)

#       use_subgraphs = BooleanOption(_('Use subgraphs'), True)
#       use_subgraphs.set_help(_("Subgraphs can help Graphviz position "
#                                "spouses together, but with non-trivial "
#                                "graphs will result in longer lines and "
#                                "larger graphs."))
#       add_option("usesubgraphs", use_subgraphs)

        HERE(getframeinfo(currentframe()))
        # --------------------------------
        add_option = partial(menu.add_option, _('People of Interest'))
        # --------------------------------

        HERE(getframeinfo(currentframe()))
        person_list = PersonListOption(_('People of interest'))
        person_list.set_help(_('People to ovelay as columns in time line contingency table.'))
        add_option('gidlist', person_list)
        HERE(getframeinfo(currentframe()))

#       self.limit_parents = BooleanOption(_('Limit the number of ancestors'),
#                                          False)
#       self.limit_parents.set_help(_('Whether to '
#                                     'limit the number of ancestors.'))
#       add_option('limitparents', self.limit_parents)
#       self.limit_parents.connect('value-changed', self.limit_changed)

#       self.max_parents = NumberOption('', 50, 10, 9999)
#       self.max_parents.set_help(_('The maximum number '
#                                   'of ancestors to include.'))
#       add_option('maxparents', self.max_parents)

#       self.limit_children = BooleanOption(_('Limit the number '
#                                             'of descendants'),
#                                           False)
#       self.limit_children.set_help(_('Whether to '
#                                      'limit the number of descendants.'))
#       add_option('limitchildren', self.limit_children)
#       self.limit_children.connect('value-changed', self.limit_changed)

#       self.max_children = NumberOption('', 50, 10, 9999)
#       self.max_children.set_help(_('The maximum number '
#                                    'of descendants to include.'))
#       add_option('maxchildren', self.max_children)

#       # --------------------
#       category_name = _('Include')
#       add_option = partial(menu.add_option, category_name)
#       # --------------------

#       self.include_dates = BooleanOption(_('Include dates'), True)
#       self.include_dates.set_help(_('Whether to include dates for people '
#                                     'and families.'))
#       add_option('incdates', self.include_dates)
#       self.include_dates.connect('value-changed', self.include_dates_changed)

#       self.justyears = BooleanOption(_("Limit dates to years only"), False)
#       self.justyears.set_help(_("Prints just dates' year, neither "
#                                 "month or day nor date approximation "
#                                 "or interval are shown."))
#       add_option("justyears", self.justyears)

#       include_places = BooleanOption(_('Include places'), True)
#       include_places.set_help(_('Whether to include placenames for people '
#                                 'and families.'))
#       add_option('incplaces', include_places)

#       include_num_children = BooleanOption(_('Include the number of '
#                                              'children'), True)
#       include_num_children.set_help(_('Whether to include the number of '
#                                       'children for families with more '
#                                       'than 1 child.'))
#       add_option('incchildcnt', include_num_children)

#       self.include_images = BooleanOption(_('Include '
#                                             'thumbnail images of people'),
#                                           True)
#       self.include_images.set_help(_('Whether to '
#                                      'include thumbnail images of people.'))
#       add_option('incimages', self.include_images)
#       self.include_images.connect('value-changed', self.images_changed)

#       self.image_location = EnumeratedListOption(_('Thumbnail location'), 0)
#       self.image_location.add_item(0, _('Above the name'))
#       self.image_location.add_item(1, _('Beside the name'))
#       self.image_location.set_help(_('Where the thumbnail image '
#                                      'should appear relative to the name'))
#       add_option('imageonside', self.image_location)

#       self.image_size = EnumeratedListOption(_('Thumbnail size'), SIZE_NORMAL)
#       self.image_size.add_item(SIZE_NORMAL, _('Normal'))
#       self.image_size.add_item(SIZE_LARGE, _('Large'))
#       self.image_size.set_help(_('Size of the thumbnail image'))
#       add_option('imagesize', self.image_size)

#       # ----------------------------
#       add_option = partial(menu.add_option, _('Family Colors'))
#       # ----------------------------

#       surname_color = SurnameColorOption(_('Family colors'))
#       surname_color.set_help(_('Colors to use for various family lines.'))
#       add_option('surnamecolors', surname_color)

#       # -------------------------
#       add_option = partial(menu.add_option, _('Individuals'))
#       # -------------------------

#       color_males = ColorOption(_('Males'), '#e0e0ff')
#       color_males.set_help(_('The color to use to display men.'))
#       add_option('colormales', color_males)

#       color_females = ColorOption(_('Females'), '#ffe0e0')
#       color_females.set_help(_('The color to use to display women.'))
#       add_option('colorfemales', color_females)

#       color_unknown = ColorOption(_('Unknown'), '#e0e0e0')
#       color_unknown.set_help(_('The color to use '
#                                'when the gender is unknown.'))
#       add_option('colorunknown', color_unknown)

#       color_family = ColorOption(_('Families'), '#ffffe0')
#       color_family.set_help(_('The color to use to display families.'))
#       add_option('colorfamilies', color_family)

#       self.limit_changed()
#       self.images_changed()

   
        print('finish def add_menu_options(self, menu):')
        HERE(getframeinfo(currentframe()))

class TimelineContingencyReport(Report):
    HERE(getframeinfo(currentframe()))
    def __init__(self, database, options, user):
        HERE(getframeinfo(currentframe()))
        print('starting TimelineContingency.Report.__init__')       
        Report.__init__(self, database, options, user)
        print('finished TimelineContingency.Report.__init__')       

        HERE(getframeinfo(currentframe()))
        menu = options.menu
        get_option_by_name = menu.get_option_by_name
        get_value = lambda name: get_option_by_name(name).get_value()

        HERE(getframeinfo(currentframe()))
#       self.set_locale(menu.get_option_by_name('trans').get_value())

        HERE(getframeinfo(currentframe()))
#       stdoptions.run_date_format_option(self, menu)

        HERE(getframeinfo(currentframe()))
#       stdoptions.run_private_data_option(self, menu)
#       stdoptions.run_living_people_option(self, menu, self._locale)
        self.database = CacheProxyDb(self.database)
        self._db = self.database
        HERE(getframeinfo(currentframe()))


       # initialize several convenient variables
        self._people = set() # handle of people we need in the report
        self._families = set() # handle of families we need in the report
        self._deleted_people = 0
        self._deleted_families = 0
        self._user = user
        HERE(getframeinfo(currentframe()))

#       self._followpar = get_value('followpar')
#       self._followchild = get_value('followchild')
#       self._removeextra = get_value('removeextra')
        HERE(getframeinfo(currentframe()))
        self._gidlist = get_value('gidlist')
#       self._colormales = get_value('colormales')
#       self._colorfemales = get_value('colorfemales')
#       self._colorunknown = get_value('colorunknown')
#       self._colorfamilies = get_value('colorfamilies')
#       self._limitparents = get_value('limitparents')
#       self._maxparents = get_value('maxparents')
#       self._limitchildren = get_value('limitchildren')
#       self._maxchildren = get_value('maxchildren')
#       self._incimages = get_value('incimages')
#       self._imageonside = get_value('imageonside')
#       self._imagesize = get_value('imagesize')
#       self._useroundedcorners = get_value('useroundedcorners')
#       self._usesubgraphs = get_value('usesubgraphs')
#       self._incdates = get_value('incdates')
#       self._just_years = get_value('justyears')
#       self._incplaces = get_value('incplaces')
#       self._incchildcount = get_value('incchildcnt')
#       self.includeid = get_value('inc_id')

        # the gidlist is annoying for us to use since we always have to convert
        # the GIDs to either Person or to handles, so we may as well convert the
        # entire list right now and not have to deal with it ever again
        self._interest_set = set()
        if not self._gidlist:
            raise ReportError(_('Empty report'),
                              _('You did not specify anybody'))
        HERE(getframeinfo(currentframe()))
#       print(gidlist)
        print(self._gidlist)
        for gid in self._gidlist.split():
            person = self._db.get_person_from_gramps_id(gid)
            if person:
                #option can be from another family tree, so person can be None
                self._interest_set.add(person.get_handle())

        HERE(getframeinfo(currentframe()))
#       print(gidlist)
        print(self._gidlist)
#       stdoptions.run_name_format_option(self, menu)
        HERE(getframeinfo(currentframe()))

         
    HERE(getframeinfo(currentframe()))




    def begin_report(self):
        print('reached def begin_report(self)')

        """ write the report """
        mark1 = docgen.IndexMark(_('Timeline Contingency Table'), docgen.INDEX_TYPE_TOC, 1)
        self.doc.start_paragraph('FSR-Key')
        self.doc.write_text('', mark1) # for use in a TOC in a book report
        self.doc.end_paragraph()


        print('finished def begin_report(self)')

