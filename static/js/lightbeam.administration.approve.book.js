/**
 * Created by HP on 24-May-17.
 */

function approveBook(product_id, action) {
    if(action == 'reject')
    {
        if (!confirm('Are you sure to reject?')) {
            return;
        }
    }

    $.ajax({
        type: "POST",
        url: "/administration-approve-book/",
        dataType: "json",
        success: function (status) {
            if(status)
            {
                row = document.getElementById('tr-' + product_id);
                row.parentNode.removeChild(row);
            }
            else
            {

            }
        },
        data: {
            product_id: product_id,
            action: action,
            csrfmiddlewaretoken: getCookie('csrftoken')
        }
    });
}