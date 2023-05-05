odoo.define('client_act.sale_cust', function (require) {
   'use strict';
   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var rpc = require('web.rpc');
   var QWeb = core.qweb;
   var SaleCustom = AbstractAction.extend({
   template: 'SaleCust',
       events: {
        'click #print_report_button': 'on_print_report',
       },

            on_print_report: function(e) {
            e.preventDefault();
            var self = this;
            var action_title = self._title;
            self._rpc({
                model: 'profit.loss.wizard',
                method: 'view_report',
                args: [
                    [self.wizard_id], action_title
                ],
            }).then(function(data) {
                var action = {
                    'type': 'ir.actions.report',
                    'report_type': 'qweb-pdf',
                    'report_name': 'team_accounting_profit_and_loss.balance_sheet',
                    'report_file': 'team_accounting_profit_and_loss.balance_sheet',
                    'data': {
                        'report_data': data,
                    },
                    'context': {
                        'active_model': 'profit.loss.wizard',
                        'landscape': 1,
                        'pnl_report': true
                    },
                    'display_name': action_title,
                };
                return self.do_action(action);
            });
        },

       init: function(parent, action) {
           this._super(parent, action);
       },
       start: function() {
           var self = this;
           alert("You've Toggle the Profit and Loss menu, don't worry it's just for testing purposes only!.. Welcome This is for ...Tesssstttingggg!!!!..")
           self.load_data();
       },
       load_data: function () {
           var self = this;
                   var self = this;
                   self._rpc({
                       model: 'sale.custom',
                       method: 'get_sale_order',
                       args: [],
                   }).then(function(datas) {
                   console.log("dataaaaaa", datas)
                       self.$('.table_view').html(QWeb.render('SaleTable', {
                                  report_lines : datas,
                       }));
                   });
           },
   });
   core.action_registry.add("sale_cust", SaleCustom);
   return SaleCustom;
});