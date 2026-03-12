import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
pio.renderers.default = 'browser'


def _code_mapping(df, src, targ):
    """ Map labels in src and targ columns to integers """

    labels = pd.concat([df[src], df[targ]]).unique().tolist()

    # Get integer codes
    codes = range(len(labels))

    # Create label to code mapping
    lc_map = dict(zip(labels, codes))

    # Substitute names for codes in dataframe
    new_df = df.copy()
    new_df[src] = new_df[src].map(lc_map)
    new_df[targ] = new_df[targ].map(lc_map)

    # return the new df along with the list of labels that were converted
    return new_df, labels


def make_sankey(df, src, targ, vals=None,  **kwargs):
    """ Generate a sankey diagram
    df - Dataframe
    src - Source column
    targ - Target column
    vals - Values column (optional)
    kwargs - optional supported params: pad, thickness, line_color, line_width.
    """

    # Handle optional vals column
    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)  # all values are identical (e.g., 1)

    # Convert column labels to integer codes
    df, labels = _code_mapping(df, src, targ)

    # Extract customizations from kwargs
    pad = kwargs.get('pad', 50)
    thickness = kwargs.get('thickness', 50)
    line_color = kwargs.get('line_color', 'black')
    line_width = kwargs.get('line_width', 0)

    # Construct sankey figure
    link = {'source': df[src], 'target': df[targ], 'value': values,
            'line': {'color': line_color, 'width': line_width}}

    node = {'label': labels, 'pad': pad, 'thickness': thickness,
            'line': {'color': line_color, 'width': line_width}}
    
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    # Optionally adjusting the width and height of the sankey diagram
    width = kwargs.get('width', 1200)
    height = kwargs.get('height', 800)
    fig.update_layout(
        autosize=False,
        width=width,
        height=height
    )


    # Make sankey simply returns the figure
    # If you want to actually display the figure, use show sankey
    return fig


def show_sankey(df, *cols, vals=None, png=None, **kwargs):
    """
    Make AND Show the sankey diagram. Optionally save it to a file
    df - The dataframe
    *cols - list containing ordered columns
    vals - optional values column (line thickness)
    png - name of the .png image file to be generated
    kwargs - optional customizations like thickness, line color, etc.
    """

    # list to store dataframes with different column pairs taken from
    # original columns

    combined_dfs= []

    # Loops through each column of df and creates column pairs
    # ex: (0, 1), 2 and 0, (1, 2)
    for i in range(len(cols) - 1):
        left_col = cols[i]
        right_col = cols[i + 1]

    # create a "combined dataframe" which contains left and right columns
    # collected from original df in loop
    # labeled 'src', 'targ' so make_sankey can read the df

        comb_df = df[[left_col, right_col]].copy()
        comb_df.columns = ['src', 'targ']

    # use inputted vals as values or set all values to 1
        if vals is None:
            comb_df['value'] = 1
        else:
            comb_df['value'] = df[vals]

    # add each new dataframe created in loop to combined_dfs
        combined_dfs.append(comb_df)

    # stacks the dataframes on top of each other saved as stacked_df
    stacked_df = pd.concat(combined_dfs, axis=0)


    # combines values and creates a single row for any rows with same src and
    # targ
    stacked_df = stacked_df.groupby(['src', 'targ'], as_index=False)[
        'value'].sum()

    # call make_sankey
    fig = make_sankey(stacked_df, 'src', 'targ', 'value', **kwargs)

    fig.show()

    if png:
        fig.write_image(png)

