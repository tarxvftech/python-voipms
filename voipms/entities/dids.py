from voipms.baseapi import BaseApi

from voipms.helpers import convert_bool, validate_email, validate_date


class Dids(BaseApi):
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(Dids, self).__init__(*args, **kwargs)
        self.endoint = 'dids'

    def _order(self, **kwargs):

        parameters = {}
        
        international_fields = ("location_id", "quantity", "routing", "pop", "dialtime", "cnam")
        did_fields = ("did", "routing", "pop", "dialtime", "cnam", "billing_type")
        required_fields = {
            "backOrderDIDUSA": ("quantity", "state", "ratecenter", "routing", "pop", "dialtime", "cnam", "billing_type"),
            "backOrderDIDCAN": ("quantity", "province", "ratecenter", "routing", "pop", "dialtime", "cnam", "billing_type"),
            "orderDID": did_fields,
            "orderDIDInternationalGeographic": international_fields,
            "orderDIDInternationalNational": international_fields,
            "orderDIDInternationalTollFree": international_fields,
            "orderDIDVirtual": ("digits", "routing", "pop", "dialtime", "cnam", "billing_type"),
            "orderTollFree": did_fields,
            "orderVanity": ("did", "routing", "pop", "dialtime", "cnam", "billing_type", "carrier"),
        }

        # Minimize possibility of code injection
        if "method" in kwargs:
            if not isinstance(kwargs["method"], str):
                raise ValueError("method needs to be a str")
            else:
                if kwargs["method"] not in required_fields:
                    raise ValueError("This method is not allowed")
            method = kwargs.pop("method")
        else:
            raise ValueError("A method needs to be specified")

        if "did" in kwargs:
            if not isinstance(kwargs["did"], int):
                raise ValueError("DID to be Ordered needs to be an int (Example: 5552223333)")
            parameters["did"] = kwargs.pop("did")

        if "digits" in kwargs:
            if not isinstance(kwargs["digits"], int):
                raise ValueError("Three Digits for the new Virtual DID needs to be an int (Example: 001)")
            parameters["digits"] = kwargs.pop("digits")

        if "location_id" in kwargs:
            if not isinstance(kwargs["location_id"], int):
                raise ValueError("ID for a specific International Location needs to be an int (Values from dids.get_dids_international_geographic)")
            parameters["location_id"] = kwargs.pop("location_id")

        if "quantity" in kwargs:
            if not isinstance(kwargs["quantity"], int):
                raise ValueError("Number of dids to be purchased needs to be an int (Example: 2)")
            parameters["quantity"] = kwargs.pop("quantity")

        if "state" in kwargs:
            if not isinstance(kwargs["state"], str):
                raise ValueError("USA State needs to be a str (values from dids.get_states)")
            parameters["state"] = kwargs.pop("state")

        if "province" in kwargs:
            if not isinstance(kwargs["province"], str):
                raise ValueError("Canadian Province needs to be a str (values from dids.get_provinces)")
            parameters["province"] = kwargs.pop("province")

        if "ratecenter" in kwargs:
            if not isinstance(kwargs["ratecenter"], str):
                if method == "backOrderDIDUSA":
                    raise ValueError("USA Ratecenter needs to be a str (Values from dids.get_rate_centers_usa)")
                else:
                    raise ValueError("Canada Ratecenter needs to be a str (Values from dids.get_rate_centers_can)")
            parameters["ratecenter"] = kwargs.pop("ratecenter")

        if "routing" in kwargs:
            if not isinstance(kwargs["routing"], str):
                raise ValueError("Main Routing for the DID needs to be an int (Values from accounts.get_routes)")
            parameters["routing"] = kwargs.pop("routing")

        if "failover_busy" in kwargs:
            if not isinstance(kwargs["failover_busy"], str):
                raise ValueError("Busy Routing for the DID needs to be a str")
            parameters["failover_busy"] = kwargs.pop("failover_busy")

        if "failover_unreachable" in kwargs:
            if not isinstance(kwargs["failover_unreachable"], str):
                raise ValueError("Unreachable Routing for the DID needs to be a str")
            parameters["failover_unreachable"] = kwargs.pop("failover_unreachable")

        if "failover_noanswer" in kwargs:
            if not isinstance(kwargs["failover_noanswer"], str):
                raise ValueError("NoAnswer Routing for the DID")
            parameters["failover_noanswer"] = kwargs.pop("failover_noanswer")

        if "voicemail" in kwargs:
            if not isinstance(kwargs["voicemail"], int):
                raise ValueError("Voicemail for the DID needs to be an int (Example: 101)")
            parameters["voicemail"] = kwargs.pop("voicemail")

        if "pop" in kwargs:
            if not isinstance(kwargs["pop"], int):
                raise ValueError("Point of pop for the DID needs to be an int (Example: 5)")
            parameters["pop"] = kwargs.pop("pop")

        if "dialtime" in kwargs:
            if not isinstance(kwargs["dialtime"], int):
                raise ValueError("Dial Time Out for the DID needs to be an int (Example: 60 -> in seconds)")
            parameters["dialtime"] = kwargs.pop("dialtime")

        if "cnam" in kwargs:
            if not isinstance(kwargs["cnam"], bool):
                raise ValueError("CNAM for the DID needs to be a bool (Boolean: True/False)")
            parameters["cnam"] = convert_bool(kwargs.pop("cnam"))

        if "carrier" in kwargs:
            if not isinstance(kwargs["carrier"], int):
                raise ValueError("Carrier for the DID needs to be a bool (Values from dids.get_carriers)")
            parameters["carrier"] = convert_bool(kwargs.pop("carrier"))

        if "callerid_prefix" in kwargs:
            if not isinstance(kwargs["callerid_prefix"], str):
                raise ValueError("Caller ID Prefix for the DID needs to be a str")
            parameters["callerid_prefix"] = kwargs.pop("callerid_prefix")

        if "note" in kwargs:
            if not isinstance(kwargs["note"], str):
                raise ValueError("Note for the DID needs to be a str")
            parameters["note"] = kwargs.pop("note")

        if "billing_type" in kwargs:
            if not isinstance(kwargs["billing_type"], int):
                raise ValueError("Billing type for the DID needs to be an int (1 = Per Minute, 2 = Flat)")
            parameters["billing_type"] = kwargs.pop("billing_type")

        if "account" in kwargs:
            if not isinstance(kwargs["account"], str):
                raise ValueError("Reseller Sub Account needs to be a str (Example: '100001_VoIP')")
            parameters["account"] = kwargs.pop("account")

        if "monthly" in kwargs:
            if not isinstance(kwargs["monthly"], float):
                raise ValueError("Montly Fee for Reseller Client needs to be a float (Example: 3.50)")
            parameters["monthly"] = kwargs.pop("monthly")

        if "setup" in kwargs:
            if not isinstance(kwargs["setup"], float):
                raise ValueError("Setup Fee for Reseller Client needs to be a float (Example: 1.99)")
            parameters["setup"] = kwargs.pop("setup")

        if "minute" in kwargs:
            if not isinstance(kwargs["minute"], float):
                raise ValueError("Minute Rate for Reseller Client needs to be a float (Example: 0.03)")
            parameters["minute"] = kwargs.pop("minute")

        if "test" in kwargs:
            if not isinstance(kwargs["test"], bool):
                raise ValueError("Test needs to be a bool (True/False)")
            parameters["test"] = convert_bool(kwargs.pop("test"))

        if len(kwargs) > 0:
            not_allowed_parameters = ""
            for key, value in kwargs.items():
                not_allowed_parameters += key + " "
            raise ValueError("Parameters not allowed: {}".format(not_allowed_parameters))

        # Verify again if all required fields present
        for field in required_fields[method]:
            if field not in parameters:
                raise ValueError("The parameter {} is required".format(field))

        return self._voipms_client._get(method, parameters)

    def back_order_did_can(self, quantity, province, ratecenter, routing, pop, dialtime, cnam, billing_type, **kwargs):
        """
        Backorder DID (USA) from a specific ratecenter and state

        :param quantity: [Required] Number of DIDs to be Ordered (Example: 3)
        :type quantity: :py:class:`int`
        :param province: [Required] Canadian Province  (values from dids.get_provinces)
        :type province: :py:class:`str`
        :param ratecenter: [Required] Canadian Ratecenter (Values from dids.get_rate_centers_can)
        :type ratecenter: :py:class:`str`
        :param routing: [Required] Main Routing for the DID
        :type routing: :py:class:`str`
        :param pop: [Required] Point of Presence for the DID (Example: 5)
        :type pop: :py:class:`int`
        :param dialtime: [Required] Dial Time Out for the DID (Example: 60 -> in seconds)
        :type dialtime: :py:class:`int`
        :param cnam: [Required] CNAM for the DID (Boolean: True/False)
        :type cnam: :py:class:`bool`
        :param billing_type: [Required] Billing type for the DID (1 = Per Minute, 2 = Flat)
        :type billing_type: :py:class:`int`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param failover_busy: Busy Routing for the DID
        :type failover_busy: :py:class:`str`
        :param failover_unreachable: Unreachable Routing for the DID
        :type failover_unreachable: :py:class:`str`
        :param failover_noanswer: NoAnswer Routing for the DID
        :type failover_noanswer: :py:class:`str`
        :param voicemail: Voicemail for the DID (Example: 101)
        :type voicemail: :py:class:`int`
        :param callerid_prefix: Caller ID Prefix for the DID
        :type callerid_prefix: :py:class:`str`
        :param note: Note for the DID
        :type note: :py:class:`str`
        :param test: Set to True if testing how Orders work
                        - Orders can not be undone
                        - When testing, no Orders are made
        :type test: :py:class:`bool`

        :returns: :py:class:`dict`

        routing, failover_busy, failover_unreachable and failover_noanswer
        can receive values in the following format => header:record_id
        Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.
        Examples:

            account     Used for routing calls to Sub Accounts
                        You can get all sub accounts using the getSubAccounts function

            fwd         Used for routing calls to Forwarding entries.
                        You can get the ID right after creating a Forwarding with setForwarding
                        or by requesting all forwardings entries with getForwardings.

            vm          Used for routing calls to a Voicemail.
                        You can get all voicemails and their IDs using the getVoicemails function

            sys         System Options:
                        hangup       = Hangup the Call
                        busy         = Busy tone
                        noservice    = System Recording: Number not in service
                        disconnected = System Recording: Number has been disconnected
                        dtmf         = DTMF Test
                        echo         = ECHO Test


            none        Used to route calls to no action

        Examples:
            'account:100001_VoIP'
            'fwd:1026'
            'vm:101'
            'none:'
            'sys:echo'
        """
        method = "backOrderDIDCAN"

        kwargs.update({
            "method": method,
            "quantity": quantity,
            "province": province,
            "ratecenter": ratecenter,
            "routing": routing,
            "pop": pop,
            "dialtime": dialtime,
            "cnam": cnam,
            "billing_type": billing_type,
        })

        return self._order(**kwargs)

    def back_order_did_usa(self, quantity, state, ratecenter, routing, pop, dialtime, cnam, billing_type, **kwargs):
        """
        Backorder DID (USA) from a specific ratecenter and state

        :param quantity: [Required] Number of DIDs to be Ordered (Example: 3)
        :type quantity: :py:class:`int`
        :param state: [Required] USA State (values from dids.get_states)
        :type state: :py:class:`str`
        :param ratecenter: [Required] USA Ratecenter (Values from dids.get_rate_centers_usa)
        :type ratecenter: :py:class:`str`
        :param routing: [Required] Main Routing for the DID
        :type routing: :py:class:`str`
        :param pop: [Required] Point of Presence for the DID (Example: 5)
        :type pop: :py:class:`int`
        :param dialtime: [Required] Dial Time Out for the DID (Example: 60 -> in seconds)
        :type dialtime: :py:class:`int`
        :param cnam: [Required] CNAM for the DID (Boolean: True/False)
        :type cnam: :py:class:`bool`
        :param billing_type: [Required] Billing type for the DID (1 = Per Minute, 2 = Flat)
        :type billing_type: :py:class:`int`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param failover_busy: Busy Routing for the DID
        :type failover_busy: :py:class:`str`
        :param failover_unreachable: Unreachable Routing for the DID
        :type failover_unreachable: :py:class:`str`
        :param failover_noanswer: NoAnswer Routing for the DID
        :type failover_noanswer: :py:class:`str`
        :param voicemail: Voicemail for the DID (Example: 101)
        :type voicemail: :py:class:`int`
        :param callerid_prefix: Caller ID Prefix for the DID
        :type callerid_prefix: :py:class:`str`
        :param note: Note for the DID
        :type note: :py:class:`str`
        :param test: Set to True if testing how Orders work
                        - Orders can not be undone
                        - When testing, no Orders are made
        :type test: :py:class:`bool`

        :returns: :py:class:`dict`

        routing, failover_busy, failover_unreachable and failover_noanswer
        can receive values in the following format => header:record_id
        Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.
        Examples:

            account     Used for routing calls to Sub Accounts
                        You can get all sub accounts using the getSubAccounts function

            fwd         Used for routing calls to Forwarding entries.
                        You can get the ID right after creating a Forwarding with setForwarding
                        or by requesting all forwardings entries with getForwardings.

            vm          Used for routing calls to a Voicemail.
                        You can get all voicemails and their IDs using the getVoicemails function

            sys         System Options:
                        hangup       = Hangup the Call
                        busy         = Busy tone
                        noservice    = System Recording: Number not in service
                        disconnected = System Recording: Number has been disconnected
                        dtmf         = DTMF Test
                        echo         = ECHO Test


            none        Used to route calls to no action

        Examples:
            'account:100001_VoIP'
            'fwd:1026'
            'vm:101'
            'none:'
            'sys:echo'
        """
        method = "backOrderDIDUSA"

        kwargs.update({
            "method": method,
            "quantity": quantity,
            "state": state,
            "ratecenter": ratecenter,
            "routing": routing,
            "pop": pop,
            "dialtime": dialtime,
            "cnam": cnam,
            "billing_type": billing_type,
        })

        return self._order(**kwargs)

    def cancel_did(self, did, **kwargs):
        """
        Deletes a specific DID from your Account

        :param did: [Required] DID to be canceled and deleted (Example: 5551234567)
        :type did: :py:class:`str` or `int`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param cancelcomment: Comment for DID cancellation
        :type cancelcomment: :py:class:`str`
        :param portout: Set to True if the DID is being ported out
        :type portout: :py:class:`bool`
        :param test: Set to True if testing how cancellation works
                                - Cancellation can not be undone
                                - When testing, no changes are made
        :type test: :py:class:`bool`

        :returns: :py:class:`dict`

        routing, failover_busy, failover_unreachable and failover_noanswer
        can receive values in the following format => header:record_id
        Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.
        Examples:

            account     Used for routing calls to Sub Accounts
                        You can get all sub accounts using the getSubAccounts function

            fwd         Used for routing calls to Forwarding entries.
                        You can get the ID right after creating a Forwarding with setForwarding
                        or by requesting all forwardings entries with getForwardings.
            
            vm          Used for routing calls to a Voicemail.
                        You can get all voicemails and their IDs using the getVoicemails function

            sys         System Options:
                        hangup       = Hangup the Call
                        busy         = Busy tone
                        noservice    = System Recording: Number not in service
                        disconnected = System Recording: Number has been disconnected
                        dtmf         = DTMF Test
                        echo         = ECHO Test


            none        Used to route calls to no action

        Examples:
            'account:100001_VoIP'
            'fwd:1026'
            'vm:101'
            'none:'
            'sys:echo'
        """
        method = "cancelDID"

        if isinstance(did, str):
            did = did.replace('.', '')
            try:
                did = int(did)
            except:
                raise ValueError("DID to be canceled and deleted needs to be an int or str of numbers (Example: 555.123.4567 or 5551234567)")
        if not isinstance(did, int):
            raise ValueError("DID to be canceled and deleted needs to be an int (Example: 5551234567)")
        parameters = {
            "did": did
        }

        if "portout" in kwargs:
            if not isinstance(kwargs["portout"], bool):
                raise ValueError("Set to True if the DID is being ported out")
            parameters["portout"] = convert_bool(kwargs.pop("portout"))

        if "test" in kwargs:
            if not isinstance(kwargs["test"], bool):
                raise ValueError("Set to True if testing how cancellation works")
            parameters["test"] = convert_bool(kwargs.pop("test"))

        if len(kwargs) > 0:
            not_allowed_parameters = ""
            for key, value in kwargs.items():
                not_allowed_parameters += key + " "
            raise ValueError("Parameters not allowed: {}".format(not_allowed_parameters))

        return self._voipms_client._get(method, parameters)

    def connect_did(self, did, account, monthly, setup, minute, **kwargs):
        """
        Connects a specific DID to a specific Reseller Client Sub Account

        :param did: [Required] DID to be canceled and deleted (Example: 5551234567)
        :type did: :py:class:`str` or `int`
        :param account: [Required] Reseller Sub Account (Example: '100001_VoIP')
        :type account: :py:class:`str`
        :param monthly: [Required] Montly Fee for Reseller Client (Example: 3.50)
        :type monthly: :py:class:`float`
        :param setup: [Required] Setup Fee for Reseller Client (Example: 1.99)
        :type setup: :py:class:`float`
        :param minute: [Required] Minute Rate for Reseller Client (Example: 0.03)
        :type minute: :py:class:`float`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param next_billing: Next billing date (Example: '2014-03-30')
        :type next_billing: :py:class:`str`
        :param dont_charge_setup: If set to true, the setup value will not be charged after Connect
        :type dont_charge_setup: :py:class:`bool`
        :param dont_charge_monthly: If set to true, the monthly value will not be charged after Connect
        :type dont_charge_monthly: :py:class:`bool`

        :returns: :py:class:`dict`
        """
        method = "connectDID"

        if isinstance(did, str):
            did = did.replace('.', '')
            try:
                did = int(did)
            except:
                raise ValueError("DID to be canceled and deleted needs to be an int or str of numbers (Example: 555.123.4567 or 5551234567)")
        if not isinstance(did, int):
            raise ValueError("DID to be canceled and deleted needs to be an int (Example: 5551234567)")

        if not isinstance(account, str):
            raise ValueError("Reseller Sub Account needs to be a str (Example: '100001_VoIP')")

        if not isinstance(monthly, float):
            raise ValueError("Montly Fee for Reseller Client needs to be a float (Example: 3.50)")

        if not isinstance(setup, float):
            raise ValueError("Setup Fee for Reseller Client needs to be a float (Example: 1.99)")

        if not isinstance(minute, float):
            raise ValueError("Minute Rate for Reseller Client needs to be a float (Example: 0.03)")

        parameters = {
            "did": did,
            "account": account,
            "monthly": monthly,
            "setup": setup,
            "minute": minute,
        }

        if "next_billing" in kwargs:
            next_billing = kwargs.pop("next_billing")
            if not isinstance(next_billing, str):
                raise ValueError("Next billing date needs to be a str (Example: '2014-03-30')")
            validate_date(next_billing)
            parameters["next_billing"] = next_billing

        if "dont_charge_setup" in kwargs:
            if not isinstance(kwargs["dont_charge_setup"], bool):
                raise ValueError("If set to True, the setup value will not be charged after Connect (needs to be bool)")
            parameters["dont_charge_setup"] = convert_bool(kwargs.pop("dont_charge_setup"))

        if "dont_charge_monthly" in kwargs:
            if not isinstance(kwargs["dont_charge_monthly"], bool):
                raise ValueError("If set to True, the monthly value will not be charged after Connect (needs to be bool)")
            parameters["dont_charge_monthly"] = convert_bool(kwargs.pop("dont_charge_monthly"))

        if len(kwargs) > 0:
            not_allowed_parameters = ""
            for key, value in kwargs.items():
                not_allowed_parameters += key + " "
            raise ValueError("Parameters not allowed: {}".format(not_allowed_parameters))

        return self._voipms_client._get(method, parameters)

    def del_callback(self, callback):
        """
        Deletes a specific Callback from your Account

        :param callback: [Required] ID for a specific Callback (Example: 19183)
        :type callback: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delCallback"

        if not isinstance(callback, int):
            raise ValueError("ID for a specific Callback needs to be an int (Example: 19183)")
        parameters = {
            "callback": callback
        }

        return self._voipms_client._get(method, parameters)

    def del_caller_id_filtering(self, filtering):
        """
        Deletes a specific CallerID Filtering from your Account

        :param filtering: [Required] ID for a specific CallerID Filtering (Example: 19183)
        :type filtering: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delCallerIDFiltering"

        if not isinstance(filtering, str):
            raise ValueError("ID for a specific CallerID Filtering needs to be an int (Example: 19183)")
        parameters = {
            "filtering": filtering
        }

        return self._voipms_client._get(method, parameters)

    def del_client(self, client):
        """
        Deletes a specific reseller client from your Account

        :param client: [Required] ID for a specific Reseller Client (Example: 1998)
        :type client: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delClient"

        if not isinstance(client, int):
            raise ValueError("ID for a specific Reseller Client needs to be an int (Example: 1998)")
        parameters = {
            "client": client
        }

        return self._voipms_client._get(method, parameters)

    def del_disa(self, disa):
        """
        Deletes a specific DISA from your Account

        :param disa: [Required] ID for a specific DISA (Example: 19183)
        :type disa: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delDISA"

        if not isinstance(disa, int):
            raise ValueError("ID for a specific DISA needs to be an int (Example: 19183)")
        parameters = {
            "disa": disa
        }

        return self._voipms_client._get(method, parameters)

    def delete_sms(self, sms_id):
        """
        Deletes a specific SMS from your Account

        :param sms_id: [Required] ID for a specific SMS (Example: 1918)
        :type sms_id: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "deleteSMS"

        if not isinstance(sms_id, int):
            raise ValueError("ID for a specific SMS needs to be an int (Example: 1918)")
        parameters = {
            "id": sms_id
        }

        return self._voipms_client._get(method, parameters)

    def del_forwarding(self, forwarding):
        """
        Deletes a specific Forwarding from your Account

        :param forwarding: [Required] ID for a specific Forwarding (Example: 19183)
        :type forwarding: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delForwarding"

        if not isinstance(forwarding, int):
            raise ValueError("ID for a specific Forwarding needs to be an int (Example: 19183)")
        parameters = {
            "forwarding": forwarding
        }

        return self._voipms_client._get(method, parameters)

    def del_ivr(self, ivr):
        """
        Deletes a specific IVR from your Account

        :param ivr: [Required] ID for a specific IVR (Example: 19183)
        :type ivr: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delIVR"

        if not isinstance(ivr, int):
            raise ValueError("ID for a specific IVR needs to be an int (Example: 19183)")
        parameters = {
            "ivr": ivr
        }

        return self._voipms_client._get(method, parameters)

    def del_phonebook(self, phonebook):
        """
        Deletes a specific Phonebook from your Account

        :param phonebook: [Required] ID for a specific Phonebook (Example: 19183)
        :type phonebook: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delPhonebook"

        if not isinstance(phonebook, int):
            raise ValueError("ID for a specific Phonebook needs to be an int (Example: 19183)")
        parameters = {
            "phonebook": phonebook
        }

        return self._voipms_client._get(method, parameters)

    def del_queue(self, queue):
        """
        Deletes a specific Queue from your Account

        :param queue: [Required] ID for a specific Queue (Example: 13183)
        :type queue: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delQueue"

        if not isinstance(queue, int):
            raise ValueError("ID for a specific Queue needs to be an int (Example: 13183)")
        parameters = {
            "queue": queue
        }

        return self._voipms_client._get(method, parameters)

    def del_recording(self, recording):
        """
        Deletes a specific Recording from your Account

        :param recording: [Required] ID for a specific Recording (Example: 19183)
        :type recording: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delRecording"

        if not isinstance(recording, int):
            raise ValueError("ID for a specific Recording needs to be an int (Example: 19183)")
        parameters = {
            "recording": recording
        }

        return self._voipms_client._get(method, parameters)

    def del_ring_group(self, ringgroup):
        """
        Deletes a specific Ring Group from your Account

        :param ringgroup: [Required] ID for a specific Ring Group (Example: 19183)
        :type ringgroup: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delRingGroup"

        if not isinstance(ringgroup, int):
            raise ValueError("ID for a specific Ring Group needs to be an int (Example: 19183)")
        parameters = {
            "ringgroup": ringgroup
        }

        return self._voipms_client._get(method, parameters)

    def del_sip_uri(self, sipuri):
        """
        Deletes a specific SIP URI from your Account

        :param sipuri: [Required] ID for a specific SIP URI (Example: 19183)
        :type sipuri: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delSIPURI"

        if not isinstance(sipuri, int):
            raise ValueError("ID for a specific SIP URI needs to be an int (Example: 19183)")
        parameters = {
            "sipuri": sipuri
        }

        return self._voipms_client._get(method, parameters)

    def del_static_member(self, member, queue):
        """
        Deletes a specific Static Member from Queue

        :param member: [Required] ID for a specific Member Queue (Example: 1918)
        :type member: :py:class:`int`
        :param queue: [Required] ID for a specific Queue (Example: 27183)
        :type queue: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delStaticMember"

        if not isinstance(member, int):
            raise ValueError("ID for a specific Member Queue needs to be an int (Example: 19183)")

        if not isinstance(queue, int):
            raise ValueError("ID for a specific Queue needs to be an int (Example: 19183)")

        parameters = {
            "member": member,
            "queue": queue,
        }

        return self._voipms_client._get(method, parameters)

    def del_time_condition(self, timecondition):
        """
        Deletes a specific Time Condition from your Account

        :param timecondition: [Required] ID for a specific Time Condition (Example: 19183)
        :type timecondition: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "delTimeCondition"

        if not isinstance(timecondition, int):
            raise ValueError("ID for a specific Time Condition needs to be an int (Example: 19183)")
        parameters = {
            "timecondition": timecondition
        }

        return self._voipms_client._get(method, parameters)

    def get_callbacks(self, callback=None):
        """
        Retrieves a list of Callbacks if no additional parameter is provided

        - Retrieves a specific Callback if a Callback code is provided

        :param callback: ID for a specific Callback (Example: 2359)
        :type callback: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getCallbacks"

        parameters = {}
        if callback:
            if not isinstance(callback, int):
                raise ValueError("ID for a specific Callback needs to be an int (Example: 2359)")
            parameters["callback"] = callback

        return self._voipms_client._get(method, parameters)

    def get_caller_id_filtering(self, filtering=None):
        """
        Retrieves a list of CallerID Filterings if no additional parameter is provided

        - Retrieves a specific CallerID Filtering if a CallerID Filtering code is provided

        :param filtering: ID for a specific CallerID Filtering (Example: 18915)
        :type filtering: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getCallerIDFiltering"

        parameters = {}
        if filtering:
            if not isinstance(filtering, int):
                raise ValueError("ID for a specific CallerID Filtering needs to be an int (Example: 18915)")
            parameters["filtering"] = filtering

        return self._voipms_client._get(method, parameters)

    def get_did_countries(self, international_type, country_id=None):
        """
        Retrieves a list of Countries for International DIDs if no country code is provided

        - Retrieves a specific Country for International DIDs if a country code is provided

        :param international_type: [Required] Type of International DID (Values from dids.get_international_types)
        :type international_type: :py:class:`str`

        :param country_id: ID for a specific country (Example: 205)
        :type country_id: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getDIDCountries"

        if not isinstance(international_type, str):
            raise ValueError("Type of International DID needs to be a str (Values from dids.get_international_types)")
        parameters = {
            "type": international_type
        }

        if country_id:
            if not isinstance(country_id, int):
                raise ValueError("ID for a specific country needs to be an int (Example: 205)")
            parameters["country_id"] = country_id

        return self._voipms_client._get(method, parameters)

    def get_carriers(self, carrier=None):
        """
        Retrieves a list of Carriers for Vanity Numbers if no additional parameter is provided

        - Retrieves a specific Carrier for Vanity Numbers if a carrier code is provided

        :param carrier: Code for a specific Carrier (Example: 2)
        :type carrier: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getCarriers"

        parameters = {}
        if carrier:
            if not isinstance(carrier, int):
                raise ValueError("ID for a specific CallerID Filtering needs to be an int (Example: 18915)")
            parameters["carrier"] = carrier

        return self._voipms_client._get(method, parameters)

    def get_dids_can(self, province, ratecenter=None):
        """
        Retrives a list of Canadian DIDs by Province and Ratecenter

        :param province: [Required] Canadian Province (Values from dids.get_provinces)
        :type province: :py:class:`str`

        :param ratecenter: Canadian Ratecenter (Values from dids.get_rate_centers_can)
        :type ratecenter: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "getDIDsCAN"

        if not isinstance(province, str):
            raise ValueError("Canadian Province needs to be a str (Values from dids.get_provinces)")
        parameters = {
            "province": province
        }

        if ratecenter:
            if not isinstance(ratecenter, str):
                raise ValueError("Canadian Ratecenter needs to be a str (Values from dids.get_rate_centers_can)")
            else:
                parameters["ratecenter"] = ratecenter

        return self._voipms_client._get(method, parameters)

    def get_dids_info(self, client=None, did=None):
        """
        Retrieves information from all your DIDs if no additional parameter is provided

        - Retrieves information from Reseller Client's DIDs if a Reseller Client ID is provided.
        - Retrieves information from Sub Account's DIDs if a Sub Accunt is provided.
        - Retrieves information from a specific DID if a DID Number is provided.
        - Retrieves SMS information from a specific DID if the SMS is available.

        :param client: Parameter could have the following values
                            - Empty Value [Not Required]
                            - Specific Reseller Client ID (Example: 561115)
                            - Specific Sub Account (Example: '100001_VoIP')
        :type client: :py:class:`str`
        :param did: DID from Client or Sub Account (Example: 5551234567)
        :type did: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "getDIDsInfo"

        parameters = {}

        if client:
            if not isinstance(client, str):
                raise ValueError("Parameter needs to be Empty Value [Not Required], Specific Reseller Client ID (Example: 561115) or Specific Sub Account (Example: '100001_VoIP'). The value needs to be a str.")
            else:
                parameters["client"] = client

        if did:
            if not isinstance(did, int):
                raise ValueError("DID from Client or Sub Account needs to be an int (Example: 5551234567)")
            else:
                parameters["did"] = did

        return self._voipms_client._get(method, parameters)

    def get_dids_international_geographic(self, country_id):
        """
        Retrieves a list of International Geographic DIDs by Country

        :param country_id: [Required] ID for a specific Country (Values from dids.get_did_countries)
        :type country_id: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "getDIDsInternationalGeographic"

        if not isinstance(country_id, int):
            raise ValueError("ID for a specific Country needs to be an int (Values from dids.get_did_countries)")
        parameters = {
            "country_id": country_id
        }

        return self._voipms_client._get(method, parameters)

    def get_dids_international_national(self, country_id):
        """
        Retrieves a list of International National DIDs by Country

        :param country_id: [Required] ID for a specific Country (Values from dids.get_did_countries)
        :type country_id: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "getDIDsInternationalNational"

        if not isinstance(country_id, int):
            raise ValueError("ID for a specific Country needs to be an int (Values from dids.get_did_countries)")
        parameters = {
            "country_id": country_id
        }

        return self._voipms_client._get(method, parameters)

    def get_dids_international_toll_free(self, country_id):
        """
        Retrieves a list of International TollFree DIDs by Country

        :param country_id: [Required] ID for a specific Country (Values from dids.get_did_countries)
        :type country_id: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "getDIDsInternationalTollFree"

        if not isinstance(country_id, int):
            raise ValueError("ID for a specific Country needs to be an int (Values from dids.get_did_countries)")
        parameters = {
            "country_id": country_id
        }

        return self._voipms_client._get(method, parameters)

    def get_dids_usa(self, state, ratecenter=None):
        """
        Retrives a list of USA DIDs by State and Ratecenter

        :param state: [Required] United States State (Values from dids.get_states)
        :type state: :py:class:`str`

        :param ratecenter: United States Ratecenter (Values from dids.get_rate_centers_usa)
        :type ratecenter: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "getDIDsUSA"

        if not isinstance(state, str):
            raise ValueError("United States State needs to be a str (Values from dids.get_states)")
        parameters = {
            "state": state
        }

        if ratecenter:
            if not isinstance(ratecenter, str):
                raise ValueError("United States Ratecenter (Values from dids.get_rate_centers_usa)")
            else:
                parameters["ratecenter"] = ratecenter

        return self._voipms_client._get(method, parameters)

    def get_disas(self, disa=None):
        """
        Retrieves a list of DISAs if no additional parameter is provided

        - Retrieves a specific DISA if a DISA code is provided

        :param disa: ID for a specific DISA (Example: 2114)
        :type disa: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getDISAs"

        parameters = {}
        if disa:
            if not isinstance(disa, int):
                raise ValueError("ID for a specific DISA needs to be an int (Example: 2114)")
            parameters["disa"] = disa

        return self._voipms_client._get(method, parameters)

    def get_forwardings(self, forwarding=None):
        """
        Retrieves a list of Forwardings if no additional parameter is provided

        - Retrieves a specific Forwarding if a fwd code is provided

        :param forwarding: ID for a specific Forwarding (Example: 18635)
        :type forwarding: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getForwardings"

        parameters = {}
        if forwarding:
            if not isinstance(forwarding, int):
                raise ValueError("ID for a specific Forwarding needs to be an int (Example: 18635)")
            parameters["forwarding"] = forwarding

        return self._voipms_client._get(method, parameters)

    def get_international_types(self, international_type=None):
        """
        Retrieves a list of Types for International DIDs if no additional parameter is provided

        - Retrieves a specific Types for International DIDs if a type code is provided

        :param international_type: Code for a specific International Type (Example: 'NATIONAL')
        :type international_type: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "getInternationalTypes"

        parameters = {}
        if international_type:
            if not isinstance(international_type, str):
                raise ValueError("Code for a specific International Type needs to be a str (Example: 'NATIONAL')")
            parameters["type"] = international_type

        return self._voipms_client._get(method, parameters)

    def get_ivrs(self, ivr=None):
        """
        Retrieves a list of IVRs if no additional parameter is provided

        - Retrieves a specific IVR if a IVR code is provided

        :param ivr: ID for a specific IVR (Example: 4636)
        :type ivr: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getIVRs"

        parameters = {}
        if ivr:
            if not isinstance(ivr, int):
                raise ValueError("ID for a specific IVR needs to be an int (Example: 4636)")
            parameters["ivr"] = ivr

        return self._voipms_client._get(method, parameters)

    def get_join_when_empty_types(self, join_type=None):
        """
        Retrieves a list of 'JoinWhenEmpty' Types if no additional parameter is provided

        - Retrieves a specific 'JoinWhenEmpty' Types if a type code is provided

        :param join_type: Code for a specific 'JoinWhenEmpty' Type (Example: 'yes')
        :type join_type: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "getJoinWhenEmptyTypes"

        parameters = {}
        if join_type:
            if not isinstance(join_type, int):
                raise ValueError("Code for a specific 'JoinWhenEmpty' Type needs to be a str (Example: 'yes')")
            parameters["type"] = join_type

        return self._voipms_client._get(method, parameters)

    def get_phonebook(self, phonebook=None, name=None):
        """
        Retrieves a list of Phonebook entries if no additional parameter is provided

        - Retrieves a list of Phonebook entries if a name is provided.
        - Retrieves a specific Phonebook entry if a Phonebook code is provided.

        :param phonebook: ID for a specific Phonebook entry (Example: 32207)
        :type phonebook: :py:class:`int`
        :param name: Name to be searched in database (Example: 'jane')
        :type name: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "getPhonebook"

        parameters = {}

        if phonebook:
            if not isinstance(phonebook, int):
                raise ValueError("ID for a specific Phonebook entry needs to an int (Example: 32207)")
            else:
                parameters["phonebook"] = phonebook

        if name:
            if not isinstance(name, str):
                raise ValueError("Name to be searched in database needs to be a str (Example: 'jane')")
            else:
                parameters["name"] = name

        return self._voipms_client._get(method, parameters)

    def get_portability(self, did):
        """
        Shows if a DID Number can be ported into our network

        - Display plans and rates available if the DID Number can be ported into our network.

        :param did: [Required] DID Number to be ported into our network (Example: 5552341234)
        :type did: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getPortability"

        if not isinstance(did, int):
            raise ValueError("DID Number to be ported into our network needs to be an int (Example: 5552341234)")
        parameters = {
            "DID": did
        }

        return self._voipms_client._get(method, parameters)

    def get_provinces(self):
        """
        Retrieves a list of Canadian Provinces

        :returns: :py:class:`dict`
        """
        method = "getProvinces"

        return self._voipms_client._get(method)

    def get_queues(self, queue=None):
        """
        Retrieves a list of Queue entries if no additional parameter is provided

        - Retrieves a specific Queue entry if a Queue code is provided.

        :param queue: ID for a specific Queue (Example: 4764)
        :type queue: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getQueues"

        parameters = {}
        if queue:
            if not isinstance(queue, int):
                raise ValueError("ID for a specific Queue needs to be an int (Example: 4764)")
            parameters["queue"] = queue

        return self._voipms_client._get(method, parameters)

    def get_rate_centers_can(self, province):
        """
        Retrieves a list of Canadian Ratecenters by Province

        :param province: [Required] Canadian Province (Values from dids.get_provinces)
        :type province: :py:class:`str`
        :returns: :py:class:`dict`
        """
        method = "getRateCentersCAN"

        parameters = {}
        if province:
            if not isinstance(province, str):
                raise ValueError("Canadian Province needs to be a str (Values from dids.get_provinces)")
            parameters["province"] = province

        return self._voipms_client._get(method, parameters)

    def get_rate_centers_usa(self, state):
        """
        Retrieves a list of USA Ratecenters by State

        :param state: [Required] United States State (Values from dids.get_states)
        :type state: :py:class:`str`
        :returns: :py:class:`dict`
        """
        method = "getRateCentersUSA"

        parameters = {}
        if state:
            if not isinstance(state, str):
                raise ValueError("United States State needs to be a str (Values from dids.get_states)")
            parameters["state"] = state

        return self._voipms_client._get(method, parameters)

    def get_states(self):
        """
        Retrieves a list of USA States

        :returns: :py:class:`dict`
        """
        method = "getStates"

        return self._voipms_client._get(method)

    def get_static_members(self, queue, member=None):
        """
        Retrieves a list of Static Members from a queue if no additional parameter is provided

        - Retrieves a specific Static Member from a queue if Queue ID and Member ID are provided

        :param state: [Required] ID for a specific Queue (Example: 4136)
        :type state: :py:class:`int`

        :param ratecenter: ID for a specific Static Member (Example: 163)
                            - The Member must belong to the queue provided
        :type ratecenter: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getStaticMembers"

        if not isinstance(queue, int):
            raise ValueError("ID for a specific Queue needs to be an int (Example: 4136)")
        parameters = {
            "queue": queue
        }

        if member:
            if not isinstance(member, str):
                raise ValueError("ID for a specific Static Member needs to be an int (Example: 163) and Member must belong to the queue provided")
            else:
                parameters["member"] = member

        return self._voipms_client._get(method, parameters)

    def get_time_conditions(self, timecondition=None):
        """
        Retrieves a list of Time Conditions if no additional parameter is provided

        - Retrieves a specific Time Condition if a time condition code is provided.

        :param timecondition: ID for a specific Time Condition (Example: 1830)
        :type timecondition: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getTimeConditions"

        parameters = {}
        if timecondition:
            if not isinstance(timecondition, int):
                raise ValueError("ID for a specific Time Condition needs to be an int (Example: 1830)")
            parameters["timecondition"] = timecondition

        return self._voipms_client._get(method, parameters)

    def get_voicemail_setups(self, voicemailsetup=None):
        """
        Retrieves a list of Voicemail Setup Options if no additional parameter is provided

        - Retrieves a specific Voicemail Setup Option if a voicemail setup code is provided.

        :param voicemailsetup: ID for a specific Voicemail Setup (Example: 2)
        :type voicemailsetup: :py:class:`int`

        :returns: :py:class:`dict`
        """
        method = "getVoicemailSetups"

        parameters = {}
        if voicemailsetup:
            if not isinstance(voicemailsetup, int):
                raise ValueError("ID for a specific Voicemail Setup needs to be an int (Example: 2)")
            parameters["voicemailsetup"] = voicemailsetup

        return self._voipms_client._get(method, parameters)

    def get_voicemail_attachment_formats(self, email_attachment_format=None):
        """
        Retrieves a list of Email Attachment Format Options if no additional parameter is provided

        - Retrieves a specific Email Attachment Format Option if a format value is provided.

        :param email_attachment_format: ID for a specific attachment format (Example: wav49)
        :type email_attachment_format: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "getVoicemailAttachmentFormats"

        parameters = {}
        if email_attachment_format:
            if not isinstance(email_attachment_format, str):
                raise ValueError("ID for a specific Voicemail Setup needs to be an int (Example: 2)")
            parameters["email_attachment_format"] = email_attachment_format

        return self._voipms_client._get(method, parameters)

    def order_did(self, did, routing, pop, dialtime, cnam, billing_type, **kwargs):
        """
        Orders and Adds a new DID Number to the Account

        :param did: [Required] DID to be Ordered (Example: 5552223333)
        :type did: :py:class:`int`
        :param routing: [Required] Main Routing for the DID
        :type routing: :py:class:`str`
        :param pop: [Required] Point of Presence for the DID (Example: 5)
        :type pop: :py:class:`int`
        :param dialtime: [Required] Dial Time Out for the DID (Example: 60 -> in seconds)
        :type dialtime: :py:class:`int`
        :param cnam: [Required] CNAM for the DID (Boolean: True/False)
        :type cnam: :py:class:`bool`
        :param billing_type: [Required] Billing type for the DID (1 = Per Minute, 2 = Flat)
        :type billing_type: :py:class:`int`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param failover_busy: Busy Routing for the DID
        :type failover_busy: :py:class:`str`
        :param failover_unreachable: Unreachable Routing for the DID
        :type failover_unreachable: :py:class:`str`
        :param failover_noanswer: NoAnswer Routing for the DID
        :type failover_noanswer: :py:class:`str`
        :param voicemail: Voicemail for the DID (Example: 101)
        :type voicemail: :py:class:`int`
        :param callerid_prefix: Caller ID Prefix for the DID
        :type callerid_prefix: :py:class:`str`
        :param note: Note for the DID
        :type note: :py:class:`str`
        :param account: Reseller Sub Account (Example: '100001_VoIP')
        :type account: :py:class:`str`
        :param monthly: Montly Fee for Reseller Client (Example: 3.50)
        :type monthly: :py:class:`float`
        :param setup: Setup Fee for Reseller Client (Example: 1.99)
        :type setup: :py:class:`float`
        :param minute: Minute Rate for Reseller Client (Example: 0.03)
        :type minute: :py:class:`float`
        :param test: Set to True if testing how Orders work
                        - Orders can not be undone
                        - When testing, no Orders are made
        :type test: :py:class:`bool`

        :returns: :py:class:`dict`

        routing, failover_busy, failover_unreachable and failover_noanswer
        can receive values in the following format => header:record_id
        Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.
        Examples:

            account     Used for routing calls to Sub Accounts
                        You can get all sub accounts using the getSubAccounts function

            fwd         Used for routing calls to Forwarding entries.
                        You can get the ID right after creating a Forwarding with setForwarding
                        or by requesting all forwardings entries with getForwardings.

            vm          Used for routing calls to a Voicemail.
                        You can get all voicemails and their IDs using the getVoicemails function

            sys         System Options:
                        hangup       = Hangup the Call
                        busy         = Busy tone
                        noservice    = System Recording: Number not in service
                        disconnected = System Recording: Number has been disconnected
                        dtmf         = DTMF Test
                        echo         = ECHO Test


            none        Used to route calls to no action

        Examples:
            'account:100001_VoIP'
            'fwd:1026'
            'vm:101'
            'none:'
            'sys:echo'
        """
        method = "orderDID"

        kwargs.update({
            "method": method,
            "did": did,
            "routing": routing,
            "pop": pop,
            "dialtime": dialtime,
            "cnam": cnam,
            "billing_type": billing_type,
        })

        return self._order(**kwargs)

    def order_did_international_geographic(self, location_id, quantity, routing, pop, dialtime, cnam, billing_type, **kwargs):
        """
        Orders and Adds new International Geographic DID Numbers to the Account

        :param location_id: [Required] ID for a specific International Location (Values from dids.get_dids_international_geographic)
        :type location_id: :py:class:`int`
        :param quantity: [Required] Number of dids to be purchased (Example: 2)
        :type quantity: :py:class:`int`
        :param routing: [Required] Main Routing for the DID
        :type routing: :py:class:`str`
        :param pop: [Required] Point of Presence for the DID (Example: 5)
        :type pop: :py:class:`int`
        :param dialtime: [Required] Dial Time Out for the DID (Example: 60 -> in seconds)
        :type dialtime: :py:class:`int`
        :param cnam: [Required] CNAM for the DID (Boolean: True/False)
        :type cnam: :py:class:`bool`
        :param billing_type: [Required] Billing type for the DID (1 = Per Minute, 2 = Flat)
        :type billing_type: :py:class:`int`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param failover_busy: Busy Routing for the DID
        :type failover_busy: :py:class:`str`
        :param failover_unreachable: Unreachable Routing for the DID
        :type failover_unreachable: :py:class:`str`
        :param failover_noanswer: NoAnswer Routing for the DID
        :type failover_noanswer: :py:class:`str`
        :param voicemail: Voicemail for the DID (Example: 101)
        :type voicemail: :py:class:`int`
        :param callerid_prefix: Caller ID Prefix for the DID
        :type callerid_prefix: :py:class:`str`
        :param note: Note for the DID
        :type note: :py:class:`str`
        :param account: Reseller Sub Account (Example: '100001_VoIP')
        :type account: :py:class:`str`
        :param monthly: Montly Fee for Reseller Client (Example: 3.50)
        :type monthly: :py:class:`float`
        :param setup: Setup Fee for Reseller Client (Example: 1.99)
        :type setup: :py:class:`float`
        :param minute: Minute Rate for Reseller Client (Example: 0.03)
        :type minute: :py:class:`float`
        :param test: Set to True if testing how Orders work
                        - Orders can not be undone
                        - When testing, no Orders are made
        :type test: :py:class:`bool`

        :returns: :py:class:`dict`

        routing, failover_busy, failover_unreachable and failover_noanswer
        can receive values in the following format => header:record_id
        Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.
        Examples:

            account     Used for routing calls to Sub Accounts
                        You can get all sub accounts using the getSubAccounts function

            fwd         Used for routing calls to Forwarding entries.
                        You can get the ID right after creating a Forwarding with setForwarding
                        or by requesting all forwardings entries with getForwardings.

            vm          Used for routing calls to a Voicemail.
                        You can get all voicemails and their IDs using the getVoicemails function

            sys         System Options:
                        hangup       = Hangup the Call
                        busy         = Busy tone
                        noservice    = System Recording: Number not in service
                        disconnected = System Recording: Number has been disconnected
                        dtmf         = DTMF Test
                        echo         = ECHO Test


            none        Used to route calls to no action

        Examples:
            'account:100001_VoIP'
            'fwd:1026'
            'vm:101'
            'none:'
            'sys:echo'
        """
        method = "orderDIDInternationalGeographic"

        kwargs.update({
            "method": method,
            "location_id": location_id,
            "quantity": quantity,
            "routing": routing,
            "pop": pop,
            "dialtime": dialtime,
            "cnam": cnam,
            "billing_type": billing_type,
        })

        return self._order(**kwargs)

    def order_did_international_national(self, location_id, quantity, routing, pop, dialtime, cnam, billing_type, **kwargs):
        """
        Orders and Adds new International National DID Numbers to the Account

        :param location_id: [Required] ID for a specific International Location (Values from dids.get_dids_international_geographic)
        :type location_id: :py:class:`int`
        :param quantity: [Required] Number of dids to be purchased (Example: 2)
        :type quantity: :py:class:`int`
        :param routing: [Required] Main Routing for the DID
        :type routing: :py:class:`str`
        :param pop: [Required] Point of Presence for the DID (Example: 5)
        :type pop: :py:class:`int`
        :param dialtime: [Required] Dial Time Out for the DID (Example: 60 -> in seconds)
        :type dialtime: :py:class:`int`
        :param cnam: [Required] CNAM for the DID (Boolean: True/False)
        :type cnam: :py:class:`bool`
        :param billing_type: [Required] Billing type for the DID (1 = Per Minute, 2 = Flat)
        :type billing_type: :py:class:`int`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param failover_busy: Busy Routing for the DID
        :type failover_busy: :py:class:`str`
        :param failover_unreachable: Unreachable Routing for the DID
        :type failover_unreachable: :py:class:`str`
        :param failover_noanswer: NoAnswer Routing for the DID
        :type failover_noanswer: :py:class:`str`
        :param voicemail: Voicemail for the DID (Example: 101)
        :type voicemail: :py:class:`int`
        :param callerid_prefix: Caller ID Prefix for the DID
        :type callerid_prefix: :py:class:`str`
        :param note: Note for the DID
        :type note: :py:class:`str`
        :param account: Reseller Sub Account (Example: '100001_VoIP')
        :type account: :py:class:`str`
        :param monthly: Montly Fee for Reseller Client (Example: 3.50)
        :type monthly: :py:class:`float`
        :param setup: Setup Fee for Reseller Client (Example: 1.99)
        :type setup: :py:class:`float`
        :param minute: Minute Rate for Reseller Client (Example: 0.03)
        :type minute: :py:class:`float`
        :param test: Set to True if testing how Orders work
                        - Orders can not be undone
                        - When testing, no Orders are made
        :type test: :py:class:`bool`

        :returns: :py:class:`dict`

        routing, failover_busy, failover_unreachable and failover_noanswer
        can receive values in the following format => header:record_id
        Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.
        Examples:

            account     Used for routing calls to Sub Accounts
                        You can get all sub accounts using the getSubAccounts function

            fwd         Used for routing calls to Forwarding entries.
                        You can get the ID right after creating a Forwarding with setForwarding
                        or by requesting all forwardings entries with getForwardings.

            vm          Used for routing calls to a Voicemail.
                        You can get all voicemails and their IDs using the getVoicemails function

            sys         System Options:
                        hangup       = Hangup the Call
                        busy         = Busy tone
                        noservice    = System Recording: Number not in service
                        disconnected = System Recording: Number has been disconnected
                        dtmf         = DTMF Test
                        echo         = ECHO Test


            none        Used to route calls to no action

        Examples:
            'account:100001_VoIP'
            'fwd:1026'
            'vm:101'
            'none:'
            'sys:echo'
        """
        method = "orderDIDInternationalNational"

        kwargs.update({
            "method": method,
            "location_id": location_id,
            "quantity": quantity,
            "routing": routing,
            "pop": pop,
            "dialtime": dialtime,
            "cnam": cnam,
            "billing_type": billing_type,
        })

        return self._order(**kwargs)

    def order_did_international_toll_free(self, location_id, quantity, routing, pop, dialtime, cnam, billing_type, **kwargs):
        """
        Orders and Adds new International TollFree DID Numbers to the Account

        :param location_id: [Required] ID for a specific International Location (Values from dids.get_dids_international_geographic)
        :type location_id: :py:class:`int`
        :param quantity: [Required] Number of dids to be purchased (Example: 2)
        :type quantity: :py:class:`int`
        :param routing: [Required] Main Routing for the DID
        :type routing: :py:class:`str`
        :param pop: [Required] Point of Presence for the DID (Example: 5)
        :type pop: :py:class:`int`
        :param dialtime: [Required] Dial Time Out for the DID (Example: 60 -> in seconds)
        :type dialtime: :py:class:`int`
        :param cnam: [Required] CNAM for the DID (Boolean: True/False)
        :type cnam: :py:class:`bool`
        :param billing_type: [Required] Billing type for the DID (1 = Per Minute, 2 = Flat)
        :type billing_type: :py:class:`int`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param failover_busy: Busy Routing for the DID
        :type failover_busy: :py:class:`str`
        :param failover_unreachable: Unreachable Routing for the DID
        :type failover_unreachable: :py:class:`str`
        :param failover_noanswer: NoAnswer Routing for the DID
        :type failover_noanswer: :py:class:`str`
        :param voicemail: Voicemail for the DID (Example: 101)
        :type voicemail: :py:class:`int`
        :param callerid_prefix: Caller ID Prefix for the DID
        :type callerid_prefix: :py:class:`str`
        :param note: Note for the DID
        :type note: :py:class:`str`
        :param account: Reseller Sub Account (Example: '100001_VoIP')
        :type account: :py:class:`str`
        :param monthly: Montly Fee for Reseller Client (Example: 3.50)
        :type monthly: :py:class:`float`
        :param setup: Setup Fee for Reseller Client (Example: 1.99)
        :type setup: :py:class:`float`
        :param minute: Minute Rate for Reseller Client (Example: 0.03)
        :type minute: :py:class:`float`
        :param test: Set to True if testing how Orders work
                        - Orders can not be undone
                        - When testing, no Orders are made
        :type test: :py:class:`bool`

        :returns: :py:class:`dict`

        routing, failover_busy, failover_unreachable and failover_noanswer
        can receive values in the following format => header:record_id
        Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.
        Examples:

            account     Used for routing calls to Sub Accounts
                        You can get all sub accounts using the getSubAccounts function

            fwd         Used for routing calls to Forwarding entries.
                        You can get the ID right after creating a Forwarding with setForwarding
                        or by requesting all forwardings entries with getForwardings.

            vm          Used for routing calls to a Voicemail.
                        You can get all voicemails and their IDs using the getVoicemails function

            sys         System Options:
                        hangup       = Hangup the Call
                        busy         = Busy tone
                        noservice    = System Recording: Number not in service
                        disconnected = System Recording: Number has been disconnected
                        dtmf         = DTMF Test
                        echo         = ECHO Test


            none        Used to route calls to no action

        Examples:
            'account:100001_VoIP'
            'fwd:1026'
            'vm:101'
            'none:'
            'sys:echo'
        """
        method = "orderDIDInternationalTollFree"

        kwargs.update({
            "method": method,
            "location_id": location_id,
            "quantity": quantity,
            "routing": routing,
            "pop": pop,
            "dialtime": dialtime,
            "cnam": cnam,
            "billing_type": billing_type,
        })

        return self._order(**kwargs)

    def order_did_virtual(self, digits, routing, pop, dialtime, cnam, billing_type, **kwargs):
        """
        Orders and Adds a new Virtual DID Number to the Account

        :param digits: [Required] Three Digits for the new Virtual DID (Example: 001)
        :type digits: :py:class:`int`
        :param routing: [Required] Main Routing for the DID
        :type routing: :py:class:`str`
        :param pop: [Required] Point of Presence for the DID (Example: 5)
        :type pop: :py:class:`int`
        :param dialtime: [Required] Dial Time Out for the DID (Example: 60 -> in seconds)
        :type dialtime: :py:class:`int`
        :param cnam: [Required] CNAM for the DID (Boolean: True/False)
        :type cnam: :py:class:`bool`
        :param billing_type: [Required] Billing type for the DID (1 = Per Minute, 2 = Flat)
        :type billing_type: :py:class:`int`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param failover_busy: Busy Routing for the DID
        :type failover_busy: :py:class:`str`
        :param failover_unreachable: Unreachable Routing for the DID
        :type failover_unreachable: :py:class:`str`
        :param failover_noanswer: NoAnswer Routing for the DID
        :type failover_noanswer: :py:class:`str`
        :param voicemail: Voicemail for the DID (Example: 101)
        :type voicemail: :py:class:`int`
        :param callerid_prefix: Caller ID Prefix for the DID
        :type callerid_prefix: :py:class:`str`
        :param note: Note for the DID
        :type note: :py:class:`str`
        :param account: Reseller Sub Account (Example: '100001_VoIP')
        :type account: :py:class:`str`
        :param monthly: Montly Fee for Reseller Client (Example: 3.50)
        :type monthly: :py:class:`float`
        :param setup: Setup Fee for Reseller Client (Example: 1.99)
        :type setup: :py:class:`float`
        :param minute: Minute Rate for Reseller Client (Example: 0.03)
        :type minute: :py:class:`float`
        :param test: Set to True if testing how Orders work
                        - Orders can not be undone
                        - When testing, no Orders are made
        :type test: :py:class:`bool`

        :returns: :py:class:`dict`

        routing, failover_busy, failover_unreachable and failover_noanswer
        can receive values in the following format => header:record_id
        Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.
        Examples:

            account     Used for routing calls to Sub Accounts
                        You can get all sub accounts using the getSubAccounts function

            fwd         Used for routing calls to Forwarding entries.
                        You can get the ID right after creating a Forwarding with setForwarding
                        or by requesting all forwardings entries with getForwardings.

            vm          Used for routing calls to a Voicemail.
                        You can get all voicemails and their IDs using the getVoicemails function

            sys         System Options:
                        hangup       = Hangup the Call
                        busy         = Busy tone
                        noservice    = System Recording: Number not in service
                        disconnected = System Recording: Number has been disconnected
                        dtmf         = DTMF Test
                        echo         = ECHO Test


            none        Used to route calls to no action

        Examples:
            'account:100001_VoIP'
            'fwd:1026'
            'vm:101'
            'none:'
            'sys:echo'
        """
        method = "orderDIDVirtual"

        kwargs.update({
            "method": method,
            "digits": digits,
            "routing": routing,
            "pop": pop,
            "dialtime": dialtime,
            "cnam": cnam,
            "billing_type": billing_type,
        })

        return self._order(**kwargs)

    def order_toll_free(self, did, routing, pop, dialtime, cnam, billing_type, **kwargs):
        """
        Orders and Adds a new Toll Free Number to the Account

        :param did: [Required] DID to be Ordered (Example: 8772223333)
        :type did: :py:class:`int`
        :param routing: [Required] Main Routing for the DID
        :type routing: :py:class:`str`
        :param pop: [Required] Point of Presence for the DID (Example: 5)
        :type pop: :py:class:`int`
        :param dialtime: [Required] Dial Time Out for the DID (Example: 60 -> in seconds)
        :type dialtime: :py:class:`int`
        :param cnam: [Required] CNAM for the DID (Boolean: True/False)
        :type cnam: :py:class:`bool`
        :param billing_type: [Required] Billing type for the DID (1 = Per Minute, 2 = Flat)
        :type billing_type: :py:class:`int`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param failover_busy: Busy Routing for the DID
        :type failover_busy: :py:class:`str`
        :param failover_unreachable: Unreachable Routing for the DID
        :type failover_unreachable: :py:class:`str`
        :param failover_noanswer: NoAnswer Routing for the DID
        :type failover_noanswer: :py:class:`str`
        :param voicemail: Voicemail for the DID (Example: 101)
        :type voicemail: :py:class:`int`
        :param callerid_prefix: Caller ID Prefix for the DID
        :type callerid_prefix: :py:class:`str`
        :param note: Note for the DID
        :type note: :py:class:`str`
        :param account: Reseller Sub Account (Example: '100001_VoIP')
        :type account: :py:class:`str`
        :param monthly: Montly Fee for Reseller Client (Example: 3.50)
        :type monthly: :py:class:`float`
        :param setup: Setup Fee for Reseller Client (Example: 1.99)
        :type setup: :py:class:`float`
        :param minute: Minute Rate for Reseller Client (Example: 0.03)
        :type minute: :py:class:`float`
        :param test: Set to True if testing how Orders work
                        - Orders can not be undone
                        - When testing, no Orders are made
        :type test: :py:class:`bool`

        :returns: :py:class:`dict`

        routing, failover_busy, failover_unreachable and failover_noanswer
        can receive values in the following format => header:record_id
        Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.
        Examples:

            account     Used for routing calls to Sub Accounts
                        You can get all sub accounts using the getSubAccounts function

            fwd         Used for routing calls to Forwarding entries.
                        You can get the ID right after creating a Forwarding with setForwarding
                        or by requesting all forwardings entries with getForwardings.

            vm          Used for routing calls to a Voicemail.
                        You can get all voicemails and their IDs using the getVoicemails function

            sys         System Options:
                        hangup       = Hangup the Call
                        busy         = Busy tone
                        noservice    = System Recording: Number not in service
                        disconnected = System Recording: Number has been disconnected
                        dtmf         = DTMF Test
                        echo         = ECHO Test


            none        Used to route calls to no action

        Examples:
            'account:100001_VoIP'
            'fwd:1026'
            'vm:101'
            'none:'
            'sys:echo'
        """
        method = "orderTollFree"

        kwargs.update({
            "method": method,
            "did": did,
            "routing": routing,
            "pop": pop,
            "dialtime": dialtime,
            "cnam": cnam,
            "billing_type": billing_type,
        })

        return self._order(**kwargs)

    def order_vanity(self, did, routing, pop, dialtime, cnam, billing_type, carrier, **kwargs):
        """
        Orders and Adds a new Vanity Toll Free Number to the Account

        :param did: [Required] DID to be Ordered (Example: 8772223333)
        :type did: :py:class:`int`
        :param routing: [Required] Main Routing for the DID
        :type routing: :py:class:`str`
        :param pop: [Required] Point of Presence for the DID (Example: 5)
        :type pop: :py:class:`int`
        :param dialtime: [Required] Dial Time Out for the DID (Example: 60 -> in seconds)
        :type dialtime: :py:class:`int`
        :param cnam: [Required] CNAM for the DID (Boolean: True/False)
        :type cnam: :py:class:`bool`
        :param billing_type: [Required] Billing type for the DID (1 = Per Minute, 2 = Flat)
        :type billing_type: :py:class:`int`
        :param carrier: [Required] Carrier for the DID (Values from dids.get_carriers)
        :type carrier: :py:class:`int`
        :param **kwargs: All optional parameters
        :type **kwargs: :py:class:`dict`

        :param failover_busy: Busy Routing for the DID
        :type failover_busy: :py:class:`str`
        :param failover_unreachable: Unreachable Routing for the DID
        :type failover_unreachable: :py:class:`str`
        :param failover_noanswer: NoAnswer Routing for the DID
        :type failover_noanswer: :py:class:`str`
        :param voicemail: Voicemail for the DID (Example: 101)
        :type voicemail: :py:class:`int`
        :param callerid_prefix: Caller ID Prefix for the DID
        :type callerid_prefix: :py:class:`str`
        :param note: Note for the DID
        :type note: :py:class:`str`
        :param account: Reseller Sub Account (Example: '100001_VoIP')
        :type account: :py:class:`str`
        :param monthly: Montly Fee for Reseller Client (Example: 3.50)
        :type monthly: :py:class:`float`
        :param setup: Setup Fee for Reseller Client (Example: 1.99)
        :type setup: :py:class:`float`
        :param minute: Minute Rate for Reseller Client (Example: 0.03)
        :type minute: :py:class:`float`
        :param test: Set to True if testing how Orders work
                        - Orders can not be undone
                        - When testing, no Orders are made
        :type test: :py:class:`bool`

        :returns: :py:class:`dict`

        routing, failover_busy, failover_unreachable and failover_noanswer
        can receive values in the following format => header:record_id
        Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.
        Examples:

            account     Used for routing calls to Sub Accounts
                        You can get all sub accounts using the getSubAccounts function

            fwd         Used for routing calls to Forwarding entries.
                        You can get the ID right after creating a Forwarding with setForwarding
                        or by requesting all forwardings entries with getForwardings.

            vm          Used for routing calls to a Voicemail.
                        You can get all voicemails and their IDs using the getVoicemails function

            sys         System Options:
                        hangup       = Hangup the Call
                        busy         = Busy tone
                        noservice    = System Recording: Number not in service
                        disconnected = System Recording: Number has been disconnected
                        dtmf         = DTMF Test
                        echo         = ECHO Test


            none        Used to route calls to no action

        Examples:
            'account:100001_VoIP'
            'fwd:1026'
            'vm:101'
            'none:'
            'sys:echo'
        """
        method = "orderVanity"

        kwargs.update({
            "method": method,
            "did": did,
            "routing": routing,
            "pop": pop,
            "dialtime": dialtime,
            "cnam": cnam,
            "billing_type": billing_type,
            "carrier": carrier,
        })

        return self._order(**kwargs)

    def search_dids_can(self, search_type, query, province=None):
        """
        Searches for Canadian DIDs by Province using a Search Criteria

        :param search_type: [Required] Type of search (Values: 'starts', 'contains', 'ends')
        :type search_type: :py:class:`str`
        :param query: [Required] Query for searching (Examples: 'JOHN', '555', '123ABC')
        :type query: :py:class:`str`

        :param province: Canadian Province (Values from dids.get_provinces)
        :type province: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "searchDIDsCAN"

        if not isinstance(search_type, str):
            raise ValueError("Type of search needs to be a str (Values: 'starts', 'contains', 'ends')")

        if not isinstance(query, str):
            raise ValueError("Query for searching needs to be a str (Examples: 'JOHN', '555', '123ABC')")

        parameters = {
            "type": search_type,
            "query": query
        }

        if province:
            if not isinstance(province, str):
                raise ValueError("Canadian Province needs to be a str (Values from dids.get_provinces)")
            else:
                parameters["province"] = province

        return self._voipms_client._get(method, parameters)

    def search_dids_usa(self, search_type, query, state=None):
        """
        Searches for USA DIDs by State using a Search Criteria

        :param search_type: [Required] Type of search (Values: 'starts', 'contains', 'ends')
        :type search_type: :py:class:`str`
        :param query: [Required] Query for searching (Examples: 'JOHN', '555', '123ABC')
        :type query: :py:class:`str`

        :param state: Canadian Province (Values from dids.get_states)
        :type state: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "searchDIDsUSA"

        if not isinstance(search_type, str):
            raise ValueError("Type of search needs to be a str (Values: 'starts', 'contains', 'ends')")

        if not isinstance(query, str):
            raise ValueError("Query for searching needs to be a str (Examples: 'JOHN', '555', '123ABC')")

        parameters = {
            "type": search_type,
            "query": query
        }

        if state:
            if not isinstance(state, str):
                raise ValueError("United States State needs to be a str (Values from dids.get_states)")
            else:
                parameters["state"] = state

        return self._voipms_client._get(method, parameters)

    def search_toll_free_can_us(self, search_type=None, query=None):
        """
        Searches for USA/Canada Toll Free Numbers using a Search Criteria

        - Shows all USA/Canada Toll Free Numbers available if no criteria is provided.

        :param search_type: Type of search (Values: 'starts', 'contains', 'ends')
        :type search_type: :py:class:`str`
        :param query: Query for searching (Examples: 'JOHN', '555', '123ABC')
        :type query: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "searchTollFreeCanUS"

        parameters = {}

        if search_type:
            if not isinstance(search_type, str):
                raise ValueError("Type of search needs to be a str (Values: 'starts', 'contains', 'ends')")
            else:
                parameters["type"] = search_type

        if query:
            if not isinstance(query, str):
                raise ValueError("Query for searching needs to be a str (Examples: 'JOHN', '555', '123ABC')")
            else:
                parameters["query"] = query

        return self._voipms_client._get(method, parameters)

    def search_toll_free_usa(self, search_type=None, query=None):
        """
        Searches for USA Toll Free Numbers using a Search Criteria

        - Shows all USA Toll Free Numbers available if no criteria is provided.

        :param search_type: Type of search (Values: 'starts', 'contains', 'ends')
        :type search_type: :py:class:`str`
        :param query: Query for searching (Examples: 'JOHN', '555', '123ABC')
        :type query: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "searchTollFreeUSA"

        parameters = {}

        if search_type:
            if not isinstance(search_type, str):
                raise ValueError("Type of search needs to be a str (Values: 'starts', 'contains', 'ends')")
            else:
                parameters["type"] = search_type

        if query:
            if not isinstance(query, str):
                raise ValueError("Query for searching needs to be a str (Examples: 'JOHN', '555', '123ABC')")
            else:
                parameters["query"] = query

        return self._voipms_client._get(method, parameters)

    def search_vanity(self, search_type, query):
        """
        Searches for USA DIDs by State using a Search Criteria

        :param search_type: [Required] Type of Vanity Number (Values: '8**', '800', '855', '866', '877', '888')
        :type search_type: :py:class:`str`
        :param query: [Required] Query for searching : 7 Chars (Examples: '***JHON', '**555**', '**HELLO')
        :type query: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "searchVanity"

        if not isinstance(search_type, str):
            raise ValueError("Type of Vanity Number needs to be a str (Values: '8**', '800', '855', '866', '877', '888')")

        if not isinstance(query, str):
            raise ValueError("Query for searching : 7 Chars needs to be a str (Examples: '***JHON', '**555**', '**HELLO')")

        parameters = {
            "type": search_type,
            "query": query
        }

        return self._voipms_client._get(method, parameters)

    def send_sms(self, did, dst, message):
        """
        Send a SMS message to a Destination Number

        :param did: [Required] DID Numbers which is sending the message (Example: 5551234567)
        :type did: :py:class:`int`
        :param dst: [Required] Destination Number (Example: 5551234568) 
        :type dst: :py:class:`int`
        :param message: [Required] Message to be sent (Example: 'hello John Smith' max chars: 160)
        :type message: :py:class:`str`

        :returns: :py:class:`dict`
        """
        method = "sendSMS"

        if not isinstance(did, int):
            raise ValueError("DID Numbers which is sending the message needs to be an int (Example: 5551234567)")

        if not isinstance(dst, int):
            raise ValueError("Destination Number needs to be an int (Example: 5551234568) ")

        if not isinstance(message, str):
            raise ValueError("Message to be sent needs to be a str (Example: 'hello John Smith' max chars: 160)")
        else:
            if len(message) > 160:
                raise ValueError("Message to be sent can only have 160 chars")

        parameters = {
            "did": did,
            "dst": dst,
            "message": message,
        }

        return self._voipms_client._get(method, parameters)
