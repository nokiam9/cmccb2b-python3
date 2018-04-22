###  flask v0.2 on 201804 ###

#### 开发记录  ####
- 修改`models.py`，根据第二个spider的开发，调整了collection name

#### 待办任务  ####
- index.html的type nav选中时颜色为active
- index.html增加图表展示
- index.html如何设置footer，pagination按钮组如何右对齐
- 研究关键词的过滤方式
- 研究https的实现方式

#### 经验之谈  ####
- `<a herf="#" onclick="gotoPage('2')">`标签等组件包含了默认动作，例如herf属性就会触发页面跳转，导致不需要的页面刷新，
可以通过控制return false的方式阻止默认动作的发生，具体参见[文档](https://www.cnblogs.com/weiwang/archive/2013/08/19/3268374.html) 