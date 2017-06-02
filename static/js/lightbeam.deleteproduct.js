/**
 * Created by HP on 30-May-17.
 */
function deleteProduct(product_id) {
    if (!confirm('Are you sure to delete this book?')) {
        return;
    }
    row = document.getElementById('tr-' + product_id);
    btn = document.getElementById('action-' + product_id);
    $.ajax({
        url : "/delete-product/",
        data: {product_id : product_id, csrfmiddlewaretoken: csrftoken},
        type: "POST",
        dataType: "json",
        success:function(data){
            if(data > 0)
            {
                row.style.visibility = 'hidden'
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