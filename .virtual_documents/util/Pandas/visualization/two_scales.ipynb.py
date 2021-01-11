get_ipython().run_line_magic("matplotlib", " inline")


import numpy as np
import matplotlib.pyplot as plt


# Create some mock data
t = np.arange(0.01, 10.0, 0.01)
data1 = np.exp(t)
data2 = np.sin(2 * np.pi * t)
print(len(data1))


fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('exp', color=color)
ax1.plot(t, data1, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
ax2.plot(t, data2, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()


import matplotlib
matplotlib.axes.Axes.twinx
matplotlib.axes.Axes.twiny
matplotlib.axes.Axes.tick_params


import pandas as pd
import matplotlib.pyplot as plt


df = pd.DataFrame({
    'name':['john','mary','peter','jeff','bill','lisa','jose'],
    'age':[23,78,22,19,45,33,20],
    'gender':['M','F','M','M','M','F','M'],
    'state':['california','dc','california','dc','california','texas','texas'],
    'num_children':[2,0,0,3,2,1,4],
    'num_pets':[5,1,0,5,2,2,3]
})
df


from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import io


tab_par = "LNREL_700_Follow"
datesq = '0110'
dbtgt = Path('C:/sqlite/2021' + datesq + '_sqlite.db')
dat_dir = dbtgt.parent
(dat_dir / 'csv').mkdir(parents=True, exist_ok=True)  # create csv folder to save temp files
ftab1 = tab_par + '.csv'  # tables and parameters to audit
dfini = pd.read_csv(dat_dir / 'csv' / ftab1)
dfini.head()


dfini.set_index("Date", inplace = True)


Dict = {0: 'Centro',
        1: 'Costa',
        2: 'NorOccidente',
        3: 'Oriente',
        4: 'SurOccidente',
        5: 'NotInBL',
       } 

def labelbar(axr):
    for patch in axr.patches:
        # xy coords of the lower left corner of the rectangle
        bl = patch.get_xy()
        x = 0.2 * patch.get_width() + bl[0]
        # change 0.2 to move the text up and down
        y = 0.2 * patch.get_height() + bl[1] 
        axr.text(x,y,"get_ipython().run_line_magic("d"", " %(patch.get_height()),")
                ha='center', rotation='vertical', fontsize=11, weight = 'bold',color='black')
# create all axes we need
frames = {i:dat for i, dat in dfini.groupby('RegionS')} # dataframe dict per region
fig = plt.figure()
#
for i in Dict:
    rslt_df=frames[Dict[i]] 
    axtemp = plt.subplot(2,3,i+1) # 2 rows, 3 columns, plot position
    rslt_df[['LNREL700_Tot', 'LNREL700_AMLE_Allowed']].plot(kind='bar', ax=axtemp, figsize=(20,10), use_index=True, legend=False)
    labelbar(axtemp)
    axtempi = axtemp.twinx() # secondary axis graph
    axtempi.plot(axtemp.get_xticks(), rslt_df[['Perc']].values, linestyle='-', marker='o', linewidth=2.0, label = 'Percentage', color="r")
    axtemp.set_title(Dict[i])
    locals()['axtemp{0}'.format(i)] = axtempi # for secondary axis sharing
    if i == 0:  # set legend in first plot
        axtempi.legend(loc=0)
        axtempi.legend(bbox_to_anchor=(0.05, 1.02, 1., .102), loc='lower left',
                   ncol=1, mode="expand", borderaxespad=0, frameon=False)
        axtemp.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                   ncol=2, mode="expand", borderaxespad=1.5, frameon=False) 
# share the secondary axes
axtemp0.get_shared_y_axes().join(axtemp0, axtemp1, axtemp2, axtemp3, axtemp4, axtemp5)
# Place a legend above this subplot, expanding itself to fully use the given bounding box.
fig.suptitle('LNREL700 amleAllowed = 0, handoverAllowed = 0')
fig. tight_layout(pad=3.0) # row separation
plt.show()

# writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')


# workbook = xlsxwriter.Workbook('test chart.xlsx')
# wks1=workbook.add_worksheet('Chart')
# wks2=workbook.add_worksheet('Data')
# wks1.write(0,0,'test')

# imgdata=io.BytesIO()
# fig.savefig(imgdata, format='png')
# wks1.insert_image(2,2, '', {'image_data': imgdata})
# workbook.close()


# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('LNREL700.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
dfini.to_excel(writer, sheet_name='Data')
# Get the xlsxwriter objects from the dataframe writer object.
workbook  = writer.book
# worksheet = writer.sheets['Data']
wks1=workbook.add_worksheet('Chart')
imgdata=io.BytesIO()
fig.savefig(imgdata, format='png')
wks1.insert_image(1,1, '', {'image_data': imgdata})
workbook.close()
# Close the Pandas Excel writer and output the Excel file.
# writer.save()















