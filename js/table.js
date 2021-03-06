// Create tables dynamically for nidm results

function isInArray(array, element) {
    return array.indexOf(element) > -1;
}

function nidm_table(image_file) {
           
    data = peaks[nidm]

    $("#papayaContainer0").css("padding-left","0px")     

    var tablehtml = '<div class="fresh-table full-color-blue"><output id="list"></output><div class="toolbar"><button id="export" class="btn btn-default">Export SVG</button></div><table id="fresh-table" class="table"><thead>'

    // Add columns to the table
    for(var i=0; i<columns.length; i++) {
        tablehtml = tablehtml + '<th data-field="' + columns[i] + '" data-sortable="true">' + columns[i] + '</th>'
    }

    tablehtml = tablehtml + '<th data-field="actions"></th></thead><tbody>'

    // These are fields that should be floats
    float_fields = ["x","y","z","pvalue_fwer","pvalue_uncorrected","equivalent_zstatistic"]

    // We will keep track of coordinate names and not append repeats
    coordinate_names = []

    // Now add data to the table!
    for(var i=0; i<data.length; i++) {
        result = data[i]           

        // Only add data for image selected
        if (result[location_key] == image_file){


            // If we have not added the coordinate
            if (!isInArray(coordinate_names,result["coord_name"])) {

                // Add the coordinate so we don't add it again            
                coordinate_names.push(result["coord_name"])

                // Start a new row
                tablehtml = tablehtml + '<tr style="background-color:none">'

                // Match result column names to our columns
                for(var ii=0; ii<columns.length; ii++) {
                    if(columns[ii] in result){
                        tablehtml = tablehtml + '<td>' + result[columns[ii]] + '</td>'
                    } else {
                        tablehtml = tablehtml + '<td></td>'
                    }   
                }

                tablehtml = tablehtml + '<td><button class="btn btn-default circle" style="padding:2px" onclick=move_coordinate(' + result["x"] + ',' + result["y"] + ',' + result["z"] + ')><i class="fb icon-crosshair"></i></button></td></tr>'

                }
    
            }  

    }
    tablehtml = tablehtml + '</tbody></table></div>'

    $("#tablerow").empty()
    $("#tablerow").append($(tablehtml))

    var $table = $('#fresh-table'),
    $exportBtn = $('#export'), 
    full_screen = false,
    window_height;
 
    window_height = $(window).height();
    table_height = window_height - 20;
                   
    $table.bootstrapTable({
        toolbar: ".toolbar",
        showRefresh: false,
        search: true,
        showToggle: false,
        showColumns: false,
        pagination: true,
        striped: true,
        sortable: true,
        height: table_height,
        pageSize: 25,
        pageList: [25,50,100],
                
        formatShowingRows: function(pageFrom, pageTo, totalRows){
             //do nothing here, we don't want to show the text "showing x of y from..." 
        },
        formatRecordsPerPage: function(pageNumber){
            return pageNumber + " rows visible";
        },
        icons: {
            refresh: 'fa fa-refresh',
            toggle: 'fa fa-th-list',
            columns: 'fa fa-columns',
            detailOpen: 'fa fa-plus-circle',
            detailClose: 'fa fa-minus-circle'
         }
    });
            
    window.operateEvents = {
        //'click .like': function (e, value, row, index) {
        //    alert('You click like icon, row: ' + JSON.stringify(row));
        //    console.log(value, row, index);
        //},
        //'click .edit': function (e, value, row, index) {
        //    alert('You click edit icon, row: ' + JSON.stringify(row));
        //    console.log(value, row, index);    
        //},
        'click .remove': function (e, value, row, index) {
        $table.bootstrapTable('remove', {
            field: 'id',
            values: [row.id]
            });   
           }
     };
            
     $exportBtn.attr("onclick","export_svg()")
            
     $(window).resize(function () {
        $table.bootstrapTable('resetView');
     });    
 
     $("#export").css("margin-left",30)

}
