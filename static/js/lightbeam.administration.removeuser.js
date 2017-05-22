/**
 * Created by HP on 22-May-17.
 */

function removeUser(user_id) {
    if (!confirm('Are you sure to delete this user?')) {
        return;
    }
    $.ajax({
        type: "POST",
        url: "/administration-remove-user/",
        dataType: "json",
        success: function (status) {
            if(status)
            {
                location.reload();
            }
            else
            {

            }
        },
        data: {
            user_id: user_id,
            csrfmiddlewaretoken: getCookie('csrftoken')
        }
    });
}