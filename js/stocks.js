function getStocks(){
    $.getJSON('/getStocks',function(stocks){
	var x={};
	var y={};
	var stockx=[];
	var stocky=[];
	for (var stock in stocks){
	    for (var data in stock["data"]){
		stockx.push(data["time"]);
	    }
	    return stockx;
	}
    });
}



function charts(){
    var r = Raphael("simpleExample");
    var chart = r.g.linechart(
	10, 10,      // top left anchor
	490, 180,    // bottom right anchor
	[
	    [1, 2, 3, 4, 5, 6, 7],        // red line x-values
	    [3.5, 4.5, 5.5, 6.5, 7, 8]    // blue line x-values
	], 
	[
	    [12, 20, 23, 15, 17, 27, 22], // red line y-values
	    [10, 20, 30, 25, 15, 28]      // blue line y-values
	], 
	{
	    nostroke: false,   // lines between points are drawn
	    axis: "0 0 1 1",   // draw axes on the left and bottom
	    symbol: "disc",    // use a filled circle as the point symbol
	    smooth: true,      // curve the lines to smooth turns on the chart
	    dash: "-",         // draw the lines dashed
	    colors: [
		"#995555",       // the first line is red  
		"#555599"        // the second line is blue
	    ]
	});
}

$(document).ready(function(){

    getStocks;
    charts;
}