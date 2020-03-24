#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
import Core
from Utils.daemon import Daemon
from Utils import logger
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.error import TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Create new daemon for UnifiedBan. 
'''
class UnifiedBanDaemon(Daemon):
  def error(update, context):
    logger.log.warning(lang.update_error, update, context.error)
  
  def run(self):
    try:
      pass
    except Exception as e:
      logger.log.exception(lang.unhandled)
    while True:
      updater = Updater(Params.telegram.Bot.token, use_context=True)
      dp = updater.dispatcher
      dp.add_error_handler(self.error)
      
      '''
      Test functions can be disabled in Params.settings.test_functions.
      '''
      if Params.settings.test_functions == True:
        dp.add_handler(CommandHandler("test", Core.test.message.init))
      
      
      '''
      User functions can be called by anyone.
      '''
      dp.add_handler(CommandHandler("start", Core.user.starter.init))
      dp.add_handler(CommandHandler("help", Core.user.helper.init))
      dp.add_handler(CommandHandler("rules", Core.user.rules.init))
      dp.add_handler(CommandHandler("report", Core.user.report.init))
      dp.add_handler(CommandHandler("setreport", Core.user.setreport.init))
      
      
      '''
      Admin functions can be called only by group admins and creator.
      '''
      dp.add_handler(CommandHandler("check", Core.admin.check.init))
      dp.add_handler(CommandHandler("rm", Core.admin.delete.init))
      dp.add_handler(CommandHandler("s", Core.admin.say.init))
      dp.add_handler(CommandHandler("feedback", Core.admin.feedback.init))
      dp.add_handler(CommandHandler("pin", Core.admin.pin.init))
      dp.add_handler(CommandHandler("ban", Core.admin.ban.init))
      dp.add_handler(CommandHandler("unban", Core.admin.ban.unban))
      dp.add_handler(CommandHandler("kick", Core.admin.kick.init))
      dp.add_handler(CommandHandler("limit", Core.admin.limit.init))
      dp.add_handler(CommandHandler("unlimit", Core.admin.limit.unlimit))
      dp.add_handler(CommandHandler("config", Core.admin.config.init))
      dp.add_handler(CommandHandler("setwelcome", Core.admin.setwelcome.init))
      dp.add_handler(CommandHandler("addwelcomebutton", Core.admin.setwelcome.addwelcomebutton))
      dp.add_handler(CommandHandler("removewelcomebutton", Core.admin.setwelcome.removewelcomebutton))
      dp.add_handler(CommandHandler("welcomebuttons", Core.admin.setwelcome.welcomebuttons))
      dp.add_handler(CommandHandler("setrules", Core.admin.setrules.init))
      dp.add_handler(CommandHandler("bad", Core.admin.bad.init))
      dp.add_handler(CommandHandler("unbad", Core.admin.bad.unbad))
      dp.add_handler(CommandHandler("badlist", Core.admin.bad.badlist))
      dp.add_handler(CommandHandler("safe", Core.admin.safe.init))
      dp.add_handler(CommandHandler("unsafe", Core.admin.safe.unsafe))
      dp.add_handler(CommandHandler("safelist", Core.admin.safe.safelist))
      dp.add_handler(CommandHandler("language", Core.admin.language.init))
      dp.add_handler(CommandHandler("setnote", Core.admin.setnote.init))
      dp.add_handler(CommandHandler("removenote", Core.admin.setnote.removenote))
      
      
      '''
      Privileged operator functions can be used by operators during maintenance.
      '''
      dp.add_handler(CommandHandler("status", Core.operator.status.init))
      dp.add_handler(CommandHandler("disable", Core.operator.disable.init))
      dp.add_handler(CommandHandler("white", Core.operator.white.init))
      
      '''
      Operator functions can be used by operators during maintenance.
      '''
      dp.add_handler(CommandHandler("startsupport", Core.operator.startsupport.init))
      dp.add_handler(CommandHandler("stopsupport", Core.operator.startsupport.stopsupport))
      dp.add_handler(CommandHandler("get", Core.operator.get.init))
      dp.add_handler(CommandHandler("register", Core.operator.register.init))
      dp.add_handler(CommandHandler("leave", Core.operator.leave.init))
      dp.add_handler(CommandHandler("sync", Core.operator.sync.init))
      dp.add_handler(CommandHandler("black", Core.operator.black.init))
      dp.add_handler(CommandHandler("bb", Core.operator.black.instant))
      dp.add_handler(CommandHandler("id", Core.operator.identity.init))
      
      
      '''
      Task functions are performed constantly.
      '''
      dp.add_handler(MessageHandler(None, Core.task.handler.init, edited_updates=True))
      
      
      '''
      Callback query handlers
      '''
      dp.add_handler(CallbackQueryHandler(Core.task.callback.init))

      updater.start_polling()
      updater.idle()