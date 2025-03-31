import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc

def img_chart(p_list):
    
    path = 'C:\\Windows\\Fonts\\HanSantteutDotum-Regular.ttf'
    font_name = fm.FontProperties(fname=path).get_name()

    rc('font', family=font_name)


    selected_data = p_list[:5]

    labels, values = zip(*selected_data)

    plt.figure(figsize=(6,2))
    
    plt.barh(labels, values, color='skyblue', height=0.5)
    plt.title('인기 메뉴')
    # plt.ylabel('메뉴')
    # plt.xlabel('판매량')

    plt.tight_layout()

    plt.savefig('img\chart.png', format='png')




