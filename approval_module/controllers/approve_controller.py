from odoo import http
from odoo.http import request


class RequestApprovalController(http.Controller):
    @http.route('/request/approve/<string:token>', type='http', auth='public', website=True)
    def request_approval(self, token):
        request_form = request.env['purchase.requisition'].sudo().search([('approval_link', '=', token)])
        if request_form:
            request_form.write({'state': 'approved'})
            msg = "Request approved successfully!"


            return f"""<script>alert("{msg}");window.close();</script>"""
        else:
            return "Invalid approval link!"

    @http.route('/request/disapprove/<string:token>', type='http', auth='public', website=True, csrf=False,
                method=['GET', 'POST'])
    def request_disapproval(self, token, **post):
        request_form = request.env['purchase.requisition'].sudo().search([('approval_link', '=', token)])
        if request_form:
            if request.httprequest.method == 'POST' and 'reason' in post:
                reason = post.get('reason')
                request_form.write({'state': 'disapprove', 'disapproval_reason': reason})
                return """<script>window.close();</script>"""
            else:
                return """
                    <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <div class="justify-content-center"> 
            <div class="modal" tabindex="-1" id="modal-show">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title">Disapproved Reason</h5>
                    </div>
                    <form method="post">
                    <div class="modal-body">
                            <textarea class="form-control"type="text" name="reason" placeholder="Reason here" id="text-area"></textarea>
                    </div>
                    <div class="modal-footer">
                      <button type="submit" class="btn btn-danger" id="saved-btn">Save</button>
                    </div>
                </form>
                  </div>
                </div>
              </div>
        </div>
    </div>
    
</body>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js" integrity="sha384-SR1sx49pcuLnqZUnnPwx6FCym0wLsk5JZuNx2bPPENzswTNFaQU1RDvt3wT4gWFG" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.min.js" integrity="sha384-j0CNLUeiqtyaRmlzUHCPZ+Gy5fQu0dQ6eZ/xAww941Ai1SxSY+0EQqNXNE6DZiVc" crossorigin="anonymous"></script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script>
    $(document).ready(function(){
        $('#modal-show').show()

    $('#saved-btn').click(function(){
        var text_area = $('#text-area').val()
        if(text_area == ''){
            alert('Enter Something')
            console.log(text_area)
            return false;
        }else{
            alert('Success')
            console.log(text_area)
        }
    })
        


    });
</script>
</html>
                    """
        else:
            return "Invalid approval link!"
