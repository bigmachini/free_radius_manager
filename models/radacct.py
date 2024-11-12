from odoo import models, fields

class RadAcct(models.Model):
    _name = 'radacct'
    _description = 'RADIUS Accounting'

    acctsessionid = fields.Char(string="Acct-Session-Id", required=True, index=True)
    acctuniqueid = fields.Char(string="Acct-Unique-Id", required=True)
    username = fields.Char(string="Username", index=True)
    groupname = fields.Char(string="Group Name")
    realm = fields.Char(string="Realm")
    nasipaddress = fields.Char(string="NAS IP Address")
    nasportid = fields.Char(string="NAS Port ID")
    nasporttype = fields.Char(string="NAS Port Type")
    acctstarttime = fields.Datetime(string="Acct-Start-Time")
    acctstoptime = fields.Datetime(string="Acct-Stop-Time")
    acctsessiontime = fields.BigInteger(string="Acct-Session-Time")
    acctauthentic = fields.Char(string="Acct-Authentic")
    acctinputoctets = fields.BigInteger(string="Acct-Input-Octets")
    acctoutputoctets = fields.BigInteger(string="Acct-Output-Octets")
    calledstationid = fields.Char(string="Called-Station-Id")
    callingstationid = fields.Char(string="Calling-Station-Id")
    acctterminatecause = fields.Char(string="Acct-Terminate-Cause")
    servicetype = fields.Char(string="Service-Type")
    framedprotocol = fields.Char(string="Framed-Protocol")
    framedipaddress = fields.Char(string="Framed-IP-Address")
    acctstartdelay = fields.Integer(string="Acct-Start-Delay")
    acctstopdelay = fields.Integer(string="Acct-Stop-Delay")
    acctupdatetime = fields.Datetime(string="Acct-Update-Time", default=fields.Datetime.now)