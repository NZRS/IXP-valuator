
$.getJSON('aggregated-metrics.json', function(data, status) {
    hop_data = [];
    $.each(data['hops'], function(entry, i) {
        hop_data.push({
            x: i['x'],
            y: i['y'],
            name: entry,
            autobinx: false,
            opacity: 0.7,
            histnorm: "percent",
            type: "histogram",
            xbins: {
                start: 0,
                end: 20,
                size: 1
            }
        });
    });

    // Force the visualization to happen here
    var layout = {
        bargap: 0.05,
        bargroupgap: 0.1,
        barmode: "group",
        title: "Hop Count",
        xaxis: {title: "Hop"},
        yaxis: {title: "Trace percentage"}
    };
    Plotly.newPlot('hop_count', hop_data, layout)

    // Display the RTT information
    rtt_data = []
    $.each(data['rtt'], function(entry, i) {
        rtt_data.push({
            x: i['x'],
            y: i['y'],
            name: entry,
            autobinx: false,
            opacity: 0.7,
            histnorm: "percent",
            type: "histogram",
            xbins: {
                start: 0,
                end: 100,
                size: 5
            }
        });
    });
    var layout = {
        bargap: 0.05,
        bargroupgap: 0.1,
        barmode: "group",
        title: "RTT",
        xaxis: {title: "RTT (s)"},
        yaxis: {title: "Trace percentage"}
    };
    Plotly.newPlot('rtt_display', rtt_data, layout)

});
