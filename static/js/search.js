// Function used to initialize select2 on all the inputs
function initSelect2s() {
    $(".sform-ingredient").each(function() {
        $(this).select2({ placeholder: "Select an Ingredient" });
    });

    $(".sform-type").each(function() {
        $(this).select2({ placeholder: "Select Categories" });
    });

    $(".sform-cuisine").each(function() {
        $(this).select2({ placeholder: "Select Cuisines" });
    });
}

// Function used to remove select2 from the inputs
function destroySelect2s() {
    $(".sform-ingredient").select2("destroy");
    $(".sform-type").select2("destroy");
    $(".sform-cuisine").select2("destroy");
}

var ingredientnum = 0;
var stepnum = 0;
var winwidth = $(window).width();

// If the widow was resized or a phone was rotated the select2 inputs would not dynamically change size so this is used to remove and then reinitialize them so they would respond to the new screen size
$(window).resize(function() {
    // Had to put this condition in because when using the keyboard on Android it causes the viewport to change which kills the select2 while you're trying to use them *rolling eyes emoji*
    if ($(window).width() != winwidth) {
        destroySelect2s();
        initSelect2s();
        winwidth = $(window).width();
    }
});

// When the document loads the select2s are initialized
$(document).ready(function() {
    // Set select2 defaults
    $.fn.select2.defaults.set("theme", "bootstrap4");
    $.fn.select2.defaults.set("tags", "true");
    $.fn.select2.defaults.set("selectOnClose", "true");
    $.fn.select2.defaults.set("allowClear", "true");
    $.fn.select2.defaults.set("maximumSelectionLength", 3);
    initSelect2s();
});

// Function runs through all child elements within an element that have a certain classname and give them numerically unique attributes. After some testing it was found that this was not needed for what I was doing but I'm leaving this here just in case, it might be handy in the future.
function numberer(parent, classname) {
    console.log(classname);
    $(parent).each(function(index, el) {
        console.log($(this).find(classname));
        $(this)
            .find(classname)
            .attr("name", classname.replace(".", "") + index);
    });
}

// Stop select2 opening again when removing a tag which was forcing you to select a tag
$("select").on("select2:unselect", function(evt) {
    if (!evt.params.originalEvent) {
        return;
    }

    evt.params.originalEvent.stopPropagation();
});

// To have an input that uses a time picker the Tempus Dominus library is kinda tricked into only submitting a time. The defaultDate is set to midnight and so when the user uses the time picker it acts as thought you are entering a time period rather than an actual time and date. While this works pretty much how I want this does have the limit that the user can only enter times of less than 24hrs. I presume there aren't very many recipes that require that much time so I should be good but I'm sure someone out there will push the limit!
$(function() {
    $("#sformTcook").datetimepicker({
        format: "HH:mm",
        defaultDate: Date.parse("2000-01-01T00:00"),
        stepping: 5
    });
});

// Infinite Scroll Code
var $scroll = $(".recipelist").infiniteScroll({
    path: function() {
        var pageNumber = this.loadCount + 1;
        var url = window.location.href;
        if (pageNumber > pagemax) {
            return null;
        } else {
            $(".img-view > img").each(function() {
                fitImage($(this));
            });
            return url + "/" + pageNumber;
        }
    },
    append: ".recipecardsmall",
    loadOnScroll: false,

    status: ".page-load-status",
    hideNav: ".next-link"
});

// enable loadOnScroll on button click
$(".load-more").on("click", function() {
    $scroll.infiniteScroll("loadNextPage");
    $scroll.infiniteScroll("option", {
        loadOnScroll: true
    });
    $(this).hide();
});

$scroll.on("append.infiniteScroll", function(event, response, path, items) {
    $(".img-view > img").each(function() {
        fitImage($(this));
    });
});

$scroll.on("last.infiniteScroll", function(event, response, path) {
    $(".infinite-scroll-request").hide();
    console.log("Final Countdown dodododo");
});
