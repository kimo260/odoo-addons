# -*- coding: utf-8 -*-
from openerp import fields, models, api
import logging
_logger = logging.getLogger(__name__)


class mrp_bom(models.Model):

    _inherit = "mrp.bom"

    auto_produce_on_picking = fields.Boolean(
        'Auto Produce on Picking',
        help='When validating a picking, \
            if picking move has a related Manufacturing Order, \
            then auto produce on delivery')


class stock_move(models.Model):

    _inherit = "stock.move"

    @api.multi
    def action_done(self):
        for move in self:
            # TODO perhups improove and search as many procuremnts as exists
            # and finish them till move quantity is reached
            _logger.info('Search for production procurement for move_id %s' % (
                move.id))
            if not move.picking_id:
                # if no picking, then it is a move of production order or
                # another move we don want to use
                continue
            # we search for procurements of this move procurment group,
            # that are has a production order lined whick is for the same
            # product, it is not cancel or dane and has bom with auto prod
            production_procurement = self.env['procurement.order'].search([
                ('group_id', '=', move.group_id.id),
                ('production_id.product_id', '=', move.product_id.id),
                ('production_id.bom_id.auto_produce_on_picking', '=', True),
                ('production_id.state', 'not in', ('cancel', 'done')),
                ], limit=1)
            _logger.info('Production procurements found %s' % (
                production_procurement))
            if production_procurement:
                production = production_procurement.production_id
                if production.state == 'draft':
                    production.action_assign()
                done = 0.0
                product_qty = move.product_uom_qty
                _logger.info('Getting production remaining qty')
                for prod_move in production.move_created_ids2:
                    _logger.info('Productin move_id %s' % prod_move.id)
                    if prod_move.product_id == production.product_id:
                        if not prod_move.scrapped:
                            done += prod_move.product_qty
                remaining_prod_qty = (
                    production.product_qty - done) or production.product_qty
                if remaining_prod_qty < product_qty:
                    product_qty = remaining_prod_qty
                _logger.info(
                    'Running Action produce on production order %s and quantity %s' % (
                        production.id, product_qty))
                production.action_produce(
                    production.id, product_qty, 'consume_produce')
        return super(stock_move, self).action_done()