def labelbar(axr):
    for patch in axr.patches:
        # xy coords of the lower left corner of the rectangle
        bl = patch.get_xy()
        x = 0.2 * patch.get_width() + bl[0]
        # change 0.92 to move the text up and down
        y = 0.2 * patch.get_height() + bl[1] 
        axr.text(x,y,"get_ipython().run_line_magic("d"", " %(patch.get_height()),")
                ha='center', rotation='vertical', fontsize=11, weight = 'bold',color='black')

# create all axes we need
frames = {i:dat for i, dat in dfini.groupby('RegionS')}
fig = plt.figure()
#
rslt_df=frames['Centro'] 
ax0 = plt.subplot(231)
rslt_df[['LNREL700_Tot', 'LNREL700_AMLE_Allowed']].plot(kind='bar', ax=ax0, figsize=(20,10), use_index=True, legend=False)
labelbar(ax0)
ax1 = ax0.twinx()
ax1.plot(ax0.get_xticks(), rslt_df[['Perc']].values, linestyle='-', marker='o', linewidth=2.0, label = 'Percentage', color="r")
ax0.set_title('Centro')
#
rslt_df=frames['Costa'] 
ax2 = plt.subplot(232)
rslt_df[['LNREL700_Tot', 'LNREL700_AMLE_Allowed']].plot(kind='bar', ax=ax2, figsize=(20,10), use_index=True, legend=False)
labelbar(ax2)
ax3 = ax2.twinx()
ax3.plot(ax0.get_xticks(), rslt_df[['Perc']].values, linestyle='-', marker='o', linewidth=2.0, color="r")
ax2.set_title('Costa')
#
rslt_df=frames['NorOccidente'] 
ax4 = plt.subplot(233)
rslt_df[['LNREL700_Tot', 'LNREL700_AMLE_Allowed']].plot(kind='bar', ax=ax4, figsize=(20,10), use_index=True, legend=False)
labelbar(ax4)
ax5 = ax4.twinx()
ax5.plot(ax0.get_xticks(), rslt_df[['Perc']].values, linestyle='-', marker='o', linewidth=2.0, color="r")
ax4.set_title('NorOccidente')
#
rslt_df=frames['Oriente'] 
ax6 = plt.subplot(234)
rslt_df[['LNREL700_Tot', 'LNREL700_AMLE_Allowed']].plot(kind='bar', ax=ax6, figsize=(20,10), use_index=True, legend=False)
labelbar(ax6)
ax7 = ax6.twinx()
ax7.plot(ax0.get_xticks(), rslt_df[['Perc']].values, linestyle='-', marker='o', linewidth=2.0, color="r")
ax6.set_title('Oriente')
#
rslt_df=frames['SurOccidente'] 
ax8 = plt.subplot(235)
rslt_df[['LNREL700_Tot', 'LNREL700_AMLE_Allowed']].plot(kind='bar', ax=ax8, figsize=(20,10), use_index=True, legend=False)
labelbar(ax8)
ax9 = ax8.twinx()
ax9.plot(ax0.get_xticks(), rslt_df[['Perc']].values, linestyle='-', marker='o', linewidth=2.0, color="r")
ax8.set_title('SurOccidente')
#
rslt_df=frames['NotInBL'] 
ax10 = plt.subplot(236)
rslt_df[['LNREL700_Tot', 'LNREL700_AMLE_Allowed']].plot(kind='bar', ax=ax10, figsize=(20,10), use_index=True, legend=False)
labelbar(ax10)
ax11 = ax10.twinx()
ax11.plot(ax0.get_xticks(), rslt_df[['Perc']].values, linestyle='-', marker='o', linewidth=2.0, color="r")
ax10.set_title('NotInBL')
#
ax1.legend(loc=0)
ax1.legend(bbox_to_anchor=(0.05, 1.02, 1., .102), loc='lower left',
           ncol=1, mode="expand", borderaxespad=0, frameon=False)
ax0.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=2, mode="expand", borderaxespad=1.5, frameon=False)
# share the secondary axes
ax1.get_shared_y_axes().join(ax1, ax3, ax5, ax7, ax9, ax11)
# Place a legend above this subplot, expanding itself to
# fully use the given bounding box.
fig.suptitle('LNREL700 amleAllowed = 0, handoverAllowed = 0')
fig. tight_layout(pad=3.0)
plt.show()



options=['Costa']
rslt_df = dfini[dfini['RegionS'].isin(options)]  
rslt_df



