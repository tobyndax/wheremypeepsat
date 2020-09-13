import plotly
import plotly.graph_objects as go
import numpy as np

bind_script = '''
var graph = document.getElementsByClassName("plotly-graph-div js-plotly-plot")[0];
var update;

function pan(axis, dx, mode=1) {
    axis += 'axis';
    var [min, max] = graph._fullLayout[axis].range;
    dx *= max - min;
    update[axis+'.range'] = [min+dx, max+mode*dx];
}

function panX(dx) {pan('x', dx)}

document.addEventListener("keydown", function(e){
    var key = e.key;
    if (e.ctrlKey) key = 'Ctrl+' + key;
    console.log(e, key);
    var fac = 1;   // pan and zoom factor
    update = {};
    var extremes = graph._fullData[0]._extremes;  // only first data set
    switch (key) {
    case 'ArrowRight': panX(fac); break;
    case 'ArrowLeft': panX(-fac); break;
    default: return;
}
Plotly.relayout(graph, update);
});
'''

def script_decorator(func):
    # append binding script
    def function_wrapper(*x):
        return (func(*x) or '') + bind_script
    return function_wrapper

plotly.offline.offline.build_save_image_post_script = script_decorator(plotly.offline.offline.build_save_image_post_script)

def plotFeedback(audio_segs, subSample, silenceScale):
    offset = 0
    fig = go.Figure()
    for i, seg in enumerate(audio_segs):
        y = np.array(seg.get_array_of_samples())
        start = offset
        end = len(seg) + offset
        offset = end
        t = np.linspace(start, end ,len(y))
        fig.add_trace(
            go.Scatter(x=t[::subSample]/1000, y=y[::subSample],
                       mode='lines',
                       name='lines'))
    fig.add_trace(
        go.Scatter(x=np.array([0, end])/1000, y=np.array([silenceScale, silenceScale]),
                   mode='lines',
                   name='lines'))
    fig.update_layout(showlegend=False)
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="linear"
        )
    )
    initial_range = [0, 10]
    fig['layout']['xaxis'].update(range=initial_range)
    plotly.offline.plot(fig)

