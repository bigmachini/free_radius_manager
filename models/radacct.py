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
    acctupdatetime = fields.Datetime(string="Acct-Update-Time", default=fields.Datetime.now)
    acctstoptime = fields.Datetime(string="Acct-Stop-Time")
    acctsessiontime = fields.Integer(string="Acct-Session-Time")
    acctauthentic = fields.Char(string="Acct-Authentic")
    connectinfo_start = fields.Char(string="ConnectInfo_start")
    connectinfo_stop = fields.Char(string="ConnectInfo_stop")
    acctinputoctets = fields.Integer(string="Acct-Input-Octets")
    acctoutputoctets = fields.Integer(string="Acct-Output-Octets")
    calledstationid = fields.Char(string="Called-Station-Id")
    callingstationid = fields.Char(string="Calling-Station-Id")
    acctterminatecause = fields.Char(string="Acct-Terminate-Cause")
    servicetype = fields.Char(string="Service-Type")
    framedprotocol = fields.Char(string="Framed-Protocol")
    framedipaddress = fields.Char(string="Framed-IP-Address")
    framedipv6address = fields.Char(string="Framed-IPv6-Address")
    framedipv6prefix = fields.Char(string="Framed-IPv6-Prefix")
    framedinterfaceid = fields.Char(string="Framed-Interface-Id")
    delegatedipv6prefix = fields.Char(string="Delegated-IPv6-Prefix")
    acctstartdelay = fields.Integer(string="Acct-Start-Delay")
    acctstopdelay = fields.Integer(string="Acct-Stop-Delay")

    _sql_constraints = [
        ('unique_acctuniqueid', 'unique(acctuniqueid)', 'AcctUniqueId must be unique.')
    ]
