#-*- coding:utf-8 -*-

"""
CyclingLog's Telegram bot interface controller

Copyright (c) 2017 Jorge Luis Rodriguez <jorgeluisrmx@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import unicode_literals
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide, InlineKeyboardMarkup, InlineKeyboardButton
import logging
from fysom import Fysom
from cyclinglog.controllers.user import User
from cyclinglog.models.stage import Stage
from cyclinglog.models.activity import Activity, ManualActivity, GpxActivity, ActivityError, InvalidTypeError

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# emojis dictionary
emojis = {
    u'bike': u'\U0001f6b2',
    u'cycling': u'\U0001f6b4',
    u'rocket': u'\U0001f680',
    u'mountain': u'\u26f0',
    u'camp_tent': u'\U0001f3d5',
    u'plus': u'\u2795',
    u'tick': u'\u2705'
}


# message commnds dictionary
msg_comm = {
    # activity exploration labels
    u'explore_actvivities': emojis['rocket'] + u' Explore activities',
    u'totals': u'Totals',
    u'rankings': u'Rankings',
    u'stage_summary': u"Stage's summary",
    u'month_summary': u"Month's summary",
    u'year_summary': u"Year's summary",
    u'route_summary': u"Route's summary",
#    u'summary_by_date': u'Summary by date',
#    u'trends': u'Trends',
#    u'activity_inspection': u'Inspect activity',

    # adding activities labels
    u'add_activity': emojis['cycling'] + u' Add an activity',
    u'add_manual_activity': u'+ MANUAL activity',
    u'add_gpx_activity': u'+ GPX activity',
    u'add_stage': u'+ STAGE',

    #others
    u'main_menu': u'Main menu',
    u'cancel': u'Cancel',
    u'restart': u'restart'
}


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class CLBot(object):

    def __init__(self, msg_pass_fun=None):
        """
        Class constructor

        :param msg_pass_fun: function to send status messages to a desired destination outside class
        :type msg_pass_fun: function
        """
        # CHAPTER ZERO: THE COMMANDS
            # message commands dictionary
        self._mcomm = msg_comm
            # reverse message commands dictionary
        self._r_mcomm = {value: key for key, value in msg_comm.items()}
            # activity to be added
        self._acty = None
            # activty attribute to be setted
        self._aattr = None


        # CHAPTER ONE: THE FSM BEHIND THE BOT
            # fsm structure
        fsm_struct = {
            'initial': 'MAIN_MENU',
            'events': [
                # event, state, state
                {'name': 'add_activity', 'src': 'MAIN_MENU', 'dst': 'ADD_ACTIVITY'},
                {'name': 'explore_actvivities', 'src': 'MAIN_MENU', 'dst': 'ACTIVITY_EXPLORATION'},
                {'name': 'main_menu', 'src': ['ADD_ACTIVITY', 'ACTIVITY_EXPLORATION'], 'dst': 'MAIN_MENU'},

                {'name': 'add_manual_activity', 'src': 'ADD_ACTIVITY', 'dst': 'MANUAL_ACTIVITY'},
                {'name': 'add_gpx_activity', 'src': 'ADD_ACTIVITY', 'dst': 'GPX_ACTIVITY'},
                {'name': 'to_gpx_activity', 'src': '*', 'dst': 'GPX_ACTIVITY'},
                {'name': 'add_stage', 'src': 'ADD_ACTIVITY', 'dst': 'STAGE'},
                {'name': 'cancel', 'src': ['MANUAL_ACTIVITY', 'GPX_ACTIVITY', 'STAGE'], 'dst': 'ADD_ACTIVITY'},

                {'name': 'totals', 'src': 'ACTIVITY_EXPLORATION', 'dst': '='},
                {'name': 'rankings', 'src': 'ACTIVITY_EXPLORATION', 'dst': '='},
                {'name': 'stage_summary', 'src': 'ACTIVITY_EXPLORATION', 'dst': '='},
                {'name': 'month_summary', 'src': 'ACTIVITY_EXPLORATION', 'dst': '='},
                {'name': 'year_summary', 'src': 'ACTIVITY_EXPLORATION', 'dst': '='},
                {'name': 'route_summary', 'src': 'ACTIVITY_EXPLORATION', 'dst': '='},
                {'name': 'summary_by_date', 'src': 'ACTIVITY_EXPLORATION', 'dst': 'SUMMARY_BY_DATE'},
                {'name': 'trends', 'src': 'ACTIVITY_EXPLORATION', 'dst': 'TRENDS'},
                {'name': 'activity_inspection', 'src': 'ACTIVITY_EXPLORATION', 'dst': 'S_ACTIVITY_EXPLORE'},
                {'name': 'cancel', 'src': ['SUMMARY_BY_DATE', 'TRENDS', 'S_ACTIVITY_EXPLORE'], 'dst': 'ACTIVITY_EXPLORATION'},

                {'name': 'restart', 'src': '*', 'dst': 'MAIN_MENU'}
            ],
            'callbacks': {
                'onmain_menu': self.on_main_menu,

                'onexplore_actvivities': self.on_explore_actvivities,
                'ontotals': self.on_totals,
                'onrankings': self.on_rankings,
                'onstage_summary': self.on_stage_summary,
                'onmonth_summary': self.on_month_summary,
                'onyear_summary': self.on_year_summary,
                'onroute_summary': self.on_route_summary,

                'onadd_activity': self.on_add_activity,
                'onadd_manual_activity': self.on_add_manual_activity,
                'onadd_gpx_activity': self.on_add_gpx_activity,
                'onadd_stage': self.on_add_stage,

                'oncancel': self.on_cancel,
                'onrestart': self.on_restart
            }
        }

            # create fms object
        self._fsm = Fysom(fsm_struct)

        # CHAPTER TWO: THE BOT
            # create and configure telegram bot connection
        self._updater = Updater(User.get_telegram_bot_config()['token'])
            # adding handlers
                # commands
        self._updater.dispatcher.add_handler(CommandHandler('start', self.start_handler))
                # content handlers
        self._updater.dispatcher.add_handler(MessageHandler([Filters.text], self.message_handler))
        self._updater.dispatcher.add_handler(MessageHandler([Filters.document], self.capture_file_handler))
        self._updater.dispatcher.add_error_handler(self.error_handler)
            # starting bot polliing
        if not msg_pass_fun:
            # TODO: Change print for logging
            print "Starting CyclingLogBot..."
        self._updater.start_polling()
        self._updater.idle()


    # - - - - - - - - - - - -
    # CUSTOM KEYBOARD METHODS
    # - - - - - - - - - - - -

    def _main_menu_kb(self):
        """
        Main menu custom keyboard
        """
        custom_keyboard = [
            [ self._mcomm['explore_actvivities'] ],
            [ self._mcomm['add_activity'] ]
        ]
        return ReplyKeyboardMarkup(custom_keyboard)


    def _add_activity_kb(self):
        """
        Add activity custom keyboard
        """
        custom_keyboard = [
            [ self._mcomm['add_manual_activity'], self._mcomm['add_gpx_activity'] ],
            [ self._mcomm['add_stage'], self._mcomm['main_menu'] ]
        ]
        return ReplyKeyboardMarkup(custom_keyboard)


    def _manual_activity_kb(self):
        """
        Adding manual activity custom keyboard
        """
        custom_keyboard = [[u'+ ' + attr] for attr in self._acty.requiered_attrs()]
        if self._acty.ready():
            custom_keyboard.append([u'SAVE ACTIVITY'])
        custom_keyboard.extend([[u'set ' + attr] for attr in  self._acty.optional_attrs()])
        custom_keyboard.append([ self._mcomm['cancel'] ])
        return ReplyKeyboardMarkup(custom_keyboard)


    def _gpx_activity_kb(self):
        """
        Adding gpx activity custom keyboard
        """

        custom_keyboard= [[u'SAVE ACTIVITY']]
        custom_keyboard.extend([[u'+ ' + attr] for attr in self._acty.extra_info()])
        custom_keyboard.extend([[u'set ' + attr] for attr in  self._acty.settable_attrs()])
        custom_keyboard.append([ self._mcomm['cancel'] ])
        return ReplyKeyboardMarkup(custom_keyboard)


    def _attribute_options_kb(self, attribute):
        """
        Return a keyboard containing the options founded in DB for each attribute
        """
        if attribute == 'route':
            custom_keyboard = [[opt] for opt in self._acty.routes()]
        elif attribute == 'mod':
            custom_keyboard = [[opt] for opt in self._acty.mods()]
        elif attribute == 'stage':
            custom_keyboard = [[opt] for opt in self._acty.stages()]
        elif attribute == 'toi_label':
            custom_keyboard = [[opt] for opt in self._acty.toi_labels()]
        elif attribute == 'cycle':
            custom_keyboard = [[u'True'], [u'False']]
        else:
            return self._hide_custom_keyboard()
        return ReplyKeyboardMarkup(custom_keyboard)


    def _activity_exploration_kb(self):
        """
        Activity exploration custom keyboard
        """
        custom_keyboard = [
            [ self._mcomm['totals'] ],
            [ self._mcomm['rankings'] ],
            [ self._mcomm['stage_summary'] ],
            [ self._mcomm['month_summary'] ],
            [ self._mcomm['year_summary'] ],
            [ self._mcomm['route_summary'] ],
            [ self._mcomm['main_menu'] ]
        ]
        return ReplyKeyboardMarkup(custom_keyboard)

    def _cancel_kb(self):
        """
        Cancel custom keyboard
        """
        custom_keyboard = [
            [ self._mcomm['cancel'] ]
        ]
        return ReplyKeyboardMarkup(custom_keyboard)

    def _hide_custom_keyboard(self):
        """
        Hide custom keyboard
        """
        return ReplyKeyboardHide()


    # - - - - - - - - - - - -
    # MESSAGE SENDING METHODS
    # - - - - - - - - - - - -

    def _send_msg(self, bot, update, msg=None, keyboard=None, markdown=False, html=False):
        """
        Send a message to telegram chat contained in update
        """
        if markdown:
            bot.sendMessage(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown', reply_markup=keyboard)
        elif html:
            bot.sendMessage(chat_id=update.message.chat_id, text=msg, parse_mode='HTML', reply_markup=keyboard)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text=msg, reply_markup=keyboard)


    def _send_fsm_state(self, bot, update):
        self._send_msg(bot, update, 'fsm STATE: {}'.format(self._fsm.current))


    # - - - - - - -
    # FSM CALLBACKS
    # - - - - - - -

    def on_main_menu(self, e):
        self._send_msg(e.bot, e.update, msg='Choose an option:', keyboard=self._main_menu_kb())

    def on_explore_actvivities(self, e):
        self._send_msg(e.bot, e.update, msg='Choose an option:', keyboard=self._activity_exploration_kb())

    def on_totals(self, e):
        summ = Activity.totals()
        fmsg = """\U0001f6b4  *TOTALS*  \U0001f6b4

