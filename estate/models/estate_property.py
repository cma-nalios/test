from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta
class EstateProperty(models.Model):
    _name="estate.property"
    _description="Estate Property Test"
    _order = "id desc"

    name = fields.Char(string='Name', required=True)
    postcode = fields.Char("Postcode")
    property_type_id=fields.Many2one("estate.property.type", string="Property Type")
    date_availability = fields.Date("Date Availability", default=lambda x : fields.Datetime.add(fields.Datetime.today(),months=+3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", help="Je fais ceci pour tester un peu le champ aide en fait, on ne sait jamais si ça m'est utile", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage",default=False)
    garden = fields.Boolean("Garden", default=True)
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[("north","North"),("south","South"),("west","West"),("east","East")])
    active = fields.Boolean("Active", default=True)
    #state = fields.Selection(string="State", selection=[("new","New"),("offer_received","Offer Received"),("offer_accepted","Offer Accepted"),("canceled","Canceled"),("sold","Sold")], required=True, copy=False, default="new")
    state = fields.Selection(string="State", selection=[("new","New"),("offer_received","Offer Received"),("offer_accepted","Offer Accepted"),("canceled","Canceled"),("sold","Sold")], required=True, copy=False, default="new")
    #garden_orientation2 = fields.Selection(string="Garden Orientation2", selection=[("north","North"),("south","South"),("west","West"),("east","East")])
    description = fields.Text(string='Description')
    salesman_id = fields.Many2one("res.users",string="Salesman", default = lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    offer_ids = fields.One2many("estate.property.offer","property_id")
    color = fields.Integer(string="Color")
    best_price = fields.Float("Best Price", compute="_highest_offer_price")
    estate_property_type_id = fields.Many2one("estate.property.type")
    


    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        (print("Le dico ", self.env.context))
        for line in self:
            line.total_area = line.garden_area+line.living_area

    @api.depends("offer_ids.price")
    def _highest_offer_price(self):
        for line in self:
            print(len(line.mapped("offer_ids.price")))
            if len(line.mapped("offer_ids.price")) !=0:
                line.best_price = min(line.mapped("offer_ids.price"))

            else:
                line.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if(self.garden is True):
            self.garden_area = 10
            self.garden_orientation = "north"

    def cancel_action(self):
        for line in self:
            if line.state=="sold" :
                raise UserError("You cannot set the state as Cancel if the state is equal to Sold")
            
            line.state = "canceled"
        return True

    def sold_action(self):
        for line in self:
            if line.state=="canceled":
                raise UserError("You cannot set the state as Sold if the state is equal to Cancel")
            line.state = "sold"
        return True

    _sql_constraints = [
        ('checkbedrooms', 'CHECK(bedrooms >= 0)','Bedrooms must be positive, you can not have a negative number of bedrooms')
    ]
    
    @api.constrains('selling_price')
    def _constraint_on_selling_price(self):
        for line in self:
            if line.selling_price<=line.expected_price*0.9:
                raise ValidationError("Le prix de vente ne peut pas être en dessous de 90 pourcents du prix d'achat ")

    
    @api.ondelete(at_uninstall=False)
    def _no_delete_when_state_is_new_or_cancelled(self):
        for record in self:
            if record.state=="new" or record.state=="cancelled":
                raise UserError("You can not delete a property if it's state is new or false")


    def testWizard(self):
        for rec in self.env['estate.property'].browse(self.env.context.get('active_ids',[])):
            print("++++++++++++++++++THE RECORD ", rec)
            rec.write({'state' : 'sold'})


    
    #def _search_is_ongoing(self,operator,value):
     #   if operator not in ['=', '!=']:
      #      raise ValueError(_('This operator is not supported'))

       # if not isinstance(value,Float):
        #    raise ValueError(_('Value should be a float (not %s'), value)

        #"return True;