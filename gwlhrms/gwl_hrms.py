from openerp.osv import fields, osv

class gwl_hrms(osv.osv):
    
  _inherit = "hr.employee"

  _columns = {
    'skype_id': fields.char('Skype Id', size=500),
    'blood_group': fields.char('Blood Group', size=500),
    'office_address':fields.many2one("x.officeadd", 'Office Address'),
    'doj': fields.date("Date of Joining"),
    'employee_pan': fields.char('PAN', size=20),
    'address_proof': fields.char('Address Proof', size=100),
    'address_proof_doc': fields.binary("Address Proof Document",
            help="This field holds the scanned document for address proof."),
    'id_proof': fields.char('ID Proof', size=100),
    'id_proof_doc': fields.binary("Id Proof Document",
            help="This field holds the scanned document for ID proof."),
     'total_hr' : fields.integer('Total working hrs per Month ', size=10 , help="This field holds the total working hrs (Month)."),
    'punch_card': fields.boolean("Punch Card"),
    
  }

  
def location_name_search(self, cr, user, name='', args=None, operator='ilike',
                         context=None, limit=100):
    if not args:
        args = []

    ids = []
    if len(name) == 2:
        ids = self.search(cr, user, [('code', 'ilike', name)] + args,
                          limit=limit, context=context)

    search_domain = [('name', operator, name)]
    if ids: search_domain.append(('id', 'not in', ids))
    ids.extend(self.search(cr, user, search_domain + args,
                           limit=limit, context=context))

    locations = self.name_get(cr, user, ids, context)
    return sorted(locations, key=lambda (id, name): ids.index(id))

class OfficeAddress(osv.osv):
    _name = 'x.officeadd'
    _description = 'Office Address'
    _columns = {
        'name': fields.char('Office Address', size=64,
            help='Office Address.', translate=True),
        'code': fields.char('Office Code', size=8,
            help='Office Code'),
    }
    _sql_constraints = [
        ('name_uniq', 'unique (name)',
            'Office Address must be unique !')
    ]

    _order='name'

    name_search = location_name_search
    def create(self, cursor, user, vals, context=None):
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super(OfficeAddress, self).create(cursor, user, vals,
                context=context)

    def write(self, cursor, user, ids, vals, context=None):
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super(OfficeAddress, self).write(cursor, user, ids, vals,
                context=context)
        
gwl_hrms()