*#*  :    *{r[tracks]}*
\U0001f3c1:    *{r[distance]:,.2f} km*
\u26f0:    +*{r[elev_gain]:,.2f} m*
\u23f3:    +*{r[time]}*
\u23f1:    +*{r[time_moving]}*
\U0001f422:    {r[min_speed_moving]:,.2f} km/h
\U0001f430:    {r[max_speed_moving]:,.2f} km/h
\U0001f682:    {r[avg_speed_moving]:,.2f} km/h
\U0001f3ce:    {r[highest_speed]:,.2f} km/h
\U0001f985:    {r[elev_max]:,.2f} m
\U0001f41c:    {r[elev_min]:,.2f} m
\U0001f3a2:    +{r[elev_loss]:,.2f} m
\U0001f4c6:    {r[date_from]} to {r[date_to]}""".format(r=summ)
        self._send_msg(e.bot, e.update, msg=fmsg, markdown=True)

    def on_rankings(self, e):
        pass

    def on_stage_summary(self, e):
        summ = Activity.summary_by_stage()
        for row in summ:
            te = '' if row['not_null_time_tracks']==row['tracks'] else '+'
            ge = '' if row['not_null_elev_gain_tracks']==row['tracks'] else '+'
            fmsg = """\U0001f3c5  *{r[stage]}*

