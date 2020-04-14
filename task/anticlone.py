#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils import logger

'''
This feature is not available in this version.
'''
def init(update, context, group, lang):
	try:
		#bot = context.bot
		pass
	except Exception as e:
		logger.exception(e)