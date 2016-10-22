var datafile = location.search.substr(1);
$.getJSON(datafile, function(data, status) {
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

    hop_cdf_data = [];
    $.each(data['hops_cdf'], function(entry, i) {
        hop_cdf_data.push({
            x: i['x'],
            y: i['y'],
            name: entry,
            mode: "lines"
        });
    });

    // Force the visualization to happen here
    var layout = {
        title: "Hop CDF",
        xaxis: {title: "# Hop"},
        yaxis: {title: "Cumulative of traces"}
    };
    Plotly.newPlot('hop_cdf', hop_cdf_data, layout)

    // Display the RTT information
    rtt_cdf_data = []
    $.each(data['rtt_cdf'], function(entry, i) {
        rtt_cdf_data.push({
            x: i['x'],
            y: i['y'],
            name: entry,
            mode: 'lines'
        });
    });
    var layout = {
        title: "RTT CDF",
        xaxis: {title: "RTT (ms)"},
        yaxis: {title: "Cumulative of traces"}
    };
    Plotly.newPlot('rtt_cdf', rtt_cdf_data, layout)
});