*#*  :    *{r[tracks]}*
\U0001f3c1:    *{r[total_distance]:,.2f} km*
\u26f0:    {ge}*{r[total_elev_gain]:,.2f} m*
\u23f3:    {te}{r[total_time]}
\u23f1:    {te}{r[total_time_moving]}
\U0001f4c6:    {r[date_from]} to {r[date_to]}""".format(r=row, ge=ge, te=te)
            self._send_msg(e.bot, e.update, msg=fmsg, markdown=True)

    def on_month_summary(self, e):
        summ = Activity.summary_by_month()
        for row in summ:
            te = '' if row['not_null_time_tracks']==row['tracks'] else '+'
            ge = '' if row['not_null_elev_gain_tracks']==row['tracks'] else '+'
            fmsg = u"""\U0001f6b4  *{r[date]}*  \U0001f6b4

*#*  :    *{r[tracks]}*
\U0001f3c1:    *{r[total_distance]:,.2f} km*
\u26f0:    {ge}*{r[total_elev_gain]:,.2f} m*
\u23f3:    {te}{r[total_time]}
\u23f1:    {te}{r[total_time_moving]}
\U0001f4c6:    {r[date_from]} to {r[date_to]}""".format(r=row, ge=ge, te=te)
            self._send_msg(e.bot, e.update, msg=fmsg, markdown=True)

    def on_year_summary(self, e):
        summ = Activity.summary_by_year()
        for row in summ:
            te = '' if row['not_null_time_tracks']==row['tracks'] else '+'
            ge = '' if row['not_null_elev_gain_tracks']==row['tracks'] else '+'
            fmsg = """\U0001f6b4  *{r[year]}*  \U0001f6b4

