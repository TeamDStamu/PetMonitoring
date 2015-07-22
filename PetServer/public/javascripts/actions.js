function loadPieData() {
    //alert("Data being refreshed!");
    var pieChart = c3.generate({
        data: {
            url: '/petm/json/pie',
            mimeType: 'json',
            type : 'pie'
        },
        bindto: '#pieChart'
    });
}

function loadLineData() {
    //alert("Data being refreshed!");
    var lineChart = c3.generate({
        data: {
            url: '/petm/json/chart',
            mimeType: 'json'
        },
        bindto: '#chart'
    });
}