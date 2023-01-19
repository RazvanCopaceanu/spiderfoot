# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_new_module
# Purpose:      SpiderFoot plug-in for creating new modules.
#
# Author:      Razvan Alexandru Copaceanu
# Based on the template: Daniel García Baameiro <dagaba13@gmail.com>
#
# Created:     18/01/2023
# Copyright:   (c) Razvan Alexandru Copaceanu 2023
# Licence:     GPL
# -------------------------------------------------------------------------------


from spiderfoot import SpiderFootEvent, SpiderFootPlugin
import json

class sfp_tendersguru(SpiderFootPlugin):

    meta = {
        'name': "Tenders Guru",
        'summary': "Allows to get data for procurements and tenders in Spain.",
        'flags': [""],
        'useCases': ["Investigate", "Passive"],
        'categories': ["Search Engines"],
        'dataSource': {
        	'website': "https://tenders.guru",
        	'model': "FREE_AUTH",
        	'references': [
        		"https://tenders.guru/es/api"
        	]
        }
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None
    errorState = False

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]


    def watchedEvents(self):
        return ["TENDERS_LIST"]
        
   
    def producedEvents(self):
        return ["COUNTRY_NAME"]

    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")

        try:
            data = None

            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")

            ########################
            # Insert here the code #
            ########################
            res = self.sf.fetchUrl('https://tenders.guru/es/api' + useragent=='SpiderFoot')
            if res['total'] != 0:
                data = res['total']
                return data
		
            if res['code'] != '200':
                self.error('Unexpected reply from tenders.guru: ' + res['code'])
                self.errorState = True
                return None
	
            try:
                return json.loads(res['content'])
            except Exception as e:
                self.debug(f"Error processing JSON response: {e}")

            if not data:
                self.sf.error("Unable to perform <ACTION MODULE> on " + eventData)
                return
        except Exception as e:
            self.sf.error("Unable to perform the <ACTION MODULE> on " + eventData + ": " + str(e))
            return

        typ = "COUNTRY_NAME"
        data = str(res)

        evt = SpiderFootEvent(typ, data, self.__name__, event)
        self.notifyListeners(evt)

# End of sfp_tendersguru class
