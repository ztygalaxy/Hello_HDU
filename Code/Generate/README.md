
## 1. 测试运行环境:

```TXT
python==3.9.7
matplotlib==3.4.3
numpy==1.20.3
pandas==1.3.4
```


## 2. 使用方法:
1. `csv_data/template/`下提供了模板文件，只需要将XXXX改为对应年份，并添加总分数据列即可。
   * `XXXX_081200_admission.csv` 计算机**学硕录取**名单初试总分
   * `XXXX_081200_reexamine.csv` 计算机**学硕复试**名单初试总分
   * `XXXX_085404_admission.csv` 计算机**专硕录取**名单初试总分
   * `XXXX_085404_reexamine.csv` 计算机**专硕复试**名单初试总分
2. 添加完数据后，修改`score_distribution.py`文件中`经常修改的参数`即可。代码文件中有详细注释。
3. 修改参数后，使用python运行，会在同级目录下生成png图片并可弹出`matplotlib`窗口。