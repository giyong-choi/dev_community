let profilePicWrapper = $(".profile-pic-wrapper");
let profilePicNote = $(".profile-pic-note");
profilePicWrapper.on({
    mouseenter: function () {
        profilePicNote.css("top", "110%");
        profilePicNote.css("opacity", "1");
    },
    mouseleave: function () {
        profilePicNote.css("top", "105%");
        profilePicNote.css("opacity", "0");
    }
});

let profileHeaderWrapper = $(".profile-header-img-wrapper");
let profileHeaderNote = $(".profile-header-note");
profileHeaderWrapper.on({
    mouseenter: function () {
        profileHeaderNote.css("top", "110%");
        profileHeaderNote.css("opacity", "1");
    },
    mouseleave: function () {
        profileHeaderNote.css("top", "105%");
        profileHeaderNote.css("opacity", "0");
    }
});


for (let i = 1; i <= 12; i++) {
    $(`#img${i}`).on({
        mouseenter: function () {
            $(`#iov${i}`).css("opacity", "1");
        },
        mouseleave: function () {
            $(`#iov${i}`).css("opacity", "0");
        }
    });
}


$("#switch").on('click', function () {
    if ($("body").hasClass("light")) {
        $("body").removeClass("light");
        $("#switch").removeClass("switched");
        $("#switch a").html('<i class="uil uil-sunset"></i> Light Mode');
    }
    else {
        $("body").addClass("light");
        $(".switch").addClass("switched");
        $("#switch a").html('<i class="uil uil-moonset"></i> Dark Mode');
    }
});

$(document).ready(function () {
    $(".category-button").click(function (event) {
        event.preventDefault();
        var category = $(this).data("category");
        var form = $('<form action="" method="get"></form>');
        form.append('<input type="hidden" name="category" value="' + category + '">');
        form.appendTo('body').submit();
    });
});