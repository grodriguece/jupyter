from plotnine import *
from plotnine.data import mtcars
def facet_pages(column):
    base_plot = [
        aes(x='wt', y='mpg', label='name'),
        geom_text(),
        ]
    for label, group_data in mtcars.groupby(column):
        yield ggplot(group_data) + base_plot + ggtitle(label)
save_as_pdf_pages(facet_pages('cyl'))



