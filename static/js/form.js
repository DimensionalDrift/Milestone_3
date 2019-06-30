// Function used to initialize select2 on all the inputs
function initSelect2s() {
    $(".rform-ingredient").each(function() {
        $(this).select2({ placeholder: "Select an Ingredient" });
    });

    $(".rform-unit").each(function() {
        $(this).select2({ placeholder: "Select a Unit" });
    });

    $(".rform-type").each(function() {
        $(this).select2({ placeholder: "Select Categories" });
    });

    $(".rform-cuisine").each(function() {
        $(this).select2({ placeholder: "Select Cuisines" });
    });

    $(".rform-utensils").each(function() {
        $(this).select2({ placeholder: "Select Utensils" });
    });
}

// Function used to remove select2 from the inputs
function destroySelect2s() {
    $(".rform-ingredient").select2("destroy");
    $(".rform-unit").select2("destroy");
    $(".rform-type").select2("destroy");
    $(".rform-cuisine").select2("destroy");
    $(".rform-utensils").select2("destroy");
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

// When the 'Add Ingredient' button is pressed, the first row of inputs are cloned and the clone cleared of any excising inputs. In order to clone the select2 inputs they must first be removed then reinitialized.
$("#ingredientButton").click(function() {
    destroySelect2s();

    var noOfDivs = $(".ingredientrow").length;
    var clonedDiv = $(".ingredientrow")
        .first()
        .clone(true);
    clonedDiv.find("input").val("");
    clonedDiv.appendTo("#ingredientdiv");
    clonedDiv.attr("id", "ingredientrow" + noOfDivs);

    initSelect2s();
});

// When the remove ingredient button is pressed, the row that contains the button is removed. Should the last remaining button be pressed then the row is instead cleared of its values.
$("#removeIngredient").click(function() {
    var noOfDivs = $(".ingredientrow").length;
    if (noOfDivs > 1) {
        $(this)
            .closest(".ingredientrow")
            .remove();
    } else {
        $(".rform-ingredient")
            .val(null)
            .trigger("change");
        $(".rform-quantity").val(null);
        $(".rform-unit")
            .val(null)
            .trigger("change");
    }
});

// The step buttons work in the same way as the ingredient buttons above
$("#stepButton").click(function() {
    var noOfDivs = $(".steprow").length;
    var clonedDiv = $(".steprow")
        .first()
        .clone(true);
    clonedDiv.find("input").val("");
    clonedDiv.appendTo("#stepdiv");
    clonedDiv.attr("id", "steprow" + noOfDivs);

    initSelect2s();
});

$("#removeStep").click(function() {
    var noOfDivs = $(".steprow").length;
    if (noOfDivs > 1) {
        $(this)
            .closest(".steprow")
            .remove();
    } else {
        $(".s-step").val(null);
    }
});

// To have an input that uses a time picker the Tempus Dominus library is kinda tricked into only submitting a time. The defaultDate is set to midnight and so when the user uses the time picker it acts as thought you are entering a time period rather than an actual time and date. While this works pretty much how I want this does have the limit that the user can only enter times of less than 24hrs. I presume there aren't very many recipes that require that much time so I should be good but I'm sure someone out there will push the limit!
$(function() {
    $("#rformTprep").datetimepicker({
        format: "HH:mm",
        defaultDate: pDate,
        stepping: 5
    });
});

$(function() {
    $("#rformTcook").datetimepicker({
        format: "HH:mm",
        defaultDate: cDate,
        stepping: 5
    });
});

// Function to handle the image picker modal, when a search term is entered a google image search is done and the first 10 images are loaded into a grid in the modal
$("#rmodalSubmit").click(function() {
    // This hides the image grid so that when re-searching for an image the initial placeholder image will not be visible
    $("#rmodalGrid").hide();
    var url =
        "https://www.googleapis.com/customsearch/v1?key=" +
        key +
        "&cx=" +
        cx +
        "&searchType=image&q=";
    var input = $("#rmodalSearch").val();

    $(".rmodal-gridcol")
        .not(":first")
        .remove();

    // get the results from the Google search
    $.get(
        url + input,
        function(data, status) {
            // The image grid is hidden at first to hide the default image which is the first choice, this default image both allows the user to clear their result and also allows a sample image div be cloned and filled with the result images
            $(".rmodal-gridcol").show();
            $("#rmodalGrid").show();
            fitImage($(".rmodal-gridimg").last());
            // For each image in the search, clone the default image and substitute the result
            for (var i = data.items.length - 1; i >= 0; i--) {
                var imglink = data.items[i].link;
                $(".rmodal-gridcol")
                    .first()
                    .clone()
                    .appendTo("#rmodalGrid");
                $(".rmodal-gridcol")
                    .last()
                    .find("img")
                    .attr("src", imglink)
                    .attr("data-height", data.items[i].image.height)
                    .attr("data-width", data.items[i].image.width);
                $(".rmodal-gridcol")
                    .last()
                    .show();
                // Once the image loads it is resized
                $(".rmodal-gridimg")
                    .last()
                    .on("load", function() {
                        fitImage($(this));
                    });
            }
        },
        "json"
    );
    // Prevents the page from reloading
    return false;
});

// When an image is chosen the url for that image is added to a hidden input on the form page so that it can be read by flask
$("#rmodalGrid").on("click", ".rmodal-gridimg", function() {
    var imglink = $(this).attr("src");
    var imgheight = $(this).attr("data-height");
    var imgwidth = $(this).attr("data-width");
    $("#rformImage").attr("src", imglink);
    $("#rformImage").attr("data-height", imgheight);
    $("#rformImage").attr("data-width", imgwidth);
    $("#imageModal").modal("hide");
    $("#rformImageurl").val([imglink, imgheight, imgwidth]);

    // Also the image is refitted to the frame on the form page
    fitImage($("#rformImage"));
});

// Alternate time picker using GIJGO, it didn't really work how I wanted but I'm leaving it here for the moment just in case I have to reconsider
// $('#rformTprep').timepicker({
//     mode: '24hr',
//     value: '00:00',
//     uiLibrary: 'bootstrap4',
//     modal: false
// });
// $('#rformTcook').timepicker({
//     mode: '24hr',
//     value: '00:00',
//     uiLibrary: 'bootstrap4',
//     modal: false
// });
