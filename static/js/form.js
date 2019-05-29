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

$(window).resize(function() {
    // Had to put this condition in because when using the keyboard on Android it causes the viewport to change which kills the select2 while you're trying to use them *rolling eyes emoji*
    if ($(window).width() != winwidth) {
        destroySelect2s();
        initSelect2s();
        winwidth = $(window).width();
    }
});

$(function() {
    $('[data-toggle="tooltip"]').tooltip();
});

$(document).ready(function() {
    // Set select2 defaults
    $.fn.select2.defaults.set("theme", "bootstrap4");
    $.fn.select2.defaults.set("tags", "true");
    $.fn.select2.defaults.set("allowClear", "true");
    initSelect2s();
});

function numberer(parent, classname) {
    console.log(classname);
    $(parent).each(function(index, el) {
        console.log($(this).find(classname));
        $(this)
            .find(classname)
            .attr("name", classname.replace(".", "") + index);
    });
}

$("#ingredient-button").click(function() {
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

$("#remove-ingredient").click(function() {
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

$("#step-button").click(function() {
    var cloneStep = $("#steprow").clone();
    cloneStep.find("input").val("");
    cloneStep.appendTo("#stepdiv");
});

$("#step-button").click(function() {
    var noOfDivs = $(".steprow").length;
    var clonedDiv = $(".steprow")
        .first()
        .clone(true);
    clonedDiv.find("input").val("");
    clonedDiv.appendTo("#stepdiv");
    clonedDiv.attr("id", "steprow" + noOfDivs);

    initSelect2s();
});

$("#remove-step").click(function() {
    var noOfDivs = $(".steprow").length;
    if (noOfDivs > 1) {
        $(this)
            .closest(".steprow")
            .remove();
    } else {
        $(".s-step").val(null);
    }
});

$(function() {
    $("#rform-tprep").datetimepicker({
        format: "HH:mm",
        defaultDate: Date.parse("2000-01-01T00:00"),
        stepping: 5
    });
});

$(function() {
    $("#rform-tcook").datetimepicker({
        format: "HH:mm",
        defaultDate: Date.parse("2000-01-01T00:00"),
        stepping: 5
    });
});

// Alternate time picker using GIJGO
// $('#rform-tprep').timepicker({
//     mode: '24hr',
//     value: '00:00',
//     uiLibrary: 'bootstrap4',
//     modal: false
// });
// $('#rform-tcook').timepicker({
//     mode: '24hr',
//     value: '00:00',
//     uiLibrary: 'bootstrap4',
//     modal: false
// });