*#*  :    *{r[tracks]}*
\U0001f3c1:    *{r[total_distance]:,.2f} km*
\u26f0:    {ge}*{r[total_elev_gain]:,.2f} m*
\u23f3:    {te}{r[total_time]}
\u23f1:    {te}{r[total_time_moving]}
\U0001f4c6:    {r[date_from]} to {r[date_to]}""".format(r=row, ge=ge, te=te)
            self._send_msg(e.bot, e.update, msg=fmsg, markdown=True)

    def on_route_summary(self, e):
        summ = Activity.summary_by_route()
        for row in summ:
            te = '' if row['not_null_time_tracks']==row['tracks'] else '+'
            ge = '' if row['not_null_elev_gain_tracks']==row['tracks'] else '+'
            fmsg = """\U0001f6b4  *{r[route]}*  \U0001f6b4

*#*  :    *{r[tracks]}*
\U0001f3c1:    *{r[total_distance]:,.2f} km*
\u26f0:    {ge}*{r[total_elev_gain]:,.2f} m*
\u23f3:    {te}{r[total_time]}
\u23f1:    {te}{r[total_time_moving]}
\U0001f4c6:    {r[date_from]} to {r[date_to]}""".format(r=row, ge=ge, te=te)
            self._send_msg(e.bot, e.update, msg=fmsg, markdown=True)

    def on_add_activity(self, e):
        self._send_msg(e.bot, e.update, msg='Choose an option:', keyboard=self._add_activity_kb())

    def on_add_manual_activity(self, e):
        self._acty = ManualActivity()
        self._aattr = None
        self._send_msg(e.bot, e.update, msg="<b>NEW MANUAL ACTIVITY</b>\n\n{}\n\nChoose an option:".format(self._acty.current_state()), keyboard=self._manual_activity_kb(), html=True)

    def on_add_gpx_activity(self, e):
        self._send_msg(e.bot, e.update, msg='Ok, *send me a valid GPX file*:', keyboard=self._cancel_kb(), markdown=True)

    def on_add_stage(self, e):
        self._send_msg(e.bot, e.update, msg='Send me the *name of the new stage*\n(or type Cancel to go back):', keyboard=self._hide_custom_keyboard(), markdown=True)

    def on_cancel(self, e):
        r_kb = None
        if e.dst == 'ADD_ACTIVITY':
            self._acty, self._aattr = None, None
            r_kb = self._add_activity_kb()
        elif e.dst == 'ACTIVITY_EXPLORATION':
            r_kb = self._activity_exploration_kb()
        self._send_msg(e.bot, e.update, msg='Choose an option:', keyboard=r_kb)

    def on_restart(self, e):
        if hasattr(e, 'bot') and hasattr(e, 'update'):
            self._send_msg(e.bot, e.update, msg='Choose an option:', keyboard=self._main_menu_kb())


    # - - - - - - - - - - - - - - -
    # ADDING ACTIVITIES CONTROLLERS
    # - - - - - - - - - - - - - - -

    def activity_kb(self):
        return self._gpx_activity_kb() if self._fsm.current == 'GPX_ACTIVITY' else self._manual_activity_kb()


    def adding_activity_ctlr(self, bot, update):
        """
        Controller for adding a new activity, manual or gpx
        """
        # setting variables
        in_msg = update.message.text
        aty_type = 'GPX' if self._fsm.current == 'GPX_ACTIVITY' else 'MANUAL'

        # in_msg processing
        if in_msg == u'SAVE ACTIVITY':
            try:
                self._acty.save()
                self._send_msg(bot, update, msg="{} *NEW {} ACTIVITY added successfully*".format(emojis['tick'], aty_type), markdown=True)
                # return to add activity menu
                self._fsm.trigger('cancel', bot=bot, update=update)
            except Exception as e:
                self._send_msg(bot, update, "{}".format(e), keyboard=self.activity_kb())
        elif not self._aattr:
            validated = False
            if in_msg.startswith('+ ') or in_msg.startswith('set '):
                self._aattr = in_msg.replace(u'+ ','') if in_msg.startswith('+ ') else in_msg.replace(u'set ','')
                if (self._fsm.current=='MANUAL_ACTIVITY') and ( self._aattr in (self._acty.requiered_attrs() + self._acty.optional_attrs()) ):
                    validated = True
                elif (self._fsm.current == 'GPX_ACTIVITY') and ( self._aattr in (self._acty.extra_info() + self._acty.settable_attrs()) ):
                    validated = True
            if validated:
                self._send_msg(bot, update, msg="Send me the *value for {}*:".format(self._aattr), keyboard=self._attribute_options_kb(self._aattr), markdown=True)
            else:
                self._send_msg(bot, update, msg="*Invalid command*. Try again choosing an option:", keyboard=self.activity_kb(), markdown=True)
        else:
            try:
                self._acty.set_by_name(self._aattr, in_msg)
                self._aattr = None
                self._send_msg(bot, update, msg="<b>NEW {} ACTIVITY</b>\n\n{}\n\nChoose an option:".format(aty_type, self._acty.current_state()), keyboard=self.activity_kb(), html=True)
            except InvalidTypeError as e:
                self._send_msg(bot, update, msg="*{}*\n\nLet's try again. Send me the *value for {}*:".format(e, self._aattr), markdown=True)
            except ActivityError as e:
                self._aattr = None
                self._send_msg(bot, update, msg="*{}*\n\nChoose an option:".format(e), keyboard=self.activity_kb(), markdown=True)


    def adding_stage_ctlr(self, bot, update):
        """
        Controller for adding a new stage
        """
        in_msg = update.message.text
        try:
            Stage.add_stage(in_msg)
            self._send_msg(bot, update, """{} *'{}' added successfully*\n\nThe *available stages* are:\n{}""".format(emojis['tick'], in_msg, u"\n".join(Stage.get_names())), markdown=True)
            # return to add activity menu
            self._fsm.trigger('cancel', bot=bot, update=update)
        except Exception as e:
            self._send_msg(bot, update, "*{}*\n\nLet's *try another name*:".format(e), markdown=True)

    # - - - - - - - - - - - - - - - -
    # EXPLORE ACTIVITIES CONTROLLERS
    # - - - - - - - - - - - - - - - -

    # - - - - - -
    # BOT METHODS
    # - - - - - -

    def start_handler(self, bot, update):
        """
        /start command handler
        """
        if update.message.from_user.username == User.current_user():        # user validation
            # restart fsm
            self._fsm.restart()

            # send main menu
            self._send_msg(bot, update, keyboard=self._main_menu_kb(),
                                msg='Welcome to your {} CyclingLog @{}, please pick an option from the menu'.format(emojis['cycling'], User.current_user()))

        else:   # not valid user
            self._send_msg(bot, update, 'Upss!! your username does not match, sorry!!!')


    def message_handler(self, bot, update):
        """
        General text messages handler
        """
        if update.message.from_user.username == User.current_user():      # user validation
            in_msg = update.message.text

            # FSM COMMANDS PROCESSING
            if in_msg in self._r_mcomm:     # if incoming mesg in r_msg_comm
                in_comm = self._r_mcomm[in_msg]     # recover valid commnd
                # if commands can be applied
                if self._fsm.can(in_comm):
                    self._fsm.trigger(in_comm, bot=bot, update=update)
                else:
                    self._fsm.restart()
                    self._send_msg(bot, update, 'Invalid command!!!', keyboard=self._main_menu_kb())

            # NON-FSM COMMANDS PROCESSING
            else:
                if self._fsm.current == 'STAGE':
                    self.adding_stage_ctlr(bot, update)
                elif self._fsm.current == 'MANUAL_ACTIVITY':
                    self.adding_activity_ctlr(bot, update)
                elif self._fsm.current == 'GPX_ACTIVITY':
                    self.adding_activity_ctlr(bot, update)
                else:
                    self._send_msg(bot, update, 'Invalid command!!!', self._hide_custom_keyboard())
                    self._send_msg(bot, update, "{0} - {0:s}".format(in_msg), self._hide_custom_keyboard())
                    print "{0} - {0:s}".format(in_msg)
                    print str(in_msg)

        else:   # not valid user
            self._send_msg(bot, update, 'Upss!! your username does not match, sorry!!!')


    def capture_file_handler(self, bot, update):
        """
        Arriving files handler
        """
        # determin if the new file is a *.gpx one
        if update.message.document.file_name.endswith('.gpx'):
            # get the new file and add download it to the tmp dir
            newFile = bot.getFile(update.message.document.file_id)
            file_uri = User.gpx_tmp_dir(update.message.document.file_name)
            newFile.download(file_uri)
            # adjust the fsm state
            if self._fsm.current != 'GPX_ACTIVITY':
                self._fsm.to_gpx_activity()
            # send a message and beging the data processing
            self._send_msg(bot, update, 'Message received, *we are working on it...*', keyboard=self._hide_custom_keyboard(), markdown=True)
            try:
                self._acty = GpxActivity(update.message.document.file_name)
                self._aattr = None
                self._send_msg(bot, update, msg="<b>NEW GPX ACTIVITY</b>\n\n{}\n\nChoose an option:".format(self._acty.current_state()), keyboard=self._gpx_activity_kb(), html=True)
            except Exception as e:
                self._send_msg(bot, update, "{}".format(e), keyboard=self._cancel_kb())



    def error_handler(self, bot, update, error):
        """
        Error handler callback method
        """
        logging.warning('Update "%s" caused error "%s"' % (update, error))
