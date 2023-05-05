odoo.define('client_act.sale_cust', function (require) {
   'use strict';
   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var rpc = require('web.rpc');
   var FormController = require('web.FormController');
   var QWeb = core.qweb;
   var SaleCustom = AbstractAction.extend({

   template: 'SaleCust',
       events: {
            'click #pdf': 'print_pdf',
            'click #xlsx': 'print_xlsx',
            'click .gl-line': 'show_drop_down',
       },
       init: function(parent, action) {
           this._super(parent, action);
       },

       print_pdf: function(e){
            console.log('Test...')
            e.preventDefault();
            var self = this;
            var action_title = self._title
            self._rpc({
                model: 'account.move',
                method: 'view_report',
                args: [
                    [self.wizard_id], action_title
                ],
            }).then(function(data) {
                var action = {
                    'type': 'ir.actions.report',
                    'report_type': 'qweb-pdf',
                    'report_name': 'team_accounting.new_debit_credit_memo_report_id',
                    'report_file': 'team_accounting.new_debit_credit_memo_report_id',
                    'data': {
                        'report_data': data
                    },
                    'context': {
//                        'active_model': 'account.general.ledger',
//                        'landscape': 1,
//                        'trial_pdf_report': true
                    },
                    'display_name': action_title,
                };
                return self.do_action(action);
            });
       },
       show_drop_down: function(){
            console.log('testttt');
            var self = this;
                   var self = this;
                   self._rpc({
                       model: 'account.custom',
                       method: 'fetch_new_data',
                       args: [],
                   }).then(function(datas) {
                   console.log("dataaaaaa", datas)
                       self.$('.table_view_new').html(QWeb.render('SaleTableNew', {
                                  report_lines_data : datas,
                       }));
                   });
       },
       load_data_new_query: function () {

           },

       start: function() {
           var self = this;
//           alert("Hello")
           self.load_data();
       },
       load_data: function () {
           var self = this;
                   var self = this;
                   self._rpc({
                       model: 'account.custom',
                       method: 'get_sale_order',
                       args: [],
                   }).then(function(datas) {
                   console.log("dataaaaaa", datas)
                       self.$('.table_view').html(QWeb.render('SaleTable', {
                                  report_lines : datas,
                       }));
                   });
           },
    //PRINTING PDF HERE//
   });
   core.action_registry.add("sale_cust", SaleCustom);
   return SaleCustom;
});