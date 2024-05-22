# FindAnyThing
一款基于WIH(目前)的穷举拼接API并访问从而达成对未授权/敏感信息的获取并尽力获取准确baseurl的工具。

下一步将直接实现类似urlfinder等的深度爬取并结合WIH的敏感信息获取与验证的功能，直接一键化使用，目前只有一个初始版本，爬的东西时多时少的。无语子···

我个人觉得信息收集是非常需要细心的，特别是在如今高强度的与设备对抗以及甲方日常化的演练中，自动化的逻辑就那么几个，想要在一轮轮演练之后依旧能取得成果是一件困难的事情，特别是我在最近的一次众测中发现了有一个未授权的路径只有经过拼接才能访问，我翻了翻urlfinder的文档还有我另一个常常使用的工具jjjjjjjjjjjjjs，经过对同一目标的测试都没有成功的复现这个漏洞，经过仔细的理解工具，我发现urlfinder的fuzz功能基于对所有筛选出的根目录的200响应进行拼接，jjjjjjjjjjjjjs则没有这个功能，只能对200的根目录进行swagger等的爆破，可是实际情况是这个根目录直接访问是404。

这款工具的目的就是将让我们从自动化中跳出来，因为我认为自动化应该做的是重复的机械工作而不是替代工作。

## 流程图

![未命名文件](https://github.com/RongSec/TryAnyPath/assets/96337516/1d1f3c0e-cbc2-4622-9816-8a70a7c11a6d)

## TODO

添加规则判断，对含有info,username等敏感的目录进行筛选提取。

图形化界面/等到功能完善了重构成go。

对访问码200的根目录项进行swagger等api遍历。

想添加异步访问和随机并发，防止被ban。

在web请求结束后再添加一个逻辑，对500等异常馅响应单独重跑去把成功数据覆盖掉失败数据。

## 工具逻辑

逻辑如下：

假设文件中有3个路径，分别为/a/b/c,/d/e/f,/i/j/k,那么提取出的1级目录就是a,d,i,拼接后的目录就是/d/a/b/c,/d/i/j/k/,/a/d/e/f,/a/i/j/k,/i/a/b/c,/i/d/e/f。

对"/"缺失的情况做了适配，杜绝了提取数据的缺损。

对匹配到的1级目录是文件名的情况进行了删除，防止其被当作1级目录拼接给待测path。

对wih获取的带有参数传递的情况可以进行分类显示。

## 使用场合

借助WIH等工具提取出了网站url/path后

## 使用方法
首先使用WIH

./wih -t target.txt -r wih_rules.yml -f -a -c 4 -P 4 -J 

<img width="884" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/6f901b9a-0dd7-4ec5-a35f-656e1d4dbc34">

1. 创建一个python虚拟环境

python3 -m venv myenv

source myenv/bin/activate

2. 直接使用fuzz功能在处理完所有数据后会询问用户

python3 FindAnyTHing.py -t target -o result/test.csv //target是存放WIH处理后的所有json文件的目录，result/test.csv是输出的文件，没有就会新建。

<img width="1298" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/1ae917c4-784c-4dbd-b3d2-659319c78f53">


## 场景示例

输出结果

1. 选择了进行fuzz会在终端输出每一个的请求情况。
这里只进行了简单的请求，下一步想添加异步访问和随机并发，防止被ban。

<img width="1459" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/8df67e26-3f11-4c2e-9449-3d19122b70c6">

访问结束后还会问你要不要继续请求
<img width="1363" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/ed7b6e74-167a-4747-b703-b5657acd8687">
你可以去看csv文件，如果你觉得线程太高了想要重新访问，可以直接重跑。

这里设计的todo是在web请求结束后再添加一个逻辑，对500等异常馅响应单独重跑去把成功数据覆盖掉失败数据。
<img width="356" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/0ebfa7a6-e700-4f6a-84f0-e52294687d3e">

根据不同类型去筛选数据

<img width="432" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/d2c9d61e-63ef-479a-a36b-35f40fb8f728">

最终的数据如下

<img width="1303" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/368a848d-1ffd-49e2-83be-b5e0ddbaa14a">


## 有效性验证

通过遍历拼接访问到了未授权的下载接口

<img width="1141" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/f432aa5f-4fb3-42d2-808d-4165e73edc8c">

<img width="615" alt="image" src="https://github.com/RongSec/TryAnyPath/assets/96337516/405e4f4c-36c0-4ccc-849e-2b3361b817c8">

