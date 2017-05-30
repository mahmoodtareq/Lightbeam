/**
 * Created by HP on 30-May-17.
 */
function confirmProduct(product_id, type) {
    btn = document.getElementById('action-' + product_id);
    status = document.getElementById('status-' + product_id);
    $.ajax({
        url : "/confirm-product/",
        data: {product_id : product_id, type : type, csrfmiddlewaretoken: csrftoken},
        type: "POST",
        dataType: "json",
        success:function(data){
            if(data > 0)
            {
                btn.className="btn btn-success disabled btn-xs";
                btn.innerHTML="confirmed!";
            }
            else
            {
                btn.className="btn btn-danger btn-xs";
                btn.innerHTML="error!";
            }
        },
        error:function () {
            btn.className="btn btn-danger btn-xs";
            btn.innerHTML="error!";
        }
    });
}