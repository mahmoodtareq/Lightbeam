/**
 * Created by coder on 5/15/2017.
 */

function standInQueue(btn, product_id) {
    txt = document.getElementById("txt-" + product_id);
    $.ajax({
        url : "/book-request/",
        data: {product_id : product_id, type : "stand-in-queue", csrfmiddlewaretoken: csrftoken},
        type: "POST",
        dataType: "json",
        success:function(data){
            if(data > 0)
            {
                btn.className="btn btn-success";
                btn.innerHTML="you are in queue!";
                txt.innerHTML="(You are at position " + data + " in serial)";
            }
            else
            {
                btn.className="btn btn-danger";
                btn.innerHTML="you already booked!";
            }
        },
        error:function () {
            btn.className="btn btn-danger";
            btn.innerHTML="some error occurred";
        }
    });
}
