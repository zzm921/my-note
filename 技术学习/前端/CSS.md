##css的单位
html中的单位只有一种，那就是像素px，所以单位是可以省略的。但是在css中不一样。css中的单位是必须要写的，因为他没有默认单位。
- 绝对单位：
    - in:英寸
    - cm：厘米

    - mm：毫米

    - pt：点Point，或者叫英镑

    - pc：皮卡（1皮卡=12点）

- 相对单位
    - px：像素

    - em：印刷单位，相当于12个点

    - %：百分比，相对周围的文字的大小

##字体属性
####行高  line-height
css中，所有的行，都有行高。盒子模型的padding，局对不是直接作用在文字上的，而是作用在行上的。
####font字体属性
css样式中，字体属性有以下几种
```

p{
	font-size:50px; 		/*字体大小*/
	line-height: 30px;      /*行高*/
	font-family:幼圆,黑体; 	/*字体类型：如果没有幼圆就显示黑体，没有黑体就显示默认*/
	font-style:italic ;		/*italic表示斜体，normal表示不倾斜*/
	font-weight:bold;	/*粗体：属性值写成bolder也可以*/
	font-variant:small-caps;  /*小写变大写*/
}

```
上面这些属性中，字号、行高、字体这三个属性是最常见的
######1、字号、行高、字体三大属性：
（1）字号
    font-size:14px
（2）行高
    line-height:24px;

（3）字体
    font-familu:'宋体'

是否加粗属性即上面三个属性，我们可以连写:(是否加粗、字号font-size、行高line-height、字体font-family)
格式
    font:加粗 字号/行高/ 字体

如
    font:400 14px/24px '宋体'

ps:400是nomal  700是bold
######2、字体属性的说明：
（1）网页中不是所有字体都能用，因为这个字体要看用户的电脑里装没装 ​