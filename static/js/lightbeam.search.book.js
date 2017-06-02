/**
 * Created by coder on 5/14/2017.
 */

function bookTheBook(btn, product_id) {
    contact = document.getElementById("contact-" + product_id);
    $.ajax({
        url : "/book-request/",
        data: {product_id : product_id, type : "book-the-book", csrfmiddlewaretoken: csrftoken},
        type: "POST",
        dataType: "json",
        success:function(data){
            if(data > 0)
            {
                btn.className="btn btn-success";
                btn.innerHTML="booked successfully!";
                contact.innerHTML="view profile for contact information"
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


