from odoo import models, fields

class RadAcct(models.Model):
    _name = 'radacct'
    _description = 'RADIUS Accounting'

    AcctSessionId = fields.Char(string="Acct-Session-Id", required=True, index=True)
    AcctUniqueId = fields.Char(string="Acct-Unique-Id", required=True)
    UserName = fields.Char(string="Username", index=True)
    GroupName = fields.Char(string="Group Name")
    Realm = fields.Char(string="Realm")
    NASIPAddress = fields.Char(string="NAS IP Address")
    NASPortId = fields.Char(string="NAS Port ID")
    NASPortType = fields.Char(string="NAS Port Type")
    AcctStartTime = fields.Datetime(string="Acct-Start-Time")
    AcctStopTime = fields.Datetime(string="Acct-Stop-Time")
    AcctSessionTime = fields.Integer(string="Acct-Session-Time")
    AcctAuthentic = fields.Char(string="Acct-Authentic")
    AcctInputOctets = fields.Integer(string="Acct-Input-Octets")
    AcctOutputOctets = fields.Integer(string="Acct-Output-Octets")
    CalledStationId = fields.Char(string="Called-Station-Id")
    CallingStationId = fields.Char(string="Calling-Station-Id")
    AcctTerminateCause = fields.Char(string="Acct-Terminate-Cause")
    ServiceType = fields.Char(string="Service-Type")
    FramedProtocol = fields.Char(string="Framed-Protocol")
    FramedIPAddress = fields.Char(string="Framed-IP-Address")
    AcctStartDelay = fields.Integer(string="Acct-Start-Delay")
    AcctStopDelay = fields.Integer(string="Acct-Stop-Delay")
    AcctUpdateTime = fields.Datetime(string="Acct-Update-Time", default=fields.Datetime.now)
