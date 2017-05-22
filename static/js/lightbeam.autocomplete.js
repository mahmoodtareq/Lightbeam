/**
 * Created by HP on 22-Apr-17.
 */
$(function() {
    $("#id_bookname").autocomplete ({
        source: "/get-book-suggestion/",
        minLength: 2,
        select: function (event, ui) {
            //alert( "You selected: " + ui.item.id );
            $("#id_bookid").val(ui.item.id);
        }
    });
});