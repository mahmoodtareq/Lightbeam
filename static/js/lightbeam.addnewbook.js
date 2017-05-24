/**
 * Created by HP on 20-May-17.
 */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function Add_New_Book() {
    var ban = document.getElementById("add-new-book-banner");
    ban.innerHTML = "";

    var field = document.getElementById("add-new-book");

    var form = document.getElementById("add-book-form");
    form.style.visibility = 'hidden';      // Hide

    var fieldLabel = document.createElement("h3");
    fieldLabel.innerHTML = "You can add the book manually";

    var bookName = document.createElement("input");
    bookName.setAttribute("type", "text");
    bookName.setAttribute("value", "");
    bookName.setAttribute("name", "Book Name");
    bookName.setAttribute("class", "form-control");

    var bookNameLabel = document.createElement("label");
    bookNameLabel.innerHTML = "Book Name";


    var bookAuthors = document.createElement("input");
    bookAuthors.setAttribute("type", "text");
    bookAuthors.setAttribute("value", "");
    bookAuthors.setAttribute("name", "Book Authors");
    bookAuthors.setAttribute("class", "form-control");

    var bookAuthorLabel = document.createElement("label");
    bookAuthorLabel.innerHTML = "Book Authors (comma separated)";


    var button = document.createElement("button");
    button.className += "btn btn-primary";
    button.innerHTML = "Add Book to Database";




    field.className += "box clearfix ";
    field.className += "form-group";

    field.appendChild(fieldLabel);
    field.appendChild(bookNameLabel);
    field.appendChild(bookName);
    field.appendChild(document.createElement("br"));
    field.appendChild(bookAuthorLabel);
    field.appendChild(bookAuthors);
    field.appendChild(document.createElement("br"));
    field.appendChild(button);

    button.addEventListener("click", function (e) {
        var strBookName = bookName.value;
        var strBookAuthors = bookAuthors.value;
        $.ajax(
        {
            type: "POST",
            url: "/add-new-book/",
            dataType: "json",
            success: function (bookid) {
               if (bookid > 0)
               {
                    button.className = "btn btn-success";
                    button.innerHTML = "<strong>Success!</strong> Waiting for admin approval.";
                    form.style.visibility = 'visible';      // Hide
                    document.getElementById("id_bookname").value = bookName.value;
                    document.getElementById("id_bookid").value = bookid;
                    field.innerHTML = "<i class='fa fa-check-circle'></i> <strong>Success!</strong> Book added to database!"
                    field.className = "alert alert-success";
               }
               else
               {
                    button.className = "btn btn-danger";
                    button.innerHTML = "Some Error Occurred";
               }
            },
            data: {
                name: bookName.value,
                authors: bookAuthors.value,
                csrfmiddlewaretoken: getCookie('csrftoken')
            }
        });
    }, false)

}
