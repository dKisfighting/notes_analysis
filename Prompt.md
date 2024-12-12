# 需求记录

## 2024-01-01
请帮我编写Python代码，实现小红书笔记处理的功能：
1. 读取路径为"D:\Cursor\小红书爆款笔记抓取\demo.xlsx"的xlsx文件，文件首行是标题，第一列是笔记官方地址，循环取第一列的数据，然后在网页中打开，网页请求需要cookie,请求头里包含cookie
2. 获取网页的数据，分别取id="detail-desc"和id="hash-tag"的数据作为笔记正文和笔记话题，追加到每行数据后面作为新的一列，注意每篇笔记内容的hash-tag有多个，要取完所有的。笔记中的detail-desc可能是空的，hash-tag也有可能是空的，如果空则写入空数据。如果detail-desc的内容仅包含hash-tag，则一样写入空数据。最后把生成的新数据写入到新的xlsx文件
3. 执行过程中务必打印必要的日志 