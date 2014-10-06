google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);
function drawChart(a,type,id,width) {
    var data = null;
    var options = null;
    var chart = null;
    if ( type == "AreaChart")
    {
        data = new google.visualization.DataTable();
        data.addColumn("string","Date");
        //消耗量+提示
        data.addColumn("number","Usage");
        data.addColumn({type:"string",role:"tooltip"});    
        //0.2GB基準線
        data.addColumn("number","0.2GB");
        data.addColumn({type:"boolean",role:"certainty"});
        data.addColumn({type:"string",role:"annotation"});
        //0.4GB基準線
        data.addColumn("number","0.4GB");
        data.addColumn({type:"boolean",role:"certainty"});
        data.addColumn({type:"string",role:"annotation"});
        //0.6GB基準線
        data.addColumn("number","0.6GB");
        data.addColumn({type:"boolean",role:"certainty"});
        data.addColumn({type:"string",role:"annotation"});
        //0.8GB基準線
        data.addColumn("number","0.8GB");
        data.addColumn({type:"boolean",role:"certainty"});
        data.addColumn({type:"string",role:"annotation"});

        var gb_line_label =[];
        for (i=1;i<=4;i++) {
            number = 0.2 * i ;
            //防止奇怪的算術結果
            gb_line_label[i-1]=  Math.round(number*10)/10 + "GB";
            //填入基準線
            a[a.length - 1][ i*3 +2 ] = gb_line_label[i-1];
        }

        data.addRows(a);
        options = {
            hAxis: {title: 'Date',  titleTextStyle: {color: '#333'}},
            vAxis: {minValue: 0},
            height: 500,
            width: width,
            backgroundColor: 'none',
            legend: { position: 'none' },
            series: {
                1: { areaOpacity: 0, color: "#000" },
                2: { areaOpacity: 0, color: "#000" },
                3: { areaOpacity: 0, color: "#000" },
                4: { areaOpacity: 0, color: "#000" }
            },
        };
        var chart = new google.visualization.AreaChart(document.getElementById(id));  
    }
    else if( type == "PieChart")
    {

        data = google.visualization.arrayToDataTable(a);

        options = {
            width: width,
        };
        var chart = new google.visualization.PieChart(document.getElementById(id));
    }
    chart.draw(data, options);
}