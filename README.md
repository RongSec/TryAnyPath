# TryAnyPath
一款用于穷举拼接url来达成未授权访问的小工具

## TODO
缝合或者调用echole/httpx，对可访问的情况进行筛选

添加规则判断，对含有info,username等敏感的目录进行筛选提取。

图形化界面/等到功能完善了重构成java或者go。

添加常见的未授权路径的遍历（但是量太大了，100多个path就会生成24000多个拼接path）

## 工具逻辑
穷举式拼接所有path，来达成尽可能多的未授权访问，目前仅能实现已知path的提取和拼接。

逻辑如下：

假设文件中有3个路径，分别为/a/b/c,/d/e/f,/i/j/k,那么提取出的1级目录就是a,d,i,拼接后的目录就是/d/a/b/c,/d/i/j/k/,/a/d/e/f,/a/i/j/k,/i/a/b/c,/i/d/e/f。

对"/"缺失的情况做了适配，杜绝了提取数据的缺损。

对匹配到的1级目录是文件名的情况进行了删除，防止其被当作1级目录拼接给待测path。

对wih获取的带有参数传递的情况可以进行着重显示。

## 使用场合
借助WIH等工具提取出了网站url/path后

## 使用方法

-f 指定txt文件

-z 指定zip文件

1. 安装依赖
pip3 install pandas
如果正常pip可以装的话就可以不用虚拟环境
python3 -m venv myenv
source myenv/bin/activate
pip install pandas
用完了就退出
deactivate

2. 参数设置
-f 指定txt文件
-z 指定zip文件

## 场景示例

输出结果

分别是：原数据，带有参数的源数据，提取的第一级目录，拼接后数据，带有参数的拼接后数据

<img width="873" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/43ceaf0d-115f-4b2f-b3ee-2d87ad24543d">

有效性验证

通过遍历拼接访问到了未授权的下载接口

<img width="1141" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/f432aa5f-4fb3-42d2-808d-4165e73edc8c">

<img width="615" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/405e4f4c-36c0-4ccc-849e-2b3361b817c8">

