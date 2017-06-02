/**
 * Created by HP on 22-Apr-17.
 */

function deleteRequest(serial_id) {
    if (!confirm('Are you sure to delete this request?')) {
        return;
    }
    row = document.getElementById('tr-' + serial_id);
    btn = document.getElementById('action-' + serial_id);
    $.ajax({
        url : "/delete-request/",
        data: {serial_id: serial_id, csrfmiddlewaretoken: csrftoken},
